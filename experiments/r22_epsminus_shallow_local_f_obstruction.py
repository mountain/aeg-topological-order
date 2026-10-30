"""Fresh local-F obstruction for the shallow epsilon-minus R(2,2) components.

This theorem-audit verifier reconstructs the independent obstruction that was
recorded historically but not promoted with an executable certificate into the
canonical main branch.

It uses only:

* the full-C* canonical scalar A/B/C representative;
* the gauge-fixed Pauli/Clifford stabilizer seed normal form at epsilon=-1;
* the four pentagons with exactly one external stabilizer h and three X's;
* the target required associator F^{XXX}_X (10 x 10).

No cross-D amplitudes, E data, final four-noninvertible pentagons, numerical
rank test, or Groebner basis is used.

The four local pentagons read only four of the eight Clifford chirality signs.
The script discovers those spaces from provenance and exhausts all 2^4=16
local chirality patterns.  For each of canonical scalar components 4,6,12,14
it proves that the determinant polynomial of F^{XXX}_X is identically zero.

As a red-team control, the same compiler is also applied to the Phase-1 deep
survivors of components 5,7,13,15 and must *not* give a zero determinant
polynomial there.  This guards against an accidentally over-constraining local
compiler.
"""
from __future__ import annotations

from collections import defaultdict

import sympy as sp

import r22_epsminus_d_trace as tr
from r22_local_associator import pentagon
from r22_scale_audit import f_class

TARGET = ("X", "X", "X", "X")
DEEP_SURVIVOR_MASKS = (0, 105, 150, 255)

# ---------------------------------------------------------------------------
# DERIVED, NOT FROZEN.
#
# The epsilon = -1 scalar components were historically split by two literal lists
#
#     SHALLOW = (4, 6, 12, 14)   <- det(F^{XXX}_X) is identically zero
#     DEEP    = (5, 7, 13, 15)   <- det(F^{XXX}_X) is not, so they survive
#
# with no stated reason.  The split is the sign of ONE scalar, exactly as eps itself
# already is (see r22_epsplus_local_f_obstruction.EPS_INDEX).  Write
#
#     chi(c) = sign of the scalar at CHI_KEY  (+1 if the bit is clear, -1 if set)
#
# Then over all 16 scalar components
#
#     det(F^{XXX}_X) identically zero   <=>   eps = +1  OR  chi = +1 ,
#
# so the epsilon = -1 half partitions as
#
#     SHALLOW = { c in eps-1 : chi(c) = +1 }      (local-F singularity)
#     DEEP    = { c in eps-1 : chi(c) = -1 }      (survives to the Phase-5 frontier)
#
# Eight distinct scalars give the identical separator; CHI_KEY is the
# lexicographically first of them.  The frozen tuples are retained below ONLY as a
# regression assertion, so that this file fails loudly if the derivation and the
# historical lists ever disagree.
# ---------------------------------------------------------------------------
from r22_epsplus_local_f_obstruction import (  # noqa: E402
    COMPONENT_REPS as _COMPONENT_REPS,
    EPS_PLUS as _EPS_PLUS,
    SC_INDEX as _SC_INDEX,
)

CHI_KEY = ("X", "X", "h", "1")
CHI_EQUIVALENT_KEYS = (
    ("X", "X", "h", "1"), ("X", "X", "h", "h"),
    ("X", "Y", "h", "g"), ("X", "Y", "h", "k"),
    ("Y", "X", "h", "g"), ("Y", "X", "h", "k"),
    ("Y", "Y", "h", "1"), ("Y", "Y", "h", "h"),
)

_FROZEN_SHALLOW = (4, 6, 12, 14)
_FROZEN_DEEP = (5, 7, 13, 15)


def chi(cid: int) -> int:
    """The controlling scalar's sign for scalar component `cid`."""
    return -1 if ((_COMPONENT_REPS[cid] >> _SC_INDEX[CHI_KEY]) & 1) else 1


def is_epsilon_plus(cid: int) -> bool:
    return cid in _EPS_PLUS


EPS_MINUS = tuple(c for c in range(len(_COMPONENT_REPS)) if c not in _EPS_PLUS)
SHALLOW = tuple(c for c in EPS_MINUS if chi(c) == 1)
DEEP = tuple(c for c in EPS_MINUS if chi(c) == -1)

assert SHALLOW == _FROZEN_SHALLOW, (SHALLOW, _FROZEN_SHALLOW)
assert DEEP == _FROZEN_DEEP, (DEEP, _FROZEN_DEEP)
assert len(_EPS_PLUS) + len(SHALLOW) + len(DEEP) == len(_COMPONENT_REPS) == 16

# the separator must not depend on which of the eight equivalent scalars is used
for _k in CHI_EQUIVALENT_KEYS:
    _sh = tuple(c for c in EPS_MINUS if not ((_COMPONENT_REPS[c] >> _SC_INDEX[_k]) & 1))
    _dp = tuple(c for c in EPS_MINUS if ((_COMPONENT_REPS[c] >> _SC_INDEX[_k]) & 1))
    assert _sh == SHALLOW and _dp == DEEP, (_k, _sh, _dp)

# All four possible positions of the single external stabilizer h.
LOCAL_EXTERNALS = (
    ("h", "X", "X", "X"),
    ("X", "h", "X", "X"),
    ("X", "X", "h", "X"),
    ("X", "X", "X", "h"),
)

FVARS = sp.symbols("u0:100")
FVAR_SET = set(FVARS)
FVAR_INDEX = {v: i for i, v in enumerate(FVARS)}


def build_local_cases():
    out = []
    read_spaces = set()
    for external in LOCAL_EXTERNALS:
        labels = dict(zip("abcd", external))
        registry, _mats, diff = pentagon(labels, "X")

        # The advertised locality is itself a theorem-interface assertion:
        # only scalar A/B/C data, stabilizer D seeds, and F^{XXX}_X may occur.
        for (meta, _sym) in registry.symbols.items():
            key, _row, _col = meta
            cl = f_class(key)
            if cl in "ABC":
                continue
            if cl == "D":
                if key not in tr.SEED_KEYS:
                    raise AssertionError(("local pentagon reads cross-D block", external, key))
                read_spaces.add(tr.underlying_h_space(key)[0])
                continue
            if cl == "F" and key == TARGET:
                continue
            raise AssertionError(("unexpected local dependency", external, key, cl))
        out.append((external, registry, diff))

    read_spaces = tuple(sorted(read_spaces))
    if len(read_spaces) != 4:
        raise AssertionError(("expected four local chirality spaces", read_spaces))
    return tuple(out), read_spaces


LOCAL_CASES, READ_SPACES = build_local_cases()


def local_mask(local_bits: int) -> int:
    """Embed one of the 2^4 locally visible chirality patterns into 8 bits."""
    mask = 0
    for j, space in enumerate(READ_SPACES):
        if (local_bits >> j) & 1:
            mask |= 1 << tr.SPACE_INDEX[space]
    return mask


def registry_sub(registry, scalar, seeds):
    sub = {}
    for (meta, sym) in registry.symbols.items():
        key, row, col = meta
        cl = f_class(key)
        if cl in "ABC":
            sub[sym] = scalar[key]
        elif cl == "D":
            if key not in seeds:
                raise AssertionError(("missing stabilizer seed", key))
            sub[sym] = seeds[key][row, col]
        elif cl == "F" and key == TARGET:
            sub[sym] = FVARS[10 * row + col]
        else:
            raise AssertionError(("unexpected local dependency during substitution", key, cl))
    return sub


def linear_row(expr):
    coeffs = defaultdict(lambda: sp.Integer(0))
    const = sp.Integer(0)
    for term in sp.Add.make_args(sp.expand(expr)):
        fs = term.free_symbols & FVAR_SET
        if not fs:
            const += term
            continue
        if len(fs) != 1:
            raise AssertionError(("nonlinear local-F term", term, fs))
        sym = next(iter(fs))
        coeff = sp.cancel(term / sym)
        if coeff.free_symbols:
            raise AssertionError(("symbolic local-F coefficient", term, coeff))
        coeffs[FVAR_INDEX[sym]] += coeff
    const = sp.cancel(const)
    if const != 0:
        raise AssertionError(("constant local obstruction before F", expr, const))
    return {i: sp.cancel(c) for i, c in coeffs.items() if sp.cancel(c) != 0}


def compile_rows(cid: int, mask: int):
    scalar = tr.scalar_assignment(cid)
    chirality = tr.chirality_assignment(mask)
    seeds = tr.seed_assignment_from_chirality(chirality)

    rows = []
    provenance = []
    for external, registry, diff in LOCAL_CASES:
        sub = registry_sub(registry, scalar, seeds)
        value = diff.applyfunc(lambda e: sp.expand(e.xreplace(sub)))
        for i in range(value.rows):
            for j in range(value.cols):
                expr = value[i, j]
                if expr == 0:
                    continue
                row = linear_row(expr)
                if not row:
                    continue
                if len(row) > 2:
                    raise AssertionError(("local-F support exceeds two", cid, mask, external, (i, j), row))
                rows.append(row)
                provenance.append((external, (i, j)))
    if not rows:
        raise AssertionError(("empty local-F system", cid, mask))
    return rows, provenance


class WeightedUF:
    """Exact homogeneous support-1/support-2 solver: x_i = w_i x_root."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.weight = [sp.Integer(1) for _ in range(n)]
        self.forced = [False] * n

    def find(self, x):
        if self.parent[x] == x:
            return x, self.weight[x]
        p = self.parent[x]
        r, wp = self.find(p)
        self.weight[x] = sp.cancel(self.weight[x] * wp)
        self.parent[x] = r
        return r, self.weight[x]

    def force(self, x):
        r, _ = self.find(x)
        self.forced[r] = True

    def relation(self, i, a, j, b):
        ri, wi = self.find(i)
        rj, wj = self.find(j)
        if ri == rj:
            if sp.cancel(a * wi + b * wj) != 0:
                self.forced[ri] = True
            return
        q = sp.cancel(-(a * wi) / (b * wj))
        fi, fj = self.forced[ri], self.forced[rj]
        self.parent[rj] = ri
        self.weight[rj] = q
        self.forced[ri] = fi or fj

    def canonicalize(self):
        for i in range(len(self.parent)):
            self.find(i)
        flags = defaultdict(bool)
        for i in range(len(self.parent)):
            r, _ = self.find(i)
            flags[r] = flags[r] or self.forced[i]
        for r, f in flags.items():
            self.forced[r] = f


def solve_rows(rows):
    uf = WeightedUF(100)
    for row in rows:
        if len(row) == 1:
            (i, _a), = row.items()
            uf.force(i)
        elif len(row) == 2:
            (i, a), (j, b) = list(row.items())
            uf.relation(i, a, j, b)
        else:
            raise AssertionError(("unsupported local row", row))
    uf.canonicalize()
    return uf


def determinant_polynomial(rows):
    """Return exact det polynomial as monomial-tuple -> Gaussian coefficient."""
    uf = solve_rows(rows)
    mat = []
    for i in range(10):
        rr = []
        for j in range(10):
            r, w = uf.find(10 * i + j)
            rr.append(None if uf.forced[r] else (r, sp.cancel(w)))
        mat.append(rr)

    dp = {0: {(): sp.Integer(1)}}
    for _i in range(10):
        nd = {}
        for mask, poly in dp.items():
            for j in range(10):
                if (mask >> j) & 1 or mat[_i][j] is None:
                    continue
                root, weight = mat[_i][j]
                sign = -1 if ((mask >> (j + 1)).bit_count() & 1) else 1
                target = nd.setdefault(mask | (1 << j), {})
                factor = sp.cancel(sign * weight)
                for mon, coeff in poly.items():
                    mm = tuple(sorted(mon + (root,)))
                    value = sp.cancel(target.get(mm, sp.Integer(0)) + factor * coeff)
                    if value != 0:
                        target[mm] = value
                    else:
                        target.pop(mm, None)
        dp = {m: p for m, p in nd.items() if p}
        if not dp:
            return {}
    return dp.get((1 << 10) - 1, {})


def audit_shallow():
    print({"local_read_spaces": READ_SPACES, "local_patterns": 1 << len(READ_SPACES)}, flush=True)
    total = 0
    for cid in SHALLOW:
        nonzero = []
        row_counts = set()
        for bits in range(1 << len(READ_SPACES)):
            mask = local_mask(bits)
            rows, _prov = compile_rows(cid, mask)
            row_counts.add(len(rows))
            det = determinant_polynomial(rows)
            total += 1
            if det:
                nonzero.append((bits, mask, len(det)))
        print({
            "component": cid,
            "local_patterns": 16,
            "row_counts": sorted(row_counts),
            "nonzero_determinant_polynomials": nonzero,
            "closed": not nonzero,
        }, flush=True)
        if nonzero:
            raise AssertionError(("shallow local-F obstruction incomplete", cid, nonzero))
    if total != 64:
        raise AssertionError(("unexpected shallow branch total", total))
    print("RESULT: components 4,6,12,14 are locally obstructed for all 64 canonical Clifford patterns", flush=True)


def audit_deep_controls():
    # These branches are known to pass the complete Phase-4 determinant gate.
    # The local compiler must therefore leave a nonzero determinant polynomial.
    for cid in DEEP:
        rows_out = []
        for mask in DEEP_SURVIVOR_MASKS:
            rows, _prov = compile_rows(cid, mask)
            det = determinant_polynomial(rows)
            rows_out.append((mask, len(rows), len(det)))
            if not det:
                raise AssertionError(("negative control became locally singular", cid, mask))
        print({"deep_control_component": cid, "branches": rows_out, "all_nonzero": True}, flush=True)
    print("CONTROL: all 16 deep Phase-1 survivors remain locally invertible under the same verifier", flush=True)


def main():
    audit_shallow()
    audit_deep_controls()


if __name__ == "__main__":
    main()
