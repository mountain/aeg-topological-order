"""Five-input associahedron check for the Fibonacci history local system.

Uses the already-frozen blind solution from fibonacci_pentagon.py. It builds
all 14 parenthesizations of five tau inputs, their 21 single-rotation edges,
identifies chordless 2-cell boundaries, and verifies exact trivial holonomy on
all 3 square and 6 pentagonal faces in both total-charge sectors.
"""

from collections import Counter
import sympy as sp

import fibonacci_pentagon as fp


def all_paths(tree, path=()):
    yield path
    if not isinstance(tree, str):
        yield from all_paths(tree[0], path + ("L",))
        yield from all_paths(tree[1], path + ("R",))


def can_rotate_right(tree, path):
    node = fp.subtree_at(tree, path)
    return not isinstance(node, str) and not isinstance(node[0], str)


def rotate_left(tree, path=()):
    if not path:
        if isinstance(tree, str) or isinstance(tree[1], str):
            raise ValueError("not of shape (A (B C))")
        A, BC = tree
        B, C = BC
        return ((A, B), C)
    if isinstance(tree, str):
        raise ValueError("path enters leaf")
    head, *tail = path
    if head == "L":
        return (rotate_left(tree[0], tuple(tail)), tree[1])
    return (tree[0], rotate_left(tree[1], tuple(tail)))


def can_rotate_left(tree, path):
    node = fp.subtree_at(tree, path)
    return not isinstance(node, str) and not isinstance(node[1], str)


def build_graph():
    trees = fp.parenthesizations(tuple("abcde"))
    index = {repr(tree): i for i, tree in enumerate(trees)}
    adjacency = {i: set() for i in range(len(trees))}
    right_edges = {}
    for i, tree in enumerate(trees):
        for path in all_paths(tree):
            if can_rotate_right(tree, path):
                target = fp.rotate_right_shape(tree, path)
                j = index[repr(target)]
                adjacency[i].add(j)
                adjacency[j].add(i)
                right_edges[(i, j)] = path
            if can_rotate_left(tree, path):
                target = rotate_left(tree, path)
                j = index[repr(target)]
                adjacency[i].add(j)
                adjacency[j].add(i)
    return trees, adjacency, right_edges


def canonical_cycle(cycle):
    n = len(cycle)
    variants = []
    for seq in (list(cycle), list(reversed(cycle))):
        for i in range(n):
            variants.append(tuple(seq[i:] + seq[:i]))
    return min(variants)


def chordless(cycle, adjacency):
    n = len(cycle)
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if cycle[j] in adjacency[cycle[i]]:
                return False
    return True


def faces(adjacency):
    cycles = set()
    for start in adjacency:
        stack = [(start, [start])]
        while stack:
            current, path = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor == start and len(path) >= 3:
                    cycles.add(canonical_cycle(path))
                elif neighbor not in path and len(path) < 5:
                    stack.append((neighbor, path + [neighbor]))
    return sorted(
        (cycle for cycle in cycles if len(cycle) in (4, 5) and chordless(cycle, adjacency)),
        key=lambda cycle: (len(cycle), cycle),
    )


def exact_solution_substitution():
    alpha = (-1 + sp.sqrt(5)) / 2
    return {
        fp.a: alpha,
        fp.b: sp.sqrt(alpha),
        fp.c: sp.sqrt(alpha),
        fp.d: -alpha,
        fp.g: 1,
    }


def edge_matrix(i, j, total, trees, right_edges):
    leaf_labels = {name: fp.TAU for name in "abcde"}
    substitution = exact_solution_substitution()
    if (i, j) in right_edges:
        path = right_edges[(i, j)]
        target, _, _, matrix = fp.reassociation_matrix(trees[i], path, total, leaf_labels)
        assert repr(target) == repr(trees[j])
        return sp.simplify(matrix.subs(substitution))
    if (j, i) in right_edges:
        return sp.simplify(edge_matrix(j, i, total, trees, right_edges).inv())
    raise KeyError((i, j))


def cycle_holonomy(cycle, total, trees, right_edges):
    leaf_labels = {name: fp.TAU for name in "abcde"}
    dim = len(fp.enumerate_labelings(trees[cycle[0]], leaf_labels, total))
    holonomy = sp.eye(dim)
    for i, j in zip(cycle, cycle[1:] + cycle[:1]):
        holonomy = sp.simplify(edge_matrix(i, j, total, trees, right_edges) * holonomy)
    return holonomy


def main():
    trees, adjacency, right_edges = build_graph()
    face_cycles = faces(adjacency)
    counts = Counter(map(len, face_cycles))

    print("vertices:", len(trees))
    print("edges:", sum(map(len, adjacency.values())) // 2)
    print("degree multiset:", sorted(map(len, adjacency.values())))
    print("faces:", dict(counts))

    assert len(trees) == 14
    assert sum(map(len, adjacency.values())) // 2 == 21
    assert all(len(adjacency[i]) == 3 for i in adjacency)
    assert counts == Counter({5: 6, 4: 3})

    for total in fp.LABELS:
        for cycle in face_cycles:
            holonomy = cycle_holonomy(list(cycle), total, trees, right_edges)
            assert all(sp.simplify(x) == 0 for x in holonomy - sp.eye(holonomy.rows))
        print(f"total={total}: all {len(face_cycles)} face holonomies are identity")


if __name__ == "__main__":
    main()
