"""Audit the non-scalar Pauli normalizer against the last cross-D Z2 class.

The connected endpoint gauge removes all continuous cross-D amplitude freedom.
The disconnected *scalar* residual gauge removes one of the two Smith Z2
components, leaving at most one genuine D-amplitude class split.

This script includes the projective Pauli normalizer of the fixed epsilon-minus
seed normal form.  On each of the eight multiplicity-two fusion spaces choose

    G_v = X^a Z^b,  (a,b) in F2^2,

modulo scalar center.  Conjugation preserves the three Pauli axes but flips
pairs of seed signs:

    L=X : b,
    M=Z : a,
    R=+/-Y : a+b.

Multiplicity-one scalar gauge transformations can compensate those sign flips
while keeping the canonical A/B/C representative fixed.  The compensation
problem is solved exactly from the Smith decomposition of the scalar+seed
monomial gauge matrix.  For every allowed Pauli-normalizer generator and every
one of the sixteen deep scalar/chirality branches, the script then:

1. reconstructs the unique projective cross-D shapes;
2. applies the actual matrix basis change G_target^{-1} T G_source;
3. verifies it is proportional to the same one-dimensional intertwiner shape;
4. combines that proportionality phase with an exact scalar-gauge compensation;
5. verifies all 168 homogeneous cross-D binomial equations;
6. evaluates the two Smith Z2 component characters of the cross-D amplitude
   solution group.

If the scalar disconnected gauge direction plus the Pauli-normalizer images
span rank two in that component group for every branch, the final Z2 is gauge
and the historical single D-amplitude witness is exhaustive modulo full
trivalent gauge.
"""
from __future__ import annotations

import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

import r22_epsminus_d_amplitude as da
import r22_epsminus_d_trace as tr
import r22_epsminus_d_probe as dp
import r22_epsminus_d_amplitude_gauge_audit as aga
import r22_epsminus_d_discrete_gauge_audit as dga


def smith_decomp(M):
    Ddm, Sdm, Tdm = smith_normal_decomp(DomainMatrix.from_Matrix(M).convert_to(ZZ))
    return Ddm.to_Matrix(), Sdm.to_Matrix(), Tdm.to_Matrix()


def gf2_rref_nullspace(row_bits, ncols):
    rows = [int(r) for r in row_bits if r]
    pivots = []
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(rows)) if (rows[i] >> c) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> c) & 1):
                rows[i] ^= rows[r]
        pivots.append(c)
        r += 1
    rows = rows[:r]
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for f in free:
        v = 1 << f
        for i, p in enumerate(pivots):
            if (rows[i] >> f) & 1:
                v |= 1 << p
        basis.append(v)
    return basis, pivots


def gf2_rank(vectors):
    rows = [int(v) for v in vectors if v]
    r = 0
    bit = 0
    while bit < 64 and r < len(rows):
        p = next((i for i in range(r, len(rows)) if (rows[i] >> bit) & 1), None)
        if p is None:
            bit += 1
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> bit) & 1):
                rows[i] ^= rows[r]
        r += 1
        bit += 1
    return r


def mod1(q):
    q = sp.Rational(q)
    return q - sp.floor(q)


def phase4(q):
    q = mod1(q)
    x = sp.simplify(4 * q)
    if not x.is_Integer:
        raise AssertionError(("phase is not a fourth root", q, x))
    return int(x) % 4


def root_phase4(z):
    z = sp.simplify(z)
    table = {sp.Integer(1): 0, sp.I: 1, sp.Integer(-1): 2, -sp.I: 3}
    if z not in table:
        raise AssertionError(("unexpected Pauli proportionality root", z))
    return table[z]


def proportionality(A, B):
    """Return alpha with A=alpha*B, or fail exactly."""
    alpha = None
    for i in range(B.rows):
        for j in range(B.cols):
            if B[i, j] != 0:
                candidate = sp.simplify(A[i, j] / B[i, j])
                if alpha is None:
                    alpha = candidate
                elif sp.simplify(candidate - alpha) != 0:
                    raise AssertionError(("not proportional", A, B))
            elif A[i, j] != 0:
                raise AssertionError(("support changed under Pauli normalizer", A, B))
    if alpha is None or sp.simplify(A - alpha * B) != sp.zeros(*A.shape):
        raise AssertionError(("not proportional", A, B, alpha))
    return sp.simplify(alpha)


def cross_component_characters(A):
    D, _S, T = smith_decomp(A)
    positions = [i for i in range(min(D.shape)) if abs(int(D[i, i])) == 2]
    if len(positions) != 2:
        raise AssertionError(("expected two cross-D Z2 Smith positions", positions))
    Tinv = T.inv()
    W = sp.Matrix([list(Tinv[pos, :]) for pos in positions])
    B, _ = aga.residual_gauge_matrix()
    if W * B != sp.zeros(2, B.cols):
        raise AssertionError("cross-D torsion characters do not vanish on connected endpoint gauge")
    return W


def seed_flip_matrix(seed_keys):
    """24 x 16 F2 map from local Pauli choices to seed sign flips."""
    P = sp.zeros(len(seed_keys), 2 * len(tr.SPACES))
    for i, key in enumerate(seed_keys):
        space, pos = dp.underlying_h_space(key)
        v = tr.SPACE_INDEX[space]
        a, b = 2 * v, 2 * v + 1
        if pos == "L":
            P[i, b] = 1
        elif pos == "M":
            P[i, a] = 1
        elif pos == "R":
            P[i, a] = 1
            P[i, b] = 1
        else:
            raise AssertionError((key, pos))
    return P


def vector_bits(v):
    out = 0
    for i, x in enumerate(v):
        if int(x) & 1:
            out |= 1 << i
    return out


def label_bits_from_phase(W_phase):
    bits = 0
    for i in range(W_phase.rows):
        p = phase4(W_phase[i, 0])
        if p not in (0, 2):
            raise AssertionError(("cross-D component character is not +/-1", i, W_phase[i, 0], p))
        if p == 2:
            bits |= 1 << i
    return bits


def pauli_gauges(qbits):
    I2 = sp.eye(2)
    out = []
    for v in range(len(tr.SPACES)):
        a = (qbits >> (2 * v)) & 1
        b = (qbits >> (2 * v + 1)) & 1
        G = I2
        if a:
            G = G * dp.PX
        if b:
            G = G * dp.PZ
        out.append(sp.Matrix(G))
    return out


def main():
    one_dim, C, H_seed, H_cross, offset = dga.build_full_scalar_gauge_action()
    C1 = C[:, :offset]
    Hs1 = H_seed[:, :offset]
    Hc1 = H_cross[:, :offset]
    M1 = C1.col_join(Hs1)
    Dm, Sm, Tm = smith_decomp(M1)
    rank = M1.rank()
    diag = [abs(int(Dm[i, i])) for i in range(min(Dm.shape)) if Dm[i, i] != 0]
    if rank != len(diag):
        raise AssertionError((rank, diag))

    seed_keys = sorted(tr.SEED_KEYS)
    P = seed_flip_matrix(seed_keys)
    seed_offset = C1.rows

    # Solvability of M1*theta = [0; seed_bits/2] mod Z.  After Smith left
    # transformation only the zero rows impose conditions; multiply by 2 and
    # reduce mod 2 to obtain linear constraints on the 24 seed-flip bits.
    Z = Sm[rank:, seed_offset:seed_offset + len(seed_keys)]
    Q = Z * P
    constraint_rows = []
    for i in range(Q.rows):
        bits = 0
        for j in range(Q.cols):
            if int(Q[i, j]) & 1:
                bits |= 1 << j
        if bits:
            constraint_rows.append(bits)
    normalizer_basis, pivots = gf2_rref_nullspace(constraint_rows, 16)
    print({
        "scalar_plus_seed_rank": rank,
        "scalar_plus_seed_smith_nonzero": diag,
        "Pauli_projective_parameters_F2": 16,
        "Pauli_compensation_constraint_rank_F2": len(pivots),
        "allowed_Pauli_normalizer_dimension_F2": len(normalizer_basis),
        "allowed_Pauli_normalizer_generators": normalizer_basis,
    }, flush=True)

    # A canonical rational right inverse for the scalar compensation.
    invdiag = sp.diag(*[sp.Rational(1, abs(int(Dm[i, i]))) for i in range(rank)])
    Rtheta = Tm[:, :rank] * invdiag * Sm[:rank, seed_offset:seed_offset + len(seed_keys)] * sp.Rational(1, 2)

    # Uniform cross-D exponent matrix and its two component characters.
    ratios0, *_ = da.collect_ratio_constraints(5, 0)
    rows0 = aga.exponent_rows(ratios0)
    A, diagA, torsionA = aga.smith_profile(rows0)
    if diagA[-2:] != [2, 2] or torsionA != [2, 2]:
        raise AssertionError((diagA, torsionA))
    W = cross_component_characters(A)

    # Existing disconnected scalar residual gauge contributes one component
    # direction.  Extract its exact label from Smith(M1).
    scalar_labels = []
    for pos in range(min(Dm.shape)):
        d = abs(int(Dm[pos, pos])) if Dm[pos, pos] != 0 else 0
        if d <= 1:
            continue
        v = Tm[:, pos]
        phase = W * Hc1 * v / d
        scalar_labels.append(label_bits_from_phase(phase))
    scalar_rank = gf2_rank(scalar_labels)
    if scalar_rank != 1:
        raise AssertionError(("expected one disconnected scalar cross-D direction", scalar_labels, scalar_rank))

    endpoint = {key: aga.multiplicity_two_endpoints(key) for key in tr.CROSS_KEYS}
    branch_results = []

    for cid in da.FRONTIER_COMPONENTS:
        for mask in da.SURVIVOR_MASKS:
            shapes, err = tr.projective_shapes(cid, mask)
            if err is not None or set(shapes) != set(tr.CROSS_KEYS):
                raise AssertionError(("projective shape failure", cid, mask, err, len(shapes)))

            generator_labels = []
            for qbits in normalizer_basis:
                q = sp.Matrix([(qbits >> j) & 1 for j in range(16)])
                seed = (P * q).applyfunc(lambda x: int(x) & 1)
                theta = Rtheta * seed
                rhs = sp.zeros(M1.rows, 1)
                for i in range(len(seed_keys)):
                    rhs[seed_offset + i, 0] = sp.Rational(int(seed[i]), 2)
                residue = M1 * theta - rhs
                if any(not mod1(x) == 0 for x in residue):
                    raise AssertionError(("scalar compensation does not solve seed flips", qbits, residue))

                G = pauli_gauges(qbits)
                alpha_phase = []
                for key in tr.CROSS_KEYS:
                    source, target = endpoint[key]
                    T0 = shapes[key]
                    transformed = G[tr.SPACE_INDEX[target]].inv() * T0 * G[tr.SPACE_INDEX[source]]
                    alpha = proportionality(transformed, T0)
                    alpha_phase.append(sp.Rational(root_phase4(alpha), 4))
                alpha_phase = sp.Matrix(alpha_phase)
                scalar_cross_phase = Hc1 * theta
                total_phase = scalar_cross_phase + alpha_phase

                # The transformed amplitude ratio must satisfy the homogeneous
                # 168-equation D system exactly as a root-of-unity phase point.
                check = A * total_phase
                if any(mod1(x) != 0 for x in check):
                    raise AssertionError(("Pauli-normalizer gauge violates cross-D equations", cid, mask, qbits))

                label = label_bits_from_phase(W * total_phase)
                generator_labels.append(label)

            total_rank = gf2_rank(scalar_labels + generator_labels)
            row = {
                "component": cid,
                "mask": mask,
                "scalar_disconnected_labels": scalar_labels,
                "Pauli_normalizer_generator_labels": generator_labels,
                "component_group_rank_after_full_normalizer": total_rank,
                "cross_D_component_group_rank": 2,
                "single_witness_complete_mod_gauge": total_rank == 2,
            }
            print(row, flush=True)
            if total_rank != 2:
                raise AssertionError(("one genuine cross-D Z2 remains", row))
            branch_results.append((cid, mask))

    if len(branch_results) != 16:
        raise AssertionError(branch_results)
    print({"complete_branches": branch_results, "total": len(branch_results)}, flush=True)
    print(
        "RESULT: scalar disconnected gauge plus Pauli projective normalizer acts transitively on the cross-D Z2 x Z2 components; one D-amplitude witness per chirality is exhaustive modulo full gauge",
        flush=True,
    )


if __name__ == "__main__":
    main()
