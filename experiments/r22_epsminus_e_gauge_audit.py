"""Audit the two-dimensional epsilon=-1 E solution space.

The first hypothesis was that E nullity 2 came from scalar gauge on the two
Clifford transport K4 orbits.  A clean replay falsified that hypothesis: the
standard trivalent gauge character of every nonzero E entry is (0,0).

This file now records that negative result and freezes the structure actually
needed by Phase 4.  The exact support-two E equations split the 128 entries into
two free weighted components.  Hence every E entry is 0 or a fixed exact
coefficient times one of two parameters p,q.  Every required 2x2 determinant
is checked to be a nonzero monomial in p,q.  Therefore the E-invertible locus
is a nonempty algebraic torus obtained by excluding coordinate zero sets, but
we do NOT identify these parameters as gauge.

Consequently F coherence must be analyzed symbolically over p,q.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

import sympy as sp

import r22_epsminus_d_amplitude as da
import r22_epsminus_e_filter as ef
from r22_d_layer_probe import transport_orbits
from r22_scale_audit import M, N, OBJECTS


ORBITS = [sorted(x) for x in transport_orbits()]
ORBITS.sort(key=lambda c: sum(x == "Y" for x in c[0]) % 2)
SPACE_ORBIT = {space: oi for oi, comp in enumerate(ORBITS) for space in comp}
assert len(SPACE_ORBIT) == 8


def bases(key):
    a, b, c, d = key
    src = []
    tgt = []
    for e in OBJECTS:
        for alpha in range(N(a, b, e)):
            for beta in range(N(e, c, d)):
                src.append((e, alpha, beta))
    for f in OBJECTS:
        for mu in range(N(b, c, f)):
            for nu in range(N(a, f, d)):
                tgt.append((f, mu, nu))
    assert len(src) == len(tgt)
    return src, tgt


def mult_orbit(a, b, c):
    if N(a, b, c) != 2:
        return None
    assert a in M and b in M and c in M
    return SPACE_ORBIT[(a, b, c)]


def entry_character(key, row, col):
    """Naive scalar gauge character from multiplicity-two orbit scalings."""
    a, b, c, d = key
    src, tgt = bases(key)
    e, _alpha, _beta = src[col]
    f, _mu, _nu = tgt[row]
    char = [0, 0]
    for triple, sign in (
        ((a, b, e), +1),
        ((e, c, d), +1),
        ((b, c, f), -1),
        ((a, f, d), -1),
    ):
        oi = mult_orbit(*triple)
        if oi is not None:
            char[oi] += sign
    return tuple(char)


def monomial_signature(expr, params):
    expr = sp.factor(sp.expand(expr))
    poly = sp.Poly(expr, *params)
    terms = poly.terms()
    if len(terms) != 1:
        return None
    powers, coeff = terms[0]
    return tuple(int(x) for x in powers), sp.cancel(coeff)


def solve_branch(cid, mask):
    scalar, ddata, d_root_group = ef.exact_d_data(cid, mask)
    uf, support, _total, n_eq, _prov = ef.build_weighted_system(scalar, ddata)
    roots, params, mats, dets = ef.parametric_blocks(uf)
    if len(roots) != 2:
        raise RuntimeError(("expected E nullity two", cid, mask, roots))

    # Negative gauge check: the orbit-scalar characters all cancel on E.
    nonzero_chars = Counter()
    for key in ef.E_KEYS:
        base = 4 * ef.E_INDEX[key]
        for row in range(2):
            for col in range(2):
                r, _w = uf.find(base + 2 * row + col)
                if not uf.forced[r]:
                    nonzero_chars[entry_character(key, row, col)] += 1
    if set(nonzero_chars) != {(0, 0)}:
        raise RuntimeError(("unexpected nontrivial naive E gauge character", cid, mask, nonzero_chars))

    det_sigs = {}
    for key, det in dets.items():
        if det == 0:
            raise RuntimeError(("E determinant identically zero", cid, mask, key))
        sig = monomial_signature(det, params)
        if sig is None:
            raise RuntimeError(("E determinant is not a monomial", cid, mask, key, det))
        powers, coeff = sig
        if coeff == 0:
            raise RuntimeError(("zero E determinant coefficient", cid, mask, key))
        det_sigs[key] = (powers, coeff)

    exponent_profile = Counter(p for p, _c in det_sigs.values())
    out = {
        "component": cid,
        "mask": mask,
        "D_root_group": d_root_group,
        "E_equations": n_eq,
        "E_support": dict(support),
        "E_nullity": len(roots),
        "naive_orbit_gauge_character_profile": dict(nonzero_chars),
        "naive_orbit_gauge_explains_nullity": False,
        "determinant_monomial_exponent_profile": {str(k): v for k, v in exponent_profile.items()},
        "all_32_determinants_nonzero_monomials": True,
        "status": "E_TWO_PARAMETER_TORUS",
    }
    print(out, flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, action="append")
    ap.add_argument("--mask", type=int, action="append")
    args = ap.parse_args()
    components = tuple(args.component) if args.component else da.FRONTIER_COMPONENTS
    masks = tuple(args.mask) if args.mask else da.SURVIVOR_MASKS
    for cid in components:
        for mask in masks:
            solve_branch(cid, mask)
    print("RESULT: E nullity two is a genuine symbolic torus for Phase 4; the naive parity-orbit scalar gauge explanation is rejected", flush=True)


if __name__ == "__main__":
    main()
