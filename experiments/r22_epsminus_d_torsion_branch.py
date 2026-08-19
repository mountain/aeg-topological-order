"""Construct the second gauge-inequivalent epsilon-minus D-amplitude class.

The theorem audit established, uniformly on all sixteen deep scalar/chirality
branches,

    H_D = (C*)^6 x mu_2 x mu_2

for the homogeneous cross-D amplitude solution group.  Connected endpoint
gauge removes the (C*)^6 part.  The full disconnected scalar residual gauge
maps to one rank-one subgroup of the two-bit component group, while the Pauli
projective normalizer contributes no additional allowed transformation in the
fixed canonical scalar/seed slice.  Hence exactly one Z2 survives modulo full
residual gauge.

This module constructs an explicit representative of that second physical
class directly from the integer Smith decomposition of the common 168 x 48
cross-D exponent matrix.  If D = S A T and D_kk = 2, then

    u = T e_k / 2

is a homogeneous order-two phase solution.  Modulo integral phases this is a
sign vector, so multiplying any exact inhomogeneous D witness by that sign
vector gives another exact D solution.

The selected Smith generator is also checked against the exact component
characters and against the disconnected scalar-gauge image, so it is not a
mere gauge copy of the historical witness.
"""
from __future__ import annotations

from functools import lru_cache

import sympy as sp
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

import r22_epsminus_d_amplitude as da
import r22_epsminus_d_trace as tr
import r22_epsminus_d_amplitude_gauge_audit as aga
import r22_epsminus_d_discrete_gauge_audit as dga


def smith_decomp(M):
    Ddm, Sdm, Tdm = smith_normal_decomp(DomainMatrix.from_Matrix(M).convert_to(ZZ))
    return Ddm.to_Matrix(), Sdm.to_Matrix(), Tdm.to_Matrix()


def phase_component_label(W, phase):
    """Evaluate the two Smith mu2 characters on an additive phase vector."""
    y = W * phase
    label = 0
    for i in range(y.rows):
        q = sp.Rational(y[i, 0])
        q = q - sp.floor(q)
        twice = sp.simplify(2 * q)
        if twice not in (0, 1):
            raise AssertionError(("component character is not order two", i, q))
        if twice == 1:
            label |= 1 << i
    return label


@lru_cache(maxsize=1)
def common_torsion_data():
    ratios, _src, _shapes, _seeds, _nz = da.collect_ratio_constraints(5, 0)
    rows = aga.exponent_rows(ratios)
    A = sp.Matrix(rows)
    D, _S, T = smith_decomp(A)
    positions = [i for i in range(min(D.shape)) if abs(int(D[i, i])) == 2]
    if len(positions) != 2:
        raise AssertionError(("expected two D-amplitude Smith Z2 factors", positions))

    Tinv = T.inv()
    W = sp.Matrix([[Tinv[pos, j] for j in range(Tinv.cols)] for pos in positions])

    # Each Smith torsion column gives a one-hot component character by design.
    candidates = []
    for pos in positions:
        full = T[:, pos]
        sign = sp.Matrix([int(full[j]) & 1 for j in range(full.rows)])
        if any(int(x) & 1 for x in A * sign):
            raise AssertionError(("Smith sign representative is not homogeneous", pos))
        phase = sign.applyfunc(lambda x: sp.Rational(int(x), 2))
        label = phase_component_label(W, phase)
        candidates.append((pos, sign, label))

    if sorted(label for _pos, _sign, label in candidates) != [1, 2]:
        raise AssertionError(("unexpected Smith component basis", [(p, l) for p, _s, l in candidates]))

    # Compute the disconnected scalar residual-gauge label in exactly the same
    # component coordinates.  The earlier audit found rank one; here we derive
    # it again rather than hard-code the answer.
    _one_dim, C, H_seed, H_cross, _offset = dga.build_full_scalar_gauge_action()
    M = C.col_join(H_seed)
    Dg, _Sg, Tg = smith_decomp(M)
    gauge_labels = []
    for pos in range(min(Dg.shape)):
        d = abs(int(Dg[pos, pos])) if Dg[pos, pos] != 0 else 0
        if d <= 1:
            continue
        phase = H_cross * Tg[:, pos] / d
        gauge_labels.append(phase_component_label(W, phase))
    gauge_labels = sorted(set(x for x in gauge_labels if x))
    if len(gauge_labels) != 1:
        raise AssertionError(("expected one disconnected scalar-gauge direction", gauge_labels))
    gauge_label = gauge_labels[0]

    # Pick a Smith generator outside the scalar-gauge subgroup {0,g}.
    chosen = next((x for x in candidates if x[2] not in (0, gauge_label)), None)
    if chosen is None:
        raise AssertionError(("all Smith torsion generators are scalar gauge", gauge_label, candidates))
    pos, sign, label = chosen
    other_physical_label = label

    return {
        "A": A,
        "W": W,
        "smith_positions": positions,
        "candidate_labels": [(p, lab) for p, _s, lab in candidates],
        "scalar_gauge_label": gauge_label,
        "selected_position": pos,
        "selected_sign": sign,
        "selected_label": other_physical_label,
        "selected_sign_weight": sum(int(x) for x in sign),
    }


def base_exponents(cid: int, mask: int):
    ratios, _source, shapes, seeds, _ = da.collect_ratio_constraints(cid, mask)
    exponents, _profile = da.solve_root_amplitudes(ratios, require_mu4=True)
    group = "mu4"
    if exponents is None:
        exponents, _profile = da.solve_root_amplitudes(ratios, require_mu4=False)
        group = "mu8"
    if exponents is None:
        raise RuntimeError(("base D-amplitude witness missing", cid, mask))
    return list(exponents), shapes, seeds, group


def class_exponents(cid: int, mask: int, amplitude_class: int):
    """Return exact root-of-unity exponents for physical class 0 or 1."""
    if amplitude_class not in (0, 1):
        raise ValueError(amplitude_class)
    exponents, shapes, seeds, group = base_exponents(cid, mask)
    if amplitude_class == 1:
        sign = common_torsion_data()["selected_sign"]
        exponents = [(k + 4 * int(sign[j])) % 8 for j, k in enumerate(exponents)]
    return exponents, shapes, seeds, group


def exact_d_data(cid: int, mask: int, amplitude_class: int):
    exponents, shapes, seeds, group = class_exponents(cid, mask, amplitude_class)
    checked, failures = da.verify_characteristic_zero(cid, mask, exponents, shapes, seeds)
    if failures:
        raise RuntimeError(("D torsion-class replay failed", cid, mask, amplitude_class, failures))
    scalar = tr.scalar_assignment(cid)
    ddata = dict(seeds)
    for key, T0 in shapes.items():
        ddata[key] = da.amplitude_value(exponents[tr.T_INDEX[key]]) * T0
    return scalar, ddata, group, checked, exponents


def main():
    info = common_torsion_data()
    print({
        "smith_Z2_positions": info["smith_positions"],
        "smith_component_basis_labels": info["candidate_labels"],
        "scalar_disconnected_gauge_label": info["scalar_gauge_label"],
        "selected_second_class_label": info["selected_label"],
        "selected_sign_weight": info["selected_sign_weight"],
    }, flush=True)

    passed = []
    for cid in da.FRONTIER_COMPONENTS:
        for mask in da.SURVIVOR_MASKS:
            base, _bd, group0, checked0, exp0 = exact_d_data(cid, mask, 0)
            alt, _ad, group1, checked1, exp1 = exact_d_data(cid, mask, 1)
            if base != alt:
                raise AssertionError("scalar data changed between D amplitude classes")
            delta = [(b - a) % 8 for a, b in zip(exp0, exp1)]
            if any(x not in (0, 4) for x in delta):
                raise AssertionError(("second class is not a sign twist", cid, mask, delta))
            if not any(x == 4 for x in delta):
                raise AssertionError(("second class collapsed to base witness", cid, mask))
            row = {
                "component": cid,
                "mask": mask,
                "base_root_group": group0,
                "second_root_group": group1,
                "sign_flipped_amplitudes": sum(x == 4 for x in delta),
                "base_verified_entries": checked0,
                "second_verified_entries": checked1,
                "two_exact_D_classes": True,
            }
            print(row, flush=True)
            passed.append((cid, mask))

    if len(passed) != 16:
        raise AssertionError(passed)
    print({"chirality_branches": len(passed), "physical_D_classes_each": 2, "deep_D_branches": 32}, flush=True)
    print(
        "RESULT: every deep chirality survivor has a second exact gauge-inequivalent D-amplitude class obtained by the common Smith torsion sign twist",
        flush=True,
    )


if __name__ == "__main__":
    main()
