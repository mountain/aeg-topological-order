"""Exact D-amplitude closure for the fresh epsilon=-1 R(2,2) survivors.

Phase 1 leaves four orbit-constant chirality masks per deep-frontier scalar
component: 0, 105, 150, 255.  This script turns their binomial D-pentagon
constraints into a finite root-of-unity congruence problem, asks Z3 only for a
witness, and then certifies that witness by direct characteristic-zero
substitution into the original multiplicity-aware pentagon engine.

The solver is therefore a discovery device, not the proof certificate.  The
certificate is the explicit root-of-unity amplitude vector plus the replay in
which every D-layer matrix entry vanishes exactly.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

import sympy as sp
from z3 import Int, Solver, Sum, sat

import r22_epsminus_d_trace as tr


SURVIVOR_MASKS = (0, 105, 150, 255)
FRONTIER_COMPONENTS = (5, 7, 13, 15)
ZETA8 = (sp.Integer(1) + sp.I) / sp.sqrt(2)
ROOT8 = tuple(sp.simplify(ZETA8 ** k) for k in range(8))


def collect_ratio_constraints(cid: int, mask: int):
    """Return the complete unique binomial amplitude-ratio constraints.

    A constraint `(d, ratio)` means

        prod_j t_j**d_j = ratio.

    Structural or direct phase conflicts are returned as errors; Phase-1
    survivors should have neither.
    """
    scalar = tr.scalar_assignment(cid)
    chir = tr.chirality_assignment(mask)
    seeds = tr.seed_assignment_from_chirality(chir)
    shapes, err = tr.projective_shapes(cid, mask)
    if err is not None:
        raise RuntimeError(("projective failure on Phase-1 survivor", cid, mask, err))

    ddata = dict(seeds)
    for key, T in shapes.items():
        ddata[key] = tr.TVARS[tr.T_INDEX[key]] * T

    ratios = {}
    source = {}
    nonzero_entries = 0
    for p, registry, diff in tr.FULL_D_CASES:
        sub, unknown = tr.registry_sub(registry, scalar, ddata)
        assert not unknown
        value = diff.applyfunc(lambda e: e.xreplace(sub))
        for i in range(value.rows):
            for j in range(value.cols):
                expr = sp.expand(value[i, j])
                if expr == 0:
                    continue
                nonzero_entries += 1
                comb = defaultdict(lambda: sp.Integer(0))
                for term in sp.Add.make_args(expr):
                    e, c = tr.term_signature(term)
                    comb[e] += c
                terms = []
                for e, c in comb.items():
                    c = sp.cancel(c)
                    if c != 0:
                        terms.append((e, c))
                if not terms:
                    continue
                if len(terms) == 1:
                    raise RuntimeError(("unexpected structural failure", cid, mask, p[:5], (i, j), terms[0]))
                if len(terms) != 2:
                    raise RuntimeError(("unexpected nonbinomial residual", cid, mask, p[:5], (i, j), expr))
                (e1, c1), (e2, c2) = terms
                key, ratio = tr.normalize_ratio(e1, c1, e2, c2)
                if not key:
                    raise RuntimeError(("degenerate ratio key", cid, mask, p[:5], (i, j)))
                ratio = sp.cancel(ratio)
                if key in ratios and sp.cancel(ratios[key] - ratio) != 0:
                    raise RuntimeError(("unexpected phase conflict", cid, mask, key, ratios[key], ratio, source[key], (p[:5], (i, j))))
                ratios[key] = ratio
                source.setdefault(key, (p[:5], (i, j)))

    assert len(ratios) == 168, (cid, mask, len(ratios))
    return ratios, source, shapes, seeds, nonzero_entries


def root8_exponent(x) -> int:
    x = sp.simplify(x)
    for k, r in enumerate(ROOT8):
        if sp.simplify(x - r) == 0:
            return k
    raise RuntimeError(("ratio is not an eighth root of unity", x))


def solve_root_amplitudes(ratios, require_mu4: bool):
    u = [Int(f"u{i}") for i in range(48)]
    s = Solver()
    for x in u:
        s.add(x >= 0, x < 8)
        if require_mu4:
            s.add(x % 2 == 0)

    phase_profile = Counter()
    for key, ratio in ratios.items():
        rhs = root8_exponent(ratio)
        phase_profile[rhs] += 1
        terms = [power * u[i] for i, power in key]
        lhs = Sum(terms) if terms else 0
        s.add((lhs - rhs) % 8 == 0)

    if s.check() != sat:
        return None, phase_profile
    m = s.model()
    sol = [m.eval(x).as_long() % 8 for x in u]
    return sol, phase_profile


def amplitude_value(k: int):
    k %= 8
    if k == 0:
        return sp.Integer(1)
    if k == 2:
        return sp.I
    if k == 4:
        return sp.Integer(-1)
    if k == 6:
        return -sp.I
    return ROOT8[k]


def verify_characteristic_zero(cid: int, mask: int, exponents, shapes, seeds):
    scalar = tr.scalar_assignment(cid)
    ddata = dict(seeds)
    for key, T in shapes.items():
        amp = amplitude_value(exponents[tr.T_INDEX[key]])
        ddata[key] = amp * T

    checked = 0
    failures = []
    for p, registry, diff in tr.FULL_D_CASES:
        sub, unknown = tr.registry_sub(registry, scalar, ddata)
        assert not unknown
        value = diff.applyfunc(lambda e: sp.simplify(e.xreplace(sub)))
        checked += value.rows * value.cols
        for i in range(value.rows):
            for j in range(value.cols):
                if value[i, j] != 0:
                    failures.append((p[:5], (i, j), sp.simplify(value[i, j])))
                    if len(failures) >= 5:
                        return checked, failures
    return checked, failures


def solve_branch(cid: int, mask: int):
    ratios, _source, shapes, seeds, nonzero_entries = collect_ratio_constraints(cid, mask)

    exponents, phase_profile = solve_root_amplitudes(ratios, require_mu4=True)
    group = "mu4"
    if exponents is None:
        exponents, phase_profile = solve_root_amplitudes(ratios, require_mu4=False)
        group = "mu8"
    if exponents is None:
        raise RuntimeError(("no mu8 amplitude solution", cid, mask))

    checked, failures = verify_characteristic_zero(cid, mask, exponents, shapes, seeds)
    if failures:
        raise RuntimeError(("characteristic-zero replay failed", cid, mask, failures))

    amp_profile = Counter(str(sp.simplify(amplitude_value(k))) for k in exponents)
    result = {
        "component": cid,
        "mask": mask,
        "root_group": group,
        "amplitude_profile": dict(sorted(amp_profile.items())),
        "constraint_phase_profile": dict(sorted(phase_profile.items())),
        "ratio_constraints": len(ratios),
        "symbolic_nonzero_entries_before_amplitude": nonzero_entries,
        "verified_matrix_entries": checked,
    }
    print(result, flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, action="append")
    ap.add_argument("--mask", type=int, action="append")
    args = ap.parse_args()

    components = tuple(args.component) if args.component else FRONTIER_COMPONENTS
    masks = tuple(args.mask) if args.mask else SURVIVOR_MASKS
    for cid in components:
        if cid not in FRONTIER_COMPONENTS:
            raise SystemExit(f"component {cid} is not in fresh deep frontier {FRONTIER_COMPONENTS}")
        for mask in masks:
            if mask not in SURVIVOR_MASKS:
                raise SystemExit(f"mask {mask} is not a Phase-1 survivor")
            solve_branch(cid, mask)

    print("RESULT: every requested Phase-1 survivor has an explicit exact D-amplitude closure", flush=True)


if __name__ == "__main__":
    main()
