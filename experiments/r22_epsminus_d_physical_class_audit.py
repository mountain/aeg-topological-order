"""Theorem-level audit of the physical cross-D amplitude component quotient.

Historical exploratory scripts tested the stronger hypothesis that disconnected
scalar gauge plus the projective Pauli normalizer kills both Smith Z2 factors.
That hypothesis is false and its failure exposed the second physical D sheet.

This final verifier states the accepted theorem boundary positively:

* H_D = (C*)^6 x Z2 x Z2 for the common 168 x 48 cross-D system;
* connected endpoint gauge is exactly the six-dimensional identity component;
* disconnected scalar gauge contributes exactly one nonzero component label;
* every allowed projective Pauli-normalizer transformation contributes no new
  component direction beyond that same scalar-gauge label;
* hence the full residual gauge image has F2 rank one inside Z2^2, leaving
  exactly one physical Z2 and therefore exactly two physical D classes;
* the common Smith torsion sign selected by r22_epsminus_d_torsion_branch is
  outside the gauge image.

All calculations are exact over integer Smith data and root-of-unity phases.
"""
from __future__ import annotations

import sympy as sp

import r22_epsminus_d_amplitude as da
import r22_epsminus_d_amplitude_gauge_audit as aga
import r22_epsminus_d_discrete_gauge_audit as dga
import r22_epsminus_d_pauli_normalizer_audit as pn
import r22_epsminus_d_probe as dp
import r22_epsminus_d_torsion_branch as tb
import r22_epsminus_d_trace as tr


def main():
    # Common homogeneous cross-D character lattice.
    ratios0, *_ = da.collect_ratio_constraints(5, 0)
    rows0 = aga.exponent_rows(ratios0)
    A, diagA, torsionA = aga.smith_profile(rows0)
    if A.rank() != 42 or diagA != [1] * 40 + [2, 2] or torsionA != [2, 2]:
        raise AssertionError(("unexpected cross-D Smith profile", A.rank(), diagA, torsionA))

    B, components = aga.residual_gauge_matrix()
    if B.rank() != 6 or A * B != sp.zeros(A.rows, B.cols):
        raise AssertionError(("connected endpoint gauge mismatch", B.rank(), components))
    if 48 - A.rank() != B.rank():
        raise AssertionError("connected gauge does not exhaust H_D identity component")

    # Scalar gauge preserving the canonical A/B/C representative and exact
    # Pauli seed slice.  Work with the multiplicity-one columns exactly as in
    # the projective-normalizer audit; multiplicity-two centers are the already
    # separated connected endpoint gauge B.
    _one_dim, C, H_seed, H_cross, offset = dga.build_full_scalar_gauge_action()
    C1 = C[:, :offset]
    Hs1 = H_seed[:, :offset]
    Hc1 = H_cross[:, :offset]
    M1 = C1.col_join(Hs1)
    Dm, Sm, Tm = pn.smith_decomp(M1)
    rank = M1.rank()
    diag = [abs(int(Dm[i, i])) for i in range(min(Dm.shape)) if Dm[i, i] != 0]
    if rank != len(diag):
        raise AssertionError(("scalar+seed Smith mismatch", rank, diag))

    W = pn.cross_component_characters(A)

    scalar_labels = []
    for pos in range(min(Dm.shape)):
        d = abs(int(Dm[pos, pos])) if Dm[pos, pos] != 0 else 0
        if d <= 1:
            continue
        v = Tm[:, pos]
        phase = W * Hc1 * v / d
        label = pn.label_bits_from_phase(phase)
        if label:
            scalar_labels.append(label)
    scalar_labels = sorted(set(scalar_labels))
    scalar_rank = pn.gf2_rank(scalar_labels)
    if scalar_rank != 1:
        raise AssertionError(("expected exactly one scalar disconnected D-component direction", scalar_labels))

    # Allowed projective Pauli normalizer modulo scalar center.  A Pauli basis
    # change is allowed only if multiplicity-one scalar gauge compensates its
    # seed sign flips while keeping the scalar representative fixed.
    seed_keys = sorted(tr.SEED_KEYS)
    P = pn.seed_flip_matrix(seed_keys)
    seed_offset = C1.rows
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
    normalizer_basis, pivots = pn.gf2_rref_nullspace(constraint_rows, 16)

    invdiag = sp.diag(*[sp.Rational(1, abs(int(Dm[i, i]))) for i in range(rank)])
    Rtheta = Tm[:, :rank] * invdiag * Sm[:rank, seed_offset:seed_offset + len(seed_keys)] * sp.Rational(1, 2)
    endpoint = {key: aga.multiplicity_two_endpoints(key) for key in tr.CROSS_KEYS}

    branch_rows = []
    for cid in da.FRONTIER_COMPONENTS:
        for mask in da.SURVIVOR_MASKS:
            shapes, err = tr.projective_shapes(cid, mask)
            if err is not None or set(shapes) != set(tr.CROSS_KEYS):
                raise AssertionError(("projective shape failure", cid, mask, err))

            generator_labels = []
            for qbits in normalizer_basis:
                q = sp.Matrix([(qbits >> j) & 1 for j in range(16)])
                seed = (P * q).applyfunc(lambda x: int(x) & 1)
                theta = Rtheta * seed

                rhs = sp.zeros(M1.rows, 1)
                for i in range(len(seed_keys)):
                    rhs[seed_offset + i, 0] = sp.Rational(int(seed[i]), 2)
                residue = M1 * theta - rhs
                if any(pn.mod1(x) != 0 for x in residue):
                    raise AssertionError(("scalar compensation failed", cid, mask, qbits))

                G = pn.pauli_gauges(qbits)
                alpha_phase = []
                for key in tr.CROSS_KEYS:
                    source, target = endpoint[key]
                    T0 = shapes[key]
                    transformed = G[tr.SPACE_INDEX[target]].inv() * T0 * G[tr.SPACE_INDEX[source]]
                    alpha = pn.proportionality(transformed, T0)
                    alpha_phase.append(sp.Rational(pn.root_phase4(alpha), 4))
                total_phase = Hc1 * theta + sp.Matrix(alpha_phase)
                if any(pn.mod1(x) != 0 for x in A * total_phase):
                    raise AssertionError(("Pauli normalizer violates cross-D equations", cid, mask, qbits))
                generator_labels.append(pn.label_bits_from_phase(W * total_phase))

            total_rank = pn.gf2_rank(scalar_labels + generator_labels)
            # This is the corrected theorem-level condition: Pauli normalizer
            # contributes no independent second component direction.
            if total_rank != 1:
                raise AssertionError(("unexpected gauge image rank in Z2^2", cid, mask, scalar_labels, generator_labels, total_rank))
            row = {
                "component": cid,
                "mask": mask,
                "scalar_disconnected_labels": scalar_labels,
                "Pauli_normalizer_labels": generator_labels,
                "gauge_component_image_rank_F2": total_rank,
                "cross_D_component_rank_F2": 2,
                "physical_component_rank_F2": 1,
                "physical_D_classes": 2,
            }
            print(row, flush=True)
            branch_rows.append(row)

    if len(branch_rows) != 16:
        raise AssertionError(("unexpected deep chirality count", len(branch_rows)))

    torsion = tb.common_torsion_data()
    if torsion["selected_label"] in (0, torsion["scalar_gauge_label"]):
        raise AssertionError(("selected second-sheet torsion is gauge", torsion))
    if torsion["selected_sign_weight"] != 8:
        raise AssertionError(("unexpected common torsion sign weight", torsion["selected_sign_weight"]))

    print({
        "cross_D_rank_Q": A.rank(),
        "cross_D_smith_nonzero": diagA,
        "connected_solution_dimension": 48 - A.rank(),
        "connected_endpoint_gauge_rank": B.rank(),
        "scalar_disconnected_component_labels": scalar_labels,
        "allowed_Pauli_normalizer_dimension_F2": len(normalizer_basis),
        "Pauli_compensation_constraint_rank_F2": len(pivots),
        "full_residual_gauge_component_image_rank_F2": 1,
        "cross_D_component_group_rank_F2": 2,
        "physical_component_group_rank_F2": 1,
        "physical_D_classes_per_chirality": 2,
        "second_sheet_label": torsion["selected_label"],
        "second_sheet_sign_weight": torsion["selected_sign_weight"],
    }, flush=True)
    print(
        "RESULT: the full residual gauge kills exactly one of the two cross-D Smith Z2 directions; one genuine Z2 survives, so every deep chirality survivor has exactly two physical D-amplitude classes",
        flush=True,
    )


if __name__ == "__main__":
    main()
