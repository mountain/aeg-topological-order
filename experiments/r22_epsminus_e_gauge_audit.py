"""Gauge audit for the two-dimensional epsilon=-1 E solution space.

After exact D closure every deep-frontier branch has E rank 126 / nullity 2.
This script checks whether that entire E freedom is the residual scalar gauge
left by the irreducible Clifford multiplicity fibers and the connected cross-D
transport graph.

The eight multiplicity-two spaces carry irreducible Pauli triples, so their
commutant is scalar.  Cross-D transport has two connected K4 orbits.  Therefore
there are two candidate residual scalar gauge parameters.  We compute their
characters on every E entry from the standard trivalent-basis gauge formula and
compare the resulting character decomposition with the exact two-dimensional E
weighted solution space.

If the two nonzero character pieces span the E nullspace and the character
matrix has rank two, every E solution with both pieces nonzero is gauge-
equivalent.  Invertibility of the required E blocks is then a gauge-invariant
property, allowing one generic exact E representative to be used in the later
F-linear analysis.
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
    """Gauge character using source-minus-target basis exponents.

    Reversing this convention negates every character and does not affect the
    rank/transitivity conclusion.
    """
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


def flatten_edata(edata):
    v = [sp.Integer(0)] * 128
    for key in ef.E_KEYS:
        base = 4 * ef.E_INDEX[key]
        Mx = edata[key]
        v[base:base + 4] = [Mx[0, 0], Mx[0, 1], Mx[1, 0], Mx[1, 1]]
    return v


def vector_to_edata(v):
    out = {}
    for key in ef.E_KEYS:
        base = 4 * ef.E_INDEX[key]
        out[key] = sp.Matrix([[v[base], v[base + 1]], [v[base + 2], v[base + 3]]])
    return out


def solve_branch(cid, mask):
    result, pack = ef.solve_branch(cid, mask)
    if pack is None or result["status"] != "E_PASS":
        raise RuntimeError(("branch does not reach invertible E", cid, mask, result))
    scalar, ddata, edata = pack
    uf, _support, _total, _neq, _prov = ef.build_weighted_system(scalar, ddata)
    roots = uf.free_roots()
    assert len(roots) == 2, (cid, mask, roots)

    v = flatten_edata(edata)
    char_entries = defaultdict(list)
    for key in ef.E_KEYS:
        base = 4 * ef.E_INDEX[key]
        for row in range(2):
            for col in range(2):
                i = base + 2 * row + col
                if v[i] != 0:
                    char_entries[entry_character(key, row, col)].append(i)

    chars = sorted(char_entries)
    pieces = []
    for ch in chars:
        w = [sp.Integer(0)] * 128
        for i in char_entries[ch]:
            w[i] = v[i]
        pieces.append(w)

    # Every character piece must separately solve the homogeneous E system.
    piece_checks = []
    for ch, w in zip(chars, pieces):
        wedata = vector_to_edata(w)
        checked, failures = ef.verify_e(scalar, ddata, wedata)
        piece_checks.append((ch, checked, failures))
        if failures:
            raise RuntimeError(("gauge character piece does not solve E", cid, mask, ch, failures))

    # The exact weighted solution has dimension two; the character pieces must
    # therefore be exactly two independent directions.
    if len(chars) != 2:
        raise RuntimeError(("expected exactly two E gauge characters", cid, mask, chars, Counter(map(entry_character, [], []))))
    char_matrix = sp.Matrix(chars)
    char_rank = char_matrix.rank()
    if char_rank != 2:
        raise RuntimeError(("residual gauge characters not independent", cid, mask, chars, char_rank))

    # Check that every invertible required E block uses both character pieces:
    # its determinant must vanish when either piece is removed.  This makes the
    # invertible locus exactly the (C*)^2 region of the two-dimensional space.
    det_profile = Counter()
    for key in ef.E_KEYS:
        Mfull = edata[key]
        if sp.cancel(Mfull.det()) == 0:
            raise RuntimeError(("reference E point unexpectedly singular", cid, mask, key))
        for ci, w in enumerate(pieces):
            Mpiece = vector_to_edata(w)[key]
            det_profile[(ci, sp.cancel(Mpiece.det()) == 0)] += 1
    if det_profile[(0, True)] != 32 or det_profile[(1, True)] != 32:
        raise RuntimeError(("E determinant does not require both gauge pieces", cid, mask, det_profile))

    out = {
        "component": cid,
        "mask": mask,
        "E_nullity": len(roots),
        "nonzero_gauge_characters": chars,
        "character_matrix_rank": char_rank,
        "each_character_piece_solves_E": True,
        "all_32_blocks_require_both_pieces_for_invertibility": True,
        "status": "E_FREEDOM_IS_RESIDUAL_GAUGE",
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
    print("RESULT: all requested E invertible loci are single residual-gauge orbits", flush=True)


if __name__ == "__main__":
    main()
