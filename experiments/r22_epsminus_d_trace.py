"""Fresh canonical epsilon=-1 D chirality trace for R(2,2).

Purpose
-------
Rebuild the finite Clifford branch localization from the original multiplicity-
aware pentagon engine, using the full-C* scalar canonical representatives.
This script does not inherit the superseded D-amplitude verdict in note 15.

For a chosen canonical epsilon=-1 scalar component and each of the 2^8 local
chirality masks it:

1. installs the Pauli/Clifford stabilizer seeds;
2. solves the 48 cross-D projective intertwiner shapes exactly;
3. substitutes one nonzero amplitude t_j per projective D block into every
   complete D-layer pentagon;
4. classifies immediate one-monomial contradictions;
5. otherwise detects exact phase conflicts in which the same amplitude
   monomial ratio is required to take two different values.

The intended fresh trace is 256 -> 64 -> 4, but the script treats that as an
assertion to be replayed rather than an input assumption.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import product

import sympy as sp

from r22_d_layer_probe import d_block_set
from r22_epsminus_d_probe import PX, PY, PZ, underlying_h_space
from r22_epsplus_local_f_obstruction import COMPONENT_REPS, SC_INDEX, SC_KEYS
from r22_local_associator import pentagon
from r22_scale_audit import M, ONE, f_class, layer_spec, pentagon_blocks, pentagon_deps


SPACES = list(product(M, repeat=3))
SPACE_INDEX = {s: i for i, s in enumerate(SPACES)}
DSET = d_block_set()
SEED_KEYS = {k for k in DSET if "h" in k[:3]}
CROSS_KEYS = sorted(DSET - SEED_KEYS)
assert len(SEED_KEYS) == 24 and len(CROSS_KEYS) == 48
T_INDEX = {k: i for i, k in enumerate(CROSS_KEYS)}
TVARS = sp.symbols("t0:48", nonzero=True)

EPS_INDEX = SC_INDEX[("h", "X", "h", "X")]
EPS_MINUS = [i for i, r in enumerate(COMPONENT_REPS) if ((r >> EPS_INDEX) & 1) == 1]
assert EPS_MINUS == [4, 5, 6, 7, 12, 13, 14, 15]


def scalar_assignment(cid: int):
    bits = COMPONENT_REPS[cid]
    return {k: (-1 if ((bits >> SC_INDEX[k]) & 1) else 1) for k in SC_KEYS}


def chirality_assignment(mask: int):
    return {s: (-1 if ((mask >> SPACE_INDEX[s]) & 1) else 1) for s in SPACES}


def seed_assignment(mask: int):
    chir = chirality_assignment(mask)
    out = {}
    for key in SEED_KEYS:
        space, pos = underlying_h_space(key)
        out[key] = {"L": PX, "M": PZ, "R": chir[space] * PY}[pos]
    return out


def build_projective_cases():
    by = defaultdict(list)
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("D", p):
            continue
        deps = pentagon_deps(*p[:5]) & DSET
        rem = deps - SEED_KEYS
        if len(rem) != 1:
            continue
        target = next(iter(rem))
        registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
        by[target].append((p, registry, diff))
    assert set(by) == set(CROSS_KEYS)
    return by


def build_full_d_cases():
    out = []
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("D", p):
            continue
        registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
        out.append((p, registry, diff))
    return out


PROJECTIVE_CASES = build_projective_cases()
FULL_D_CASES = build_full_d_cases()


def registry_sub(registry, scalar, ddata, leave=None):
    sub = {}
    unknown = []
    for (meta, sym) in registry.symbols.items():
        key, row, col = meta
        cl = f_class(key)
        if cl in "ABC":
            sub[sym] = scalar[key]
        elif cl == "D":
            if key in ddata:
                sub[sym] = ddata[key][row, col]
            elif key == leave:
                unknown.append((sym, row, col))
            else:
                raise RuntimeError(("unknown D block", key, leave))
        else:
            raise RuntimeError(("unexpected layer", key, cl))
    return sub, unknown


def projective_shapes(cid: int, mask: int):
    scalar = scalar_assignment(cid)
    seeds = seed_assignment(mask)
    shapes = {}
    for target in CROSS_KEYS:
        equations = []
        pos = {}
        syms = set()
        for _p, registry, diff in PROJECTIVE_CASES[target]:
            sub, unknown = registry_sub(registry, scalar, seeds, leave=target)
            for sym, r, c in unknown:
                syms.add(sym)
                pos[sym] = (r, c)
            value = diff.subs(sub)
            equations.extend(sp.expand(e) for e in value if e != 0)
        syms = sorted(syms, key=str)
        if len(syms) != 4:
            return None, ("projective_symbol_count", target, len(syms))
        A, b = sp.linear_eq_to_matrix(equations, syms)
        if b != sp.zeros(len(equations), 1):
            return None, ("projective_inhomogeneous", target)
        ns = A.nullspace()
        if len(ns) != 1:
            return None, ("projective_nullity", target, len(ns))
        v = ns[0]
        first = next((x for x in v if x != 0), None)
        if first is None:
            return None, ("projective_zero", target)
        v = sp.simplify(v / first)
        T = sp.zeros(2)
        for sym, val in zip(syms, v):
            T[pos[sym]] = sp.simplify(val)
        if sp.simplify(T.det()) == 0:
            return None, ("projective_singular", target, T)
        shapes[target] = T
    return shapes, None


def term_signature(term):
    pd = term.as_powers_dict()
    exp = [0] * 48
    coeff = term
    for i, t in enumerate(TVARS):
        p = pd.get(t, 0)
        if p:
            if not p.is_Integer:
                raise RuntimeError(("noninteger amplitude power", term, t, p))
            p = int(p)
            exp[i] = p
            coeff /= t ** p
    coeff = sp.simplify(coeff)
    if coeff.free_symbols:
        raise RuntimeError(("unexpected free symbols", coeff.free_symbols, term))
    return tuple(exp), coeff


def normalize_ratio(e1, c1, e2, c2):
    # c1*m1 + c2*m2 = 0  =>  m1/m2 = -c2/c1.
    d = tuple(a - b for a, b in zip(e1, e2))
    ratio = sp.simplify(-c2 / c1)
    first = next((x for x in d if x), 0)
    if first < 0:
        d = tuple(-x for x in d)
        ratio = sp.simplify(1 / ratio)
    return d, ratio


def classify_mask(cid: int, mask: int):
    scalar = scalar_assignment(cid)
    seeds = seed_assignment(mask)
    shapes, err = projective_shapes(cid, mask)
    if err is not None:
        return "projective", {"error": repr(err)}

    ddata = dict(seeds)
    for key, T in shapes.items():
        ddata[key] = TVARS[T_INDEX[key]] * T

    ratios = {}
    checked_entries = 0
    for p, registry, diff in FULL_D_CASES:
        sub, unknown = registry_sub(registry, scalar, ddata)
        assert not unknown
        value = diff.subs(sub)
        for i in range(value.rows):
            for j in range(value.cols):
                expr = sp.expand(value[i, j])
                if expr == 0:
                    continue
                checked_entries += 1
                terms = [term_signature(t) for t in sp.Add.make_args(expr)]
                # Combine identical amplitude monomials exactly.
                comb = defaultdict(lambda: sp.Integer(0))
                for e, c in terms:
                    comb[e] = sp.simplify(comb[e] + c)
                terms = [(e, sp.simplify(c)) for e, c in comb.items() if sp.simplify(c) != 0]
                if not terms:
                    continue
                if len(terms) == 1:
                    e, c = terms[0]
                    return "structural", {
                        "pentagon": p[:5], "entry": (i, j),
                        "monomial": e, "coefficient": str(c),
                        "checked_entries": checked_entries,
                    }
                if len(terms) != 2:
                    return "nonbinomial", {
                        "pentagon": p[:5], "entry": (i, j),
                        "support": len(terms), "expr": str(expr),
                    }
                (e1, c1), (e2, c2) = terms
                key, ratio = normalize_ratio(e1, c1, e2, c2)
                if key in ratios and sp.simplify(ratios[key][0] - ratio) != 0:
                    prev_ratio, prev_meta = ratios[key]
                    return "phase", {
                        "pentagon": p[:5], "entry": (i, j),
                        "ratio_key": key,
                        "ratio": str(ratio), "previous_ratio": str(prev_ratio),
                        "previous": prev_meta,
                        "checked_entries": checked_entries,
                    }
                ratios[key] = (ratio, (p[:5], (i, j)))
    return "survivor", {"ratio_constraints": len(ratios), "checked_entries": checked_entries}


def run_component(cid: int, start: int = 0, stop: int = 256):
    counts = Counter()
    survivors = []
    examples = {}
    for mask in range(start, stop):
        stage, meta = classify_mask(cid, mask)
        counts[stage] += 1
        if stage == "survivor":
            survivors.append(mask)
        examples.setdefault(stage, (mask, meta))
        if (mask + 1) % 32 == 0:
            print("progress", cid, mask + 1, dict(counts), "survivors", survivors)
    print("component", cid, "counts", dict(counts))
    print("component", cid, "survivors", survivors)
    for k, v in examples.items():
        print("example", k, v)
    return counts, survivors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, default=13)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=256)
    ap.add_argument("--assert-trace", action="store_true")
    args = ap.parse_args()
    if args.component not in EPS_MINUS:
        raise SystemExit(f"component must be one of {EPS_MINUS}")
    counts, survivors = run_component(args.component, args.start, args.stop)
    if args.assert_trace and args.start == 0 and args.stop == 256:
        assert counts == Counter({"structural": 192, "phase": 60, "survivor": 4}), counts
        assert survivors == [0, 105, 150, 255], survivors
        print("RESULT: fresh exact D trace is 256 -> 64 -> 4")


if __name__ == "__main__":
    main()
