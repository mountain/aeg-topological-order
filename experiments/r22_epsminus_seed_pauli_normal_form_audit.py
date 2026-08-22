"""Theorem audit of the epsilon-minus Pauli seed normal form.

Goal: prove that the 24 seed-D matrices used before the chirality census are
not a Pauli ansatz.  Starting from the original multiplicity-aware pentagons
and each canonical deep scalar component, this verifier checks that on every
2D multiplicity space the three seed endomorphisms L,M,R satisfy exactly

    L^2=M^2=R^2=I,
    LM+ML=LR+RL=MR+RM=0.

It also checks that the 24 singleton plus 24 pair pentagons exhaust every
seed-only D-layer pentagon.  The remaining normal-form step is the elementary
2D Clifford lemma encoded at the end of the file: an invertible triple with
these relations is GL2(C)-conjugate to X,Z,+/-Y.

No Groebner basis, numerical solve, or branch search is used.
"""
from __future__ import annotations

from collections import Counter
from itertools import product

import sympy as sp

import r22_epsminus_d_trace as tr
import r22_epsminus_d_probe as dp
import r22_epsminus_d_discrete_gauge_audit as dga
from r22_d_layer_probe import d_block_set, singleton_d_cases
from r22_local_associator import pentagon
from r22_scale_audit import M, ONE, N, f_class, layer_spec, pentagon_blocks, pentagon_deps

DEEP = (5, 7, 13, 15)
DSET = d_block_set()
SEEDS = set(tr.SEED_KEYS)
SPACES = tuple(product(M, repeat=3))


def generic_matrix(prefix: str):
    syms = sp.symbols(f"{prefix}00 {prefix}01 {prefix}10 {prefix}11")
    return sp.Matrix([[syms[0], syms[1]], [syms[2], syms[3]]]), syms


def registry_sub(registry, scalar, ddata):
    sub = {}
    for (meta, sym) in registry.symbols.items():
        key, row, col = meta
        cl = f_class(key)
        if cl in "ABC":
            sub[sym] = scalar[key]
        elif cl == "D":
            if key not in ddata:
                raise AssertionError(("unexpected seed-D dependency", key, tuple(ddata)))
            sub[sym] = ddata[key][row, col]
        else:
            raise AssertionError(("unexpected layer in seed-only pentagon", key, cl))
    return sub


def proportional_constant(actual: sp.Matrix, model: sp.Matrix, variables):
    """Return nonzero constant k with actual=k*model, else None."""
    vars_set = set(variables)
    ratio = None
    for i in range(model.rows):
        for j in range(model.cols):
            a = sp.expand(actual[i, j])
            b = sp.expand(model[i, j])
            if b == 0:
                if a != 0:
                    return None
                continue
            q = sp.cancel(a / b)
            if q == 0 or (q.free_symbols & vars_set):
                return None
            if ratio is None:
                ratio = q
            elif sp.simplify(q - ratio) != 0:
                return None
    if ratio is None or ratio == 0:
        return None
    if sp.simplify(actual - ratio * model) != sp.zeros(*model.shape):
        return None
    return sp.simplify(ratio)


def role_keys(space):
    m, n, out = space
    keys = {
        "L": ("h", m, n, out),
        "M": (m, "h", n, out),
        "R": (m, n, "h", out),
    }
    if not set(keys.values()) <= SEEDS:
        raise AssertionError(("missing seed role", space, keys))
    return keys


def pair_cases(space):
    m, n, out = space
    return (
        ({"a": "h", "b": m, "c": "h", "d": n}, out, ("L", "M")),
        ({"a": "h", "b": m, "c": n, "d": "h"}, out, ("L", "R")),
        ({"a": m, "b": "h", "c": n, "d": "h"}, out, ("M", "R")),
    )


def audit_seed_case_completeness():
    seed_only = set()
    for p in pentagon_blocks():
        if ONE in p[:4] or not layer_spec("D", p):
            continue
        deps = pentagon_deps(*p[:5]) & DSET
        if deps and deps <= SEEDS:
            seed_only.add(tuple(p[:5]))

    singleton = {tuple(p[:5]) for p, _target in singleton_d_cases()}
    pairs = set()
    for space in SPACES:
        for labels, total, _roles in pair_cases(space):
            pairs.add((labels["a"], labels["b"], labels["c"], labels["d"], total))

    if len(singleton) != 24 or len(pairs) != 24:
        raise AssertionError((len(singleton), len(pairs)))
    if singleton & pairs:
        raise AssertionError(("singleton/pair overlap", singleton & pairs))
    if seed_only != singleton | pairs:
        raise AssertionError(("seed-only D pentagons not exhausted", seed_only - singleton - pairs, (singleton | pairs) - seed_only))
    return len(seed_only)


def audit_conjugation_endpoints():
    """Every seed block is an endomorphism of its underlying 2D fusion space."""
    rows = []
    for key in sorted(SEEDS):
        source, target = dga.d_path_triples(key)
        src2 = [t for t in source if N(*t) == 2]
        tgt2 = [t for t in target if N(*t) == 2]
        if len(src2) != 1 or len(tgt2) != 1:
            raise AssertionError(("seed path does not contain one 2D vertex per side", key, source, target))
        underlying, _pos = dp.underlying_h_space(key)
        if src2[0] != underlying or tgt2[0] != underlying:
            raise AssertionError(("seed gauge is not conjugation on one 2D space", key, src2, tgt2, underlying))
        rows.append(key)
    return len(rows)


def audit_singletons():
    U, us = generic_matrix("u")
    profile = Counter()
    factors = Counter()
    for cid in DEEP:
        scalar = tr.scalar_assignment(cid)
        for p, target in singleton_d_cases():
            registry, _mats, diff = pentagon(dict(zip("abcd", p[:4])), p[4])
            sub = registry_sub(registry, scalar, {target: U})
            actual = diff.applyfunc(lambda e: sp.expand(e.xreplace(sub)))

            found = None
            for lam in (1, -1):
                model = U * U - lam * sp.eye(2)
                k = proportional_constant(actual, model, us)
                if k is not None:
                    found = (lam, k)
                    break
            if found is None:
                raise AssertionError(("singleton is not U^2=+/-I", cid, p[:5], target, actual))
            lam, k = found
            profile[lam] += 1
            factors[str(k)] += 1

    expected = len(DEEP) * 24
    if sum(profile.values()) != expected:
        raise AssertionError((profile, expected))
    return profile, factors


def audit_pairs():
    L, ls = generic_matrix("l")
    MM, ms = generic_matrix("m")
    R, rs = generic_matrix("r")
    matrices = {"L": L, "M": MM, "R": R}
    allvars = ls + ms + rs

    profile = Counter()
    factors = Counter()
    for cid in DEEP:
        scalar = tr.scalar_assignment(cid)
        for space in SPACES:
            keys = role_keys(space)
            ddata = {keys[role]: matrices[role] for role in ("L", "M", "R")}
            for labels, total, (ra, rb) in pair_cases(space):
                registry, _mats, diff = pentagon(labels, total)
                sub = registry_sub(registry, scalar, ddata)
                actual = diff.applyfunc(lambda e: sp.expand(e.xreplace(sub)))
                A, B = matrices[ra], matrices[rb]

                anti = proportional_constant(actual, A * B + B * A, allvars)
                comm = proportional_constant(actual, A * B - B * A, allvars)
                if anti is not None and comm is not None:
                    raise AssertionError(("pair relation ambiguously comm/anticomm", cid, space, ra, rb))
                if anti is not None:
                    profile["anticommute"] += 1
                    factors[str(anti)] += 1
                elif comm is not None:
                    profile["commute"] += 1
                    factors[str(comm)] += 1
                else:
                    raise AssertionError(("pair relation is neither commutator nor anticommutator", cid, space, ra, rb, actual))

    expected = len(DEEP) * len(SPACES) * 3
    if sum(profile.values()) != expected:
        raise AssertionError((profile, expected))
    return profile, factors


def audit_local_clifford_lemma():
    """Encode the elementary classification after diagonalizing M to Z."""
    a, b, u = sp.symbols("a b u", nonzero=True)
    Z = dp.PZ
    L = sp.Matrix([[0, a], [b, 0]])

    if sp.simplify(Z * L + L * Z) != sp.zeros(2):
        raise AssertionError("off-diagonal L does not anticommute with Z")
    if sp.simplify(L * L - a * b * sp.eye(2)) != sp.zeros(2):
        raise AssertionError("L square formula failed")

    # L^2=I gives ab=1.  Residual diagonal conjugation G=diag(a,1)
    # then sends L exactly to X while leaving Z fixed.
    G = sp.diag(a, 1)
    Ln = (G.inv() * L * G).subs(b, 1 / a).applyfunc(sp.simplify)
    if Ln != dp.PX or G.inv() * Z * G != Z:
        raise AssertionError(("residual diagonal normalization failed", Ln))

    # A matrix anticommuting with both Z and X is [[0,u],[-u,0]].
    R = sp.Matrix([[0, u], [-u, 0]])
    if sp.simplify(Z * R + R * Z) != sp.zeros(2):
        raise AssertionError("R/Z anticommutator failed")
    if sp.simplify(dp.PX * R + R * dp.PX) != sp.zeros(2):
        raise AssertionError("R/X anticommutator failed")
    if sp.simplify(R * R + u**2 * sp.eye(2)) != sp.zeros(2):
        raise AssertionError("R square formula failed")
    if sp.expand(u**2 + 1 - (u - sp.I) * (u + sp.I)) != 0:
        raise AssertionError("u^2+1 factorization failed")
    if R.subs(u, -sp.I) != dp.PY or R.subs(u, sp.I) != -dp.PY:
        raise AssertionError("R roots are not +/-Y")

    return {
        "diagonalize": "M^2=I and invertible anticommuting L force eigenvalues +1,-1, hence M~Z",
        "residual": "L=[[0,a],[b,0]], L^2=I => ab=1; diag(a,1) sends L to X",
        "third": "R anticommutes with Z,X => R=[[0,u],[-u,0]]; R^2=I => u=+/-i => R=+/-Y",
    }


def main():
    seed_case_count = audit_seed_case_completeness()
    conjugation_count = audit_conjugation_endpoints()
    square_profile, square_factors = audit_singletons()
    pair_profile, pair_factors = audit_pairs()

    print({
        "deep_scalar_components": DEEP,
        "multiplicity_two_spaces": len(SPACES),
        "seed_D_blocks": len(SEEDS),
        "seed_only_D_pentagons": seed_case_count,
        "seed_blocks_verified_as_GL2_conjugation_endomorphisms": conjugation_count,
        "singleton_square_profile": dict(square_profile),
        "singleton_scalar_factor_profile": dict(square_factors),
        "pair_relation_profile": dict(pair_profile),
        "pair_scalar_factor_profile": dict(pair_factors),
    }, flush=True)

    expected_singletons = len(DEEP) * 24
    expected_pairs = len(DEEP) * len(SPACES) * 3
    if square_profile != Counter({1: expected_singletons}):
        raise AssertionError(("seed squares are not uniformly +I", square_profile))
    if pair_profile != Counter({"anticommute": expected_pairs}):
        raise AssertionError(("seed pairs are not uniformly Clifford", pair_profile))

    lemma = audit_local_clifford_lemma()
    print("CLIFFORD_LEMMA", lemma, flush=True)
    print(
        "RESULT: every invertible epsilon-minus seed solution is independently GL2(C)-conjugate on each 2D multiplicity space to (X,Z,+/-Y); the 2^8 Pauli chirality census is projectively exhaustive",
        flush=True,
    )


if __name__ == "__main__":
    main()
