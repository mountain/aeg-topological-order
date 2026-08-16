"""Blind Fibonacci pentagon reconstruction from fusion grammar.

This script deliberately does not contain standard Fibonacci F- or R-symbol values.
It starts from the multiplicity-free fusion grammar

    1 x x = x x 1 = x
    t x t = 1 + t

with strict-unit normalization and symbolic nontrivial associators. It then:

1. enumerates fusion-tree bases for 3--5 tau anyons;
2. constructs the 4-anyon associahedral pentagon as local reassociation maps;
3. emits exact polynomial coherence equations;
4. derives the nondegenerate solution family up to vertex gauge;
5. applies a unitary-selection test without importing a known answer.

Research labels:
- CLASSICAL: fusion-tree decomposition, F-moves, pentagon coherence.
- REFORMULATION: sparse operation-history complex and edge-transport matrices.
- COMPUTATIONAL-CLAIM: exact equation generation/checks performed here.

No braiding/R-symbol data are used.
"""

from __future__ import annotations

from typing import Dict, List, Mapping, Sequence, Tuple, Union

import sympy as sp

ONE = "1"
TAU = "t"
LABELS = (ONE, TAU)

Leaf = str
Tree = Union[Leaf, Tuple["Tree", "Tree"]]
Path = Tuple[str, ...]
Labeling = Dict[Path, str]


def fuse(a: str, b: str) -> Tuple[str, ...]:
    """CLASSICAL: multiplicity-free Fibonacci fusion grammar."""
    if a == ONE:
        return (b,)
    if b == ONE:
        return (a,)
    if a == TAU and b == TAU:
        return (ONE, TAU)
    raise ValueError(f"unknown labels: {a}, {b}")


def parenthesizations(leaves: Sequence[str]) -> Tuple[Tree, ...]:
    """CLASSICAL: enumerate full binary parenthesizations in leaf order."""
    leaves = tuple(leaves)
    if len(leaves) == 1:
        return (leaves[0],)
    out: List[Tree] = []
    for cut in range(1, len(leaves)):
        for left in parenthesizations(leaves[:cut]):
            for right in parenthesizations(leaves[cut:]):
                out.append((left, right))
    return tuple(out)


def subtree_at(tree: Tree, path: Path) -> Tree:
    node = tree
    for step in path:
        if isinstance(node, str):
            raise ValueError(f"path {path} enters a leaf")
        node = node[0] if step == "L" else node[1]
    return node


def enumerate_labelings(
    tree: Tree, leaf_labels: Mapping[str, str], total: str | None = None
) -> List[Labeling]:
    """CLASSICAL: enumerate admissible internal fusion-channel assignments."""

    def rec(node: Tree, path: Path) -> List[Tuple[str, Labeling]]:
        if isinstance(node, str):
            return [(leaf_labels[node], {})]
        left, right = node
        result: List[Tuple[str, Labeling]] = []
        for left_label, left_map in rec(left, path + ("L",)):
            for right_label, right_map in rec(right, path + ("R",)):
                for out_label in fuse(left_label, right_label):
                    merged = dict(left_map)
                    merged.update(right_map)
                    merged[path] = out_label
                    result.append((out_label, merged))
        return result

    states = rec(tree, ())
    if total is not None:
        states = [(root, m) for root, m in states if root == total]
    return [m for _, m in states]


def root_label(
    tree: Tree, labeling: Mapping[Path, str], leaf_labels: Mapping[str, str], path: Path
) -> str:
    node = subtree_at(tree, path)
    return leaf_labels[node] if isinstance(node, str) else labeling[path]


def rotate_right_shape(tree: Tree, path: Path = ()) -> Tree:
    """CLASSICAL: ((A B) C) -> (A (B C)) at a selected node."""
    if not path:
        if isinstance(tree, str) or isinstance(tree[0], str):
            raise ValueError("selected node is not of shape ((A B) C)")
        (left_pair, c_tree) = tree
        a_tree, b_tree = left_pair
        return (a_tree, (b_tree, c_tree))
    if isinstance(tree, str):
        raise ValueError("path enters a leaf")
    head, *tail = path
    if head == "L":
        return (rotate_right_shape(tree[0], tuple(tail)), tree[1])
    if head == "R":
        return (tree[0], rotate_right_shape(tree[1], tuple(tail)))
    raise ValueError(f"invalid path step {head!r}")


def leafset_labels(tree: Tree, labeling: Mapping[Path, str]) -> Dict[frozenset[str], str]:
    """Index internal-channel labels by the subtree leaf set they fuse."""
    result: Dict[frozenset[str], str] = {}

    def walk(node: Tree, path: Path) -> frozenset[str]:
        if isinstance(node, str):
            return frozenset((node,))
        leaves = walk(node[0], path + ("L",)) | walk(node[1], path + ("R",))
        result[leaves] = labeling[path]
        return leaves

    walk(tree, ())
    return result


# Blind symbolic local F-data. The coefficient table uses old intermediate
# channel e as its first index and new channel f as its second index.
a, b, c, d, g = sp.symbols("a b c d g")
F_TTT_TO_TAU = {(ONE, ONE): a, (ONE, TAU): b, (TAU, ONE): c, (TAU, TAU): d}


def f_coefficient(x: str, y: str, z: str, out: str, old: str, new: str) -> sp.Expr:
    """CLASSICAL + T0 normalization: symbolic local associator coefficient."""
    if ONE in (x, y, z):
        return sp.Integer(1)
    if (x, y, z) != (TAU, TAU, TAU):
        raise ValueError("unexpected simple-object triple")
    if out == ONE:
        if old != TAU or new != TAU:
            raise ValueError("inadmissible ttt -> 1 channel")
        return g
    if out == TAU:
        return F_TTT_TO_TAU[(old, new)]
    raise ValueError(f"unexpected total {out}")


def basis_sort_key(labeling: Mapping[Path, str]) -> Tuple[Tuple[Path, str], ...]:
    return tuple(sorted(labeling.items()))


def reassociation_matrix(
    source: Tree, path: Path, total: str, leaf_labels: Mapping[str, str]
) -> Tuple[Tree, List[Labeling], List[Labeling], sp.Matrix]:
    """REFORMULATION: sparse edge transport for one local F-move.

    Matrix convention: columns are source fusion histories and rows are target
    fusion histories, so compositions multiply from the left.
    """
    target = rotate_right_shape(source, path)
    source_basis = sorted(enumerate_labelings(source, leaf_labels, total), key=basis_sort_key)
    target_basis = sorted(enumerate_labelings(target, leaf_labels, total), key=basis_sort_key)
    matrix = sp.zeros(len(target_basis), len(source_basis))

    p_a = path + ("L", "L")
    p_b = path + ("L", "R")
    p_c = path + ("R",)
    p_old = path + ("L",)
    p_out = path
    p_new = path + ("R",)

    for col, source_state in enumerate(source_basis):
        x = root_label(source, source_state, leaf_labels, p_a)
        y = root_label(source, source_state, leaf_labels, p_b)
        z = root_label(source, source_state, leaf_labels, p_c)
        old = source_state[p_old]
        out = source_state[p_out]
        source_leafsets = leafset_labels(source, source_state)

        for row, target_state in enumerate(target_basis):
            target_leafsets = leafset_labels(target, target_state)
            common = source_leafsets.keys() & target_leafsets.keys()
            if any(source_leafsets[s] != target_leafsets[s] for s in common):
                continue
            new = target_state[p_new]
            matrix[row, col] = f_coefficient(x, y, z, out, old, new)

    return target, source_basis, target_basis, matrix


P0: Tree = ((("a", "b"), "c"), "d")
P1: Tree = (("a", ("b", "c")), "d")
P2: Tree = ("a", (("b", "c"), "d"))
P3: Tree = ("a", ("b", ("c", "d")))
P4: Tree = (("a", "b"), ("c", "d"))
LEAF_LABELS_4 = {name: TAU for name in "abcd"}


def pentagon_matrices(total: str) -> Dict[str, sp.Matrix]:
    """COMPUTATIONAL-CLAIM: build the five local transports of K_4."""
    t1, _, _, m01 = reassociation_matrix(P0, ("L",), total, LEAF_LABELS_4)
    t2, _, _, m12 = reassociation_matrix(P1, (), total, LEAF_LABELS_4)
    t3, _, _, m23 = reassociation_matrix(P2, ("R",), total, LEAF_LABELS_4)
    t4, _, _, m04 = reassociation_matrix(P0, (), total, LEAF_LABELS_4)
    t5, _, _, m43 = reassociation_matrix(P4, (), total, LEAF_LABELS_4)
    assert (t1, t2, t3, t4, t5) == (P1, P2, P3, P4, P3)
    return {"01": m01, "12": m12, "23": m23, "04": m04, "43": m43}


def pentagon_difference(total: str) -> sp.Matrix:
    matrices = pentagon_matrices(total)
    long_path = matrices["23"] * matrices["12"] * matrices["01"]
    short_path = matrices["43"] * matrices["04"]
    return sp.simplify(long_path - short_path)


def nonzero_equations(matrix: sp.Matrix) -> List[sp.Expr]:
    out: List[sp.Expr] = []
    for entry in matrix:
        entry = sp.factor(sp.expand(entry))
        if entry != 0 and entry not in out:
            out.append(entry)
    return out


def all_pentagon_equations() -> List[sp.Expr]:
    equations: List[sp.Expr] = []
    for total in LABELS:
        for eq in nonzero_equations(pentagon_difference(total)):
            if eq not in equations:
                equations.append(eq)
    return equations


def derive_nondegenerate_solution() -> Dict[str, sp.Expr]:
    """COMPUTATIONAL-CLAIM: derive the generic invertible associator branch."""
    eqs = [sp.expand(e) for e in all_pentagon_equations()]
    required = [
        a - b * c * g,
        a * g**2 - b * c,
        b * d * (g - 1),
        c * d * (g - 1),
        b * (a + d**2 - 1),
        c * (a + d**2 - 1),
        b * (a + d * g),
        c * (a + d * g),
    ]
    normalized = {sp.factor(e) for e in eqs} | {-sp.factor(e) for e in eqs}
    assert all(sp.factor(r) in normalized for r in required)

    # Nondegeneracy forces bc != 0: a=bcg and bc=0 imply a=0, making
    # det([[a,c],[b,d]]) vanish. Then a+dg=0 and d(g-1)=0 force g=1.
    # The residual equations give d=-a, bc=a, a^2+a-1=0.
    return {
        "g": sp.Integer(1),
        "d": -a,
        "bc": a,
        "minimal_polynomial": a**2 + a - 1,
        "determinant": sp.Integer(-1),
    }


def verify_solution_family() -> None:
    """COMPUTATIONAL-CLAIM: independent substitution check of the family."""
    relation = {g: 1, d: -a, c: a / b}
    for total in LABELS:
        diff = pentagon_difference(total).subs(relation)
        for entry in diff:
            numerator = sp.together(entry).as_numer_denom()[0]
            reduced = sp.rem(sp.Poly(numerator, a), sp.Poly(a**2 + a - 1, a))
            assert sp.simplify(reduced.as_expr()) == 0


def history_counts() -> Dict[int, Dict[str, int]]:
    """COMPUTATIONAL-CLAIM: basis dimensions and parenthesization counts."""
    result: Dict[int, Dict[str, int]] = {}
    for n in (3, 4, 5):
        leaves = tuple(chr(ord("a") + i) for i in range(n))
        trees = parenthesizations(leaves)
        leaf_labels = {leaf: TAU for leaf in leaves}
        dims = {}
        for total in LABELS:
            per_tree = {len(enumerate_labelings(tree, leaf_labels, total)) for tree in trees}
            assert len(per_tree) == 1
            dims[total] = per_tree.pop()
        result[n] = {"parenthesizations": len(trees), "dim_1": dims[ONE], "dim_t": dims[TAU]}
    return result


def unitary_selection() -> Dict[str, sp.Expr | bool]:
    """CLASSICAL/COMPUTATIONAL: select the algebraic branch compatible with unitarity."""
    roots = sp.solve(sp.Eq(a**2 + a - 1, 0), a)
    admissible = [root for root in roots if abs(float(sp.N(root))) <= 1 + 1e-12]
    assert len(admissible) == 1
    chosen = admissible[0]
    block = sp.Matrix([[chosen, sp.sqrt(chosen)], [sp.sqrt(chosen), -chosen]])
    assert sp.simplify(block.det() + 1) == 0
    assert (block.T * block).applyfunc(sp.simplify) == sp.eye(2)
    return {"root": chosen, "orthogonal_gauge_exists": True}


def main() -> None:
    print("history-counts")
    for n, data in history_counts().items():
        print(n, data)

    for total in LABELS:
        print(f"\n4-tau pentagon, total={total}")
        for name, matrix in pentagon_matrices(total).items():
            print(name)
            print(matrix)
        print("difference")
        print(pentagon_difference(total))

    print("\nunique coherence equations")
    for eq in all_pentagon_equations():
        print(sp.factor(eq), "= 0")

    print("\nnondegenerate family")
    for key, value in derive_nondegenerate_solution().items():
        print(f"{key}: {value}")

    verify_solution_family()
    print("independent substitution verification: PASS")

    print("unitary selection")
    for key, value in unitary_selection().items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
