"""Audit whether disconnected residual trivalent gauge removes D-amplitude Z2^2.

The cross-D amplitude lattice has a uniform homogeneous solution group

    (C*)^6 x Z2 x Z2

for every deep scalar/chirality survivor.  The connected six-dimensional part
is already exactly the scalar-center gauge on the eight multiplicity-two
fusion spaces.  This script asks whether the remaining four connected
components are also gauge-equivalent once the *full scalar trivalent gauge
stabilizer* of the canonical A/B/C representative and exact Pauli seed slice is
included.

Gauge variables:

* one C* scalar for each of the 29 multiplicity-one non-unit fusion vertices;
* the scalar center of GL2 for each of the eight multiplicity-two spaces.

For every D F-block, the scalar gauge exponent is reconstructed directly from
its unique source and target fusion paths using the standard F-symbol basis
change: source vertex factors with exponent +1, target factors with exponent
-1.

Let C be the scalar A/B/C gauge exponent matrix, H_seed the 24 seed-D gauge
rows, and H_cross the 48 cross-D rows.  The residual gauge group preserving the
chosen scalar representative and the *exact* Pauli seed matrices is

    K = ker M,   M = [ C ; H_seed ].

K can be disconnected.  Smith decomposition of M provides explicit
root-of-unity representatives for its component group.  We map those
representatives through H_cross and measure their images modulo the connected
six-dimensional cross-D gauge torus.  If their F2 images span two additional
directions, they act transitively on the previously observed Z2^2 amplitude
components and the single downstream D witness is theorem-complete.
"""
from __future__ import annotations

import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

import r22_scalar_audit as sa
import r22_epsminus_d_amplitude as da
import r22_epsminus_d_trace as tr
import r22_epsminus_d_amplitude_gauge_audit as aga
from r22_scale_audit import N, OBJECTS, ONE


def d_path_triples(key):
    """Return the two source and two target trivalent vertices of a D block.

    Every D block in this problem has one admissible intermediate object on
    each side, with total multiplicity two coming from exactly one 2D fusion
    vertex.  This is asserted rather than assumed.
    """
    a, b, c, d = key
    source = []
    target = []
    for e in OBJECTS:
        n1, n2 = N(a, b, e), N(e, c, d)
        if n1 and n2:
            source.append((e, n1, n2, ((a, b, e), (e, c, d))))
    for f in OBJECTS:
        n1, n2 = N(b, c, f), N(a, f, d)
        if n1 and n2:
            target.append((f, n1, n2, ((b, c, f), (a, f, d))))
    if len(source) != 1 or source[0][1] * source[0][2] != 2:
        raise AssertionError(("unexpected D source paths", key, source))
    if len(target) != 1 or target[0][1] * target[0][2] != 2:
        raise AssertionError(("unexpected D target paths", key, target))
    return source[0][3], target[0][3]


def build_full_scalar_gauge_action():
    scalar_keys, _idx, _A, _examples = sa.build_scalar_system()
    one_dim_triples, C1 = sa.build_scalar_gauge(scalar_keys)
    one_idx = {t: i for i, t in enumerate(one_dim_triples)}
    offset = len(one_dim_triples)
    nvars = offset + len(tr.SPACES)

    C = sp.zeros(C1.rows, nvars)
    C[:, :offset] = C1

    def gauge_col(t):
        a, b, c = t
        if a == ONE or b == ONE:
            return None  # strict-unit gauge is fixed
        mult = N(a, b, c)
        if mult == 1:
            if t not in one_idx:
                raise AssertionError(("missing multiplicity-one gauge vertex", t))
            return one_idx[t]
        if mult == 2:
            if t not in tr.SPACE_INDEX:
                raise AssertionError(("unexpected multiplicity-two gauge vertex", t))
            return offset + tr.SPACE_INDEX[t]
        raise AssertionError(("invalid fusion vertex in D gauge action", t, mult))

    D_KEYS = sorted(tr.SEED_KEYS | set(tr.CROSS_KEYS))
    H = sp.zeros(len(D_KEYS), nvars)
    didx = {k: i for i, k in enumerate(D_KEYS)}
    for key in D_KEYS:
        source, target = d_path_triples(key)
        for t, sign in [(source[0], 1), (source[1], 1), (target[0], -1), (target[1], -1)]:
            col = gauge_col(t)
            if col is not None:
                H[didx[key], col] += sign

    seed_rows = [didx[k] for k in sorted(tr.SEED_KEYS)]
    cross_rows = [didx[k] for k in tr.CROSS_KEYS]
    H_seed = H[seed_rows, :]
    H_cross = H[cross_rows, :]

    # The last eight columns are exactly the connected endpoint-incidence
    # action already audited independently on the cross amplitudes.
    B, _components = aga.residual_gauge_matrix()
    if H_cross[:, offset:] != B:
        raise AssertionError("multiplicity-two center action disagrees with independent endpoint audit")

    return one_dim_triples, C, H_seed, H_cross, offset


def f2_rank_columns(columns, nrows):
    vecs = []
    for col in columns:
        bits = 0
        for i in range(nrows):
            if int(col[i]) & 1:
                bits |= 1 << i
        if bits:
            vecs.append(bits)
    rank = 0
    for pivot_bit in range(nrows):
        p = next((i for i in range(rank, len(vecs)) if (vecs[i] >> pivot_bit) & 1), None)
        if p is None:
            continue
        vecs[rank], vecs[p] = vecs[p], vecs[rank]
        for i in range(len(vecs)):
            if i != rank and ((vecs[i] >> pivot_bit) & 1):
                vecs[i] ^= vecs[rank]
        rank += 1
    return rank


def main():
    one_dim_triples, C, H_seed, H_cross, offset = build_full_scalar_gauge_action()
    M = C.col_join(H_seed)

    print({
        "one_dim_scalar_gauges": len(one_dim_triples),
        "multiplicity_two_center_gauges": len(tr.SPACES),
        "total_scalar_gauge_parameters": M.cols,
        "scalar_rep_constraints": C.rows,
        "exact_Pauli_seed_constraints": H_seed.rows,
        "residual_constraint_rank_Q": M.rank(),
        "residual_connected_dimension": M.cols - M.rank(),
        "cross_image_rank_from_2D_centers": H_cross[:, offset:].rank(),
    }, flush=True)

    # Smith decomposition D = S M T.  If d_i > 1, the i-th transformed
    # coordinate has a disconnected mu_{d_i} kernel component.  The original
    # gauge phase representative is column_i(T)/d_i.
    dm = DomainMatrix.from_Matrix(M).convert_to(ZZ)
    Ddm, _Sdm, Tdm = smith_normal_decomp(dm)
    D = Ddm.to_Matrix()
    T = Tdm.to_Matrix()
    diag = [
        abs(int(D[i, i]))
        for i in range(min(D.shape))
        if D[i, i] != 0
    ]
    torsion_positions = [
        (i, abs(int(D[i, i])))
        for i in range(min(D.shape))
        if D[i, i] not in (0, 1, -1)
    ]
    print({
        "residual_gauge_smith_nonzero": diag,
        "residual_gauge_component_factors": [d for _i, d in torsion_positions],
    }, flush=True)

    # Confirm the cross-D homogeneous exponent matrix is uniform across all 16
    # branches and has component group Z2^2.
    rows0 = None
    for cid in da.FRONTIER_COMPONENTS:
        for mask in da.SURVIVOR_MASKS:
            ratios, _source, _shapes, _seeds, _nonzero = da.collect_ratio_constraints(cid, mask)
            rows = aga.exponent_rows(ratios)
            if rows0 is None:
                rows0 = rows
            elif rows != rows0:
                raise AssertionError(("nonuniform cross-D exponent matrix", cid, mask))
    A, diagA, torsionA = aga.smith_profile(rows0)
    if torsionA != [2, 2] or len(diagA) != 42:
        raise AssertionError(("unexpected cross-D component group", diagA, torsionA))

    # Gauge invariance at the infinitesimal/connected level: every cross-D
    # character equation vanishes on the rational kernel of M.
    AH = A * H_cross
    if M.col_join(AH).rank() != M.rank():
        raise AssertionError("cross-D equations are not invariant under residual gauge tangent directions")

    B = H_cross[:, offset:]
    base_rank_f2 = f2_rank_columns([B[:, j] for j in range(B.cols)], B.rows)
    if base_rank_f2 != 6:
        raise AssertionError(("unexpected connected cross-gauge F2 rank", base_rank_f2))

    torsion_images = []
    mapped = []
    for pos, d in torsion_positions:
        v = T[:, pos]
        Mv = M * v
        if any(int(x) % d for x in Mv):
            raise AssertionError(("Smith torsion representative does not preserve scalar/seed slice", pos, d))
        y = H_cross * v
        if any(int(x) % d for x in A * y):
            raise AssertionError(("disconnected gauge representative violates homogeneous D equations", pos, d))

        if d != 2:
            mapped.append({"smith_position": pos, "order": d, "classification": "non-binary-unhandled"})
            continue
        bit_col = y.applyfunc(lambda x: int(x) & 1)
        torsion_images.append(bit_col)
        rank_with = f2_rank_columns(
            [B[:, j] for j in range(B.cols)] + torsion_images,
            B.rows,
        )
        mapped.append({
            "smith_position": pos,
            "order": d,
            "cross_sign_weight": sum(int(x) & 1 for x in y),
            "rank_mod_connected_after_adding": rank_with - base_rank_f2,
        })

    augmented_rank = f2_rank_columns(
        [B[:, j] for j in range(B.cols)] + torsion_images,
        B.rows,
    )
    discrete_cross_rank = augmented_rank - base_rank_f2
    print({
        "disconnected_gauge_images": mapped,
        "connected_cross_rank_F2": base_rank_f2,
        "cross_rank_after_disconnected_gauge_F2": augmented_rank,
        "new_discrete_cross_directions": discrete_cross_rank,
        "cross_D_component_rank_to_kill": 2,
    }, flush=True)

    if discrete_cross_rank != 2:
        raise AssertionError((
            "full scalar residual gauge does not remove all cross-D Z2^2 components",
            discrete_cross_rank,
            mapped,
        ))

    print(
        "RESULT: disconnected residual trivalent gauge maps surjectively onto the cross-D Z2 x Z2 component group; the single exact D witness is complete modulo gauge",
        flush=True,
    )


if __name__ == "__main__":
    main()
