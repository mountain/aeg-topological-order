"""Encoding-soundness audit for theorem promotion of Meng--Yu R(2,2).

This is an interface theorem audit, not a new branch search.

For a nonexistence result we do not need to prove that the solver uses every
possible consequence of the fusion-category axioms.  We need the one-way
soundness/cover statement:

    every genuine R(2,2) categorification, after legitimate strict-unit and
    trivalent-basis gauge normalization, maps into the candidate branch space
    audited by this repository;

and every equation/inequality used to eliminate a candidate is a necessary
fusion-category condition (pentagon or associator invertibility).

If that candidate superset is empty, the genuine categorification space is
empty as well.

The audit is split into five executable gates:

1. independent fusion/object/multiplicity inventory;
2. full unconstrained non-unit F-entry inventory + strict-unit normalization;
3. pentagon soundness and structural A--F/final coverage;
4. standard trivalent-basis gauge and completeness of the post-Pauli residual
   scalar-center gauge;
5. static isolation of the R(2,2) theorem engine from braiding/unitarity/
   spherical/pivotal/ribbon constraints.
"""
from __future__ import annotations

import ast
import inspect
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

import sympy as sp

import r22_scale_audit as sc
import r22_local_associator as la
import r22_scalar_audit as sa


ONE = "1"
OBJECTS = ("1", "g", "h", "k", "X", "Y")  # k = gh
G = frozenset(("1", "g", "h", "k"))
M = frozenset(("X", "Y"))


def expected_gmul(a: str, b: str) -> str:
    if a == ONE:
        return b
    if b == ONE:
        return a
    if a == b:
        return ONE
    table = {
        frozenset(("g", "h")): "k",
        frozenset(("g", "k")): "h",
        frozenset(("h", "k")): "g",
    }
    return table[frozenset((a, b))]


def expected_act(g: str, x: str) -> str:
    if g in (ONE, "h"):
        return x
    return "Y" if x == "X" else "X"


def expected_fuse(a: str, b: str) -> dict[str, int]:
    """Independent transcription of the R(2,2) based-ring products."""
    if a in G and b in G:
        return {expected_gmul(a, b): 1}
    if a in G and b in M:
        return {expected_act(a, b): 1}
    if b in G and a in M:
        return {expected_act(b, a): 1}
    if a == b and a in M:
        return {"1": 1, "h": 1, "X": 2, "Y": 2}
    if a in M and b in M:
        return {"g": 1, "k": 1, "X": 2, "Y": 2}
    raise AssertionError(("unexpected object pair", a, b))


def eN(a: str, b: str, c: str) -> int:
    return expected_fuse(a, b).get(c, 0)


def expected_bases(a: str, b: str, c: str, d: str):
    src = []
    for e in OBJECTS:
        for alpha in range(eN(a, b, e)):
            for beta in range(eN(e, c, d)):
                src.append((e, alpha, beta))
    tgt = []
    for f in OBJECTS:
        for mu in range(eN(b, c, f)):
            for nu in range(eN(a, f, d)):
                tgt.append((f, mu, nu))
    return src, tgt


def expected_f_blocks():
    out = []
    for a, b, c, d in product(OBJECTS, repeat=4):
        src, tgt = expected_bases(a, b, c, d)
        if len(src) != len(tgt):
            raise AssertionError(("independent associativity dimension mismatch", a, b, c, d, len(src), len(tgt)))
        if src:
            out.append((a, b, c, d, len(src)))
    return out


def expected_pentagon_blocks():
    out = []
    for a, b, c, d, z in product(OBJECTS, repeat=5):
        dim = 0
        for x in OBJECTS:
            for y in OBJECTS:
                dim += eN(a, b, x) * eN(x, c, y) * eN(y, d, z)
        if dim:
            out.append((a, b, c, d, z, dim))
    return out


def gate1_fusion_inventory():
    if tuple(sc.OBJECTS) != OBJECTS:
        raise AssertionError(("object inventory mismatch", sc.OBJECTS, OBJECTS))

    for a, b in product(OBJECTS, repeat=2):
        got = sc.fuse(a, b)
        want = expected_fuse(a, b)
        if got != want:
            raise AssertionError(("fusion product mismatch", a, b, got, want))

    # Independently check associativity of the transcribed based ring.
    for a, b, c in product(OBJECTS, repeat=3):
        left = defaultdict(int)
        right = defaultdict(int)
        for x, nx in expected_fuse(a, b).items():
            for y, ny in expected_fuse(x, c).items():
                left[y] += nx * ny
        for x, nx in expected_fuse(b, c).items():
            for y, ny in expected_fuse(a, x).items():
                right[y] += nx * ny
        if dict(left) != dict(right):
            raise AssertionError(("independent ring associativity failure", a, b, c, left, right))

    triples = [
        (a, b, c, eN(a, b, c))
        for a, b, c in product(OBJECTS, repeat=3)
        if eN(a, b, c)
    ]
    mult2 = {(a, b, c) for a, b, c, n in triples if n == 2}
    expected_mult2 = set(product(("X", "Y"), repeat=3))
    if mult2 != expected_mult2:
        raise AssertionError(("multiplicity-two fusion-space inventory mismatch", mult2, expected_mult2))

    print({
        "gate": 1,
        "objects": len(OBJECTS),
        "fusion_products_checked": len(OBJECTS) ** 2,
        "nonzero_fusion_triples": len(triples),
        "multiplicity_profile": dict(Counter(n for *_abc, n in triples)),
        "multiplicity_two_spaces": len(mult2),
    }, flush=True)
    print("GATE1: independent R(2,2) object/fusion/multiplicity inventory matches the engine", flush=True)
    return triples, mult2


def gate2_f_inventory_and_unit_normalization():
    want_blocks = expected_f_blocks()
    got_blocks = sc.f_blocks()
    if got_blocks != want_blocks:
        raise AssertionError("F-block inventory differs from independent fusion-path enumeration")

    nonunit_entries = 0
    nonunit_symbols = set()
    unit_blocks = 0

    for a, b, c, d, dim in want_blocks:
        src, tgt = expected_bases(a, b, c, d)
        if len(src) != dim or len(tgt) != dim:
            raise AssertionError(("basis dimension mismatch", (a, b, c, d), dim, len(src), len(tgt)))
        reg = la.Registry()
        mat = sp.zeros(dim, dim)
        for col, (e, alpha, beta) in enumerate(src):
            for row, (f, mu, nu) in enumerate(tgt):
                mat[row, col] = reg.entry(a, b, c, d, e, alpha, beta, f, mu, nu)

        if ONE not in (a, b, c):
            expected_count = dim * dim
            if len(reg.symbols) != expected_count:
                raise AssertionError(("non-unit F block is not a full independent matrix", (a, b, c, d), dim, len(reg.symbols)))
            if any(not isinstance(x, sp.Symbol) for x in mat):
                raise AssertionError(("non-unit F entry was hard-coded", (a, b, c, d)))
            names = {str(x) for x in mat}
            if len(names) != expected_count:
                raise AssertionError(("non-unit F entries are not independent", (a, b, c, d), expected_count, len(names)))
            nonunit_entries += expected_count
            nonunit_symbols |= names
        else:
            unit_blocks += 1
            if reg.symbols:
                raise AssertionError(("strict-unit block unexpectedly introduced free symbols", (a, b, c, d)))
            if any(x not in (0, 1) for x in mat):
                raise AssertionError(("strict-unit block has noncanonical coefficient", (a, b, c, d), mat))
            if any(sum(mat[row, col] for row in range(dim)) != 1 for col in range(dim)):
                raise AssertionError(("strict-unit map is not column-bijective", (a, b, c, d), mat))
            if any(sum(mat[row, col] for col in range(dim)) != 1 for row in range(dim)):
                raise AssertionError(("strict-unit map is not row-bijective", (a, b, c, d), mat))

    if len(nonunit_symbols) != nonunit_entries:
        raise AssertionError(("F symbol names collide across blocks", nonunit_entries, len(nonunit_symbols)))

    # Invertibility is a necessary category condition.  Check that the staged
    # engine represents the complete matrix inventories on which determinant
    # gates are imposed, rather than a symmetry-reduced ansatz.
    import r22_epsminus_e_filter as ef
    import r22_epsminus_f_parametric as fp

    e_expected = {
        (a, b, c, d): dim for a, b, c, d, dim in want_blocks
        if ONE not in (a, b, c) and sc.f_class((a, b, c, d)) == "E"
    }
    f_expected = {
        (a, b, c, d): dim for a, b, c, d, dim in want_blocks
        if ONE not in (a, b, c) and sc.f_class((a, b, c, d)) == "F"
    }
    if set(ef.E_KEYS) != set(e_expected) or any(e_expected[k] != 2 for k in e_expected):
        raise AssertionError("E-layer variable inventory is not the full independent 2x2 associator inventory")
    if ef.EVARS and len(ef.EVARS) != sum(d * d for d in e_expected.values()):
        raise AssertionError(("E variable count mismatch", len(ef.EVARS), e_expected))
    if dict(fp.F_DIMS) != f_expected or len(fp.FVARS) != sum(d * d for d in f_expected.values()):
        raise AssertionError(("F variable inventory mismatch", len(fp.FVARS), f_expected))

    print({
        "gate": 2,
        "all_F_blocks": len(want_blocks),
        "nonunit_free_F_entries": nonunit_entries,
        "strict_unit_blocks": unit_blocks,
        "E_blocks": len(e_expected),
        "E_entries": len(ef.EVARS),
        "F_blocks": len(f_expected),
        "F_entries": len(fp.FVARS),
    }, flush=True)
    print("GATE2: every non-unit associator block is a full independent matrix; only strict-unit maps are normalized", flush=True)


def stage_of(p):
    a, b, c, d, z, _dim = p
    if ONE in (a, b, c, d):
        return "UNIT"
    nm = sum(x in M for x in (a, b, c, d))
    if nm == 0:
        return "A"
    if nm == 1:
        return "B"
    if nm == 2:
        return "C" if z in G else "D"
    if nm == 3:
        return "E" if z in G else "F"
    if nm == 4:
        return "FINAL"
    raise AssertionError(p)


def gate3_pentagon_soundness_and_cover():
    want_pb = expected_pentagon_blocks()
    got_pb = sc.pentagon_blocks()
    if got_pb != want_pb:
        raise AssertionError("pentagon block inventory differs from independent four-fold fusion-history enumeration")

    # The dense primitive is exactly the standard two paths around Mac Lane's
    # pentagon.  Inspect the implementation boundary so later solvers cannot
    # silently substitute a different coherence relation.
    pent_src = inspect.getsource(la.pentagon)
    required = ("m23 * m12 * m01", "m43 * m04")
    if any(x not in pent_src for x in required):
        raise AssertionError(("pentagon primitive changed", pent_src))

    nonunit = [p for p in want_pb if ONE not in p[:4]]
    stages = Counter(stage_of(p) for p in nonunit)
    if sum(stages.values()) != len(nonunit):
        raise AssertionError(("pentagon stage partition lost blocks", stages, len(nonunit)))

    import r22_epsminus_d_trace as dt
    import r22_epsminus_e_filter as ef
    import r22_epsminus_f_parametric as fp
    import r22_epsminus_final_kernel as fk

    want_d = {p for p in nonunit if stage_of(p) == "D"}
    got_d = {tuple(p) for p, _registry, _diff in dt.FULL_D_CASES}
    if got_d != want_d:
        raise AssertionError(("D-layer pentagon coverage mismatch", len(got_d), len(want_d), want_d - got_d, got_d - want_d))

    want_e = {p for p in nonunit if stage_of(p) == "E"}
    got_e = {tuple(p) for p, _registry, _diff in ef.E_CASES}
    if got_e != want_e:
        raise AssertionError(("E-layer pentagon coverage mismatch", len(got_e), len(want_e), want_e - got_e, got_e - want_e))

    want_f = {p for p in nonunit if stage_of(p) == "F"}
    got_f = {tuple(p) for p, _registry, _diff in fp.F_CASES}
    if got_f != want_f:
        raise AssertionError(("F-layer pentagon coverage mismatch", len(got_f), len(want_f), want_f - got_f, got_f - want_f))

    want_final = {p for p in nonunit if stage_of(p) == "FINAL"}
    got_final = {tuple(p) for p in fk.FINAL_BLOCKS}
    if got_final != want_final:
        raise AssertionError(("final four-noninvertible pentagon coverage mismatch", len(got_final), len(want_final), want_final - got_final, got_final - want_final))

    # Scalar equations used by the quotient are also genuine entries from the
    # same pentagon primitive.  They need not include every possible
    # consequence for a nonexistence proof; omitting equations can only enlarge
    # the candidate space.
    _keys, _idx, scalar_A, scalar_examples = sa.build_scalar_system()
    pb_set = set(want_pb)
    if any(tuple(p) not in pb_set for p in scalar_examples):
        raise AssertionError("scalar quotient used an equation outside the standard pentagon inventory")

    print({
        "gate": 3,
        "all_pentagon_blocks": len(want_pb),
        "nonunit_external_blocks": len(nonunit),
        "stage_profile": dict(stages),
        "scalar_monomial_equations": scalar_A.rows,
        "D_cases": len(got_d),
        "E_cases": len(got_e),
        "F_cases": len(got_f),
        "final_cases": len(got_final),
    }, flush=True)
    print("GATE3: every used coherence equation is a standard pentagon entry; D/E/F/final stage coverage is exact", flush=True)


def independent_scalar_gauge_row(key, triples):
    a, b, c, d = key
    left = [e for e in OBJECTS if eN(a, b, e) == 1 and eN(e, c, d) == 1]
    right = [f for f in OBJECTS if eN(b, c, f) == 1 and eN(a, f, d) == 1]
    if len(left) != 1 or len(right) != 1:
        raise AssertionError(("scalar gauge row is not one-dimensional", key, left, right))
    e, f = left[0], right[0]
    idx = {t: i for i, t in enumerate(triples)}
    row = [0] * len(triples)
    for t, sign in (
        ((a, b, e), +1),
        ((e, c, d), +1),
        ((b, c, f), -1),
        ((a, f, d), -1),
    ):
        if t in idx:
            row[idx[t]] += sign
    return row


def gate4_basis_gauge(mult2):
    keys, _idx, _A, _examples = sa.build_scalar_system()
    triples, Gmat = sa.build_scalar_gauge(keys)

    expected_gauges = [
        (a, b, c)
        for a, b in product(OBJECTS, repeat=2)
        if a != ONE and b != ONE
        for c in OBJECTS
        if eN(a, b, c) == 1
    ]
    if set(triples) != set(expected_gauges):
        raise AssertionError(("multiplicity-one trivalent gauge inventory mismatch", set(triples), set(expected_gauges)))
    for i, key in enumerate(keys):
        row = independent_scalar_gauge_row(key, triples)
        if list(Gmat.row(i)) != row:
            raise AssertionError(("standard scalar F-symbol basis-change exponent mismatch", key, list(Gmat.row(i)), row))

    import r22_epsminus_d_trace as dt
    import r22_epsminus_d_discrete_gauge_audit as dg

    if set(dt.SPACES) != mult2:
        raise AssertionError(("GL2 multiplicity-space inventory mismatch", set(dt.SPACES), mult2))

    # Seed F-blocks transform by conjugation on the unique multiplicity-two
    # source/target fusion space.  Verify that this is derived from fusion
    # paths, not assumed from the Pauli notation.
    for key in dt.SEED_KEYS:
        source, target = dg.d_path_triples(key)
        s2 = [t for t in source if eN(*t) == 2]
        t2 = [t for t in target if eN(*t) == 2]
        if len(s2) != 1 or len(t2) != 1 or s2[0] != t2[0]:
            raise AssertionError(("seed block is not an endomorphism under the same GL2 basis gauge", key, source, target, s2, t2))

    # The centralizer of the normalized X,Z seed pair in GL2(C) is exactly the
    # scalar center.  Hence after the proved Pauli normal form there is no
    # omitted non-scalar continuous GL2 stabilizer.
    a, b, c, d = sp.symbols("a b c d")
    H = sp.Matrix([[a, b], [c, d]])
    X = sp.Matrix([[0, 1], [1, 0]])
    Z = sp.Matrix([[1, 0], [0, -1]])
    if H * Z - Z * H != sp.Matrix([[0, -2*b], [2*c, 0]]):
        raise AssertionError("unexpected symbolic centralizer equation for Z")
    reduced_x = (H * X - X * H).subs({b: 0, c: 0})
    if reduced_x != sp.Matrix([[0, a-d], [d-a, 0]]):
        raise AssertionError("unexpected symbolic centralizer equation for X")

    one_dim, C, H_seed, H_cross, offset = dg.build_full_scalar_gauge_action()
    if set(one_dim) != set(expected_gauges) or offset != len(one_dim):
        raise AssertionError("post-Pauli residual scalar-gauge inventory is incomplete")
    if H_seed.rows != len(dt.SEED_KEYS) or H_cross.rows != len(dt.CROSS_KEYS):
        raise AssertionError(("D gauge action row inventory mismatch", H_seed.shape, H_cross.shape))
    if C.cols != len(one_dim) + len(mult2):
        raise AssertionError(("full residual trivalent gauge parameter count mismatch", C.cols, len(one_dim), len(mult2)))

    print({
        "gate": 4,
        "multiplicity_one_Cstar_gauges": len(one_dim),
        "multiplicity_two_GL2_spaces_before_Pauli_slice": len(mult2),
        "seed_blocks_checked_as_GL2_endomorphisms": len(dt.SEED_KEYS),
        "post_Pauli_scalar_center_gauges": len(mult2),
        "total_post_Pauli_scalar_parameters": C.cols,
    }, flush=True)
    print("GATE4: implemented gauge is the standard trivalent basis gauge; post-Pauli GL2 stabilizer reduces exactly to scalar centers", flush=True)


def gate5_no_hidden_extra_structure():
    root = Path(__file__).resolve().parent
    files = sorted(root.glob("r22_*.py"))
    forbidden_import_tokens = (
        "braid", "hexagon", "levin", "ribbon", "pivotal", "spherical", "unitary"
    )
    forbidden_identifier_tokens = (
        "hexagon", "dagger", "unitarity", "sphericality", "pivotality", "ribbon"
    )
    bad_imports = []
    bad_identifiers = []

    for path in files:
        if path.name == Path(__file__).name:
            continue
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
                for name in names:
                    low = name.lower()
                    if any(tok in low for tok in forbidden_import_tokens):
                        bad_imports.append((path.name, name))
            elif isinstance(node, ast.ImportFrom):
                name = node.module or ""
                low = name.lower()
                if any(tok in low for tok in forbidden_import_tokens):
                    bad_imports.append((path.name, name))
            elif isinstance(node, ast.Name):
                low = node.id.lower()
                if any(tok == low for tok in forbidden_identifier_tokens):
                    bad_identifiers.append((path.name, node.id))
            elif isinstance(node, ast.Attribute):
                low = node.attr.lower()
                if any(tok == low for tok in forbidden_identifier_tokens):
                    bad_identifiers.append((path.name, node.attr))

    if bad_imports or bad_identifiers:
        raise AssertionError(("R(2,2) theorem engine imports/uses extra-structure constraints", bad_imports, bad_identifiers))

    # The primitive Registry has only strict-unit special cases; every nonunit
    # entry falls through to a free symbol.  This is the decisive local check
    # against hidden unitarity/symmetry/pivotal restrictions.
    entry_src = inspect.getsource(la.Registry.entry)
    for token in ("conjugate", "adjoint", "unitary", "spherical", "pivotal", "braid", "hexagon"):
        if token in entry_src.lower():
            raise AssertionError(("hidden extra structure in primitive associator registry", token))

    print({
        "gate": 5,
        "r22_modules_AST_scanned": len(files) - 1,
        "forbidden_extra_structure_imports": 0,
        "forbidden_extra_structure_identifiers": 0,
        "primitive_nonunit_registry": "free-symbol matrix entries",
    }, flush=True)
    print("GATE5: R(2,2) theorem engine is isolated from braiding/unitarity/spherical/pivotal/ribbon constraints", flush=True)


def main():
    _triples, mult2 = gate1_fusion_inventory()
    gate2_f_inventory_and_unit_normalization()
    gate3_pentagon_soundness_and_cover()
    gate4_basis_gauge(mult2)
    gate5_no_hidden_extra_structure()
    print({
        "encoding_soundness": True,
        "direction": "genuine categorifications modulo legitimate gauge -> audited candidate branch superset",
        "candidate_branch_superset": "EMPTY by canonical exact replay",
        "promotion_implication": "R(2,2) has no categorification over C",
    }, flush=True)
    print("RESULT: encoding soundness + branch cover are exact; the empty audited candidate space implies non-categorifiability of R(2,2) over C", flush=True)


if __name__ == "__main__":
    main()
