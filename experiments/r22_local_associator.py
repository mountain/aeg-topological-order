from __future__ import annotations

import sympy as sp

from r22_scale_audit import ONE, OBJECTS, fuse, N

P0 = ((("a", "b"), "c"), "d")
P1 = (("a", ("b", "c")), "d")
P2 = ("a", (("b", "c"), "d"))
P3 = ("a", ("b", ("c", "d")))
P4 = (("a", "b"), ("c", "d"))


def subtree_at(tree, path):
    node = tree
    for step in path:
        node = node[0] if step == "L" else node[1]
    return node


def enum_states(tree, leaf_labels, total=None):
    def rec(node, path):
        if isinstance(node, str):
            return [(leaf_labels[node], {})]
        res = []
        for la, sa in rec(node[0], path + ("L",)):
            for lb, sb in rec(node[1], path + ("R",)):
                for out, mult in fuse(la, lb).items():
                    for idx in range(mult):
                        st = dict(sa)
                        st.update(sb)
                        st[path] = (out, idx)
                        res.append((out, st))
        return res

    vals = rec(tree, ())
    if total is not None:
        vals = [(r, s) for r, s in vals if r == total]
    return [s for _, s in vals]


def leafsets_state(tree, state):
    out = {}

    def walk(node, path):
        if isinstance(node, str):
            return frozenset([node])
        ss = walk(node[0], path + ("L",)) | walk(node[1], path + ("R",))
        out[ss] = state[path]
        return ss

    walk(tree, ())
    return out


def root_label(tree, state, leaf_labels, path):
    node = subtree_at(tree, path)
    return leaf_labels[node] if isinstance(node, str) else state[path][0]


def rotate_right(tree, path=()):
    if not path:
        ab, c = tree
        a, b = ab
        return (a, (b, c))
    head, *tail = path
    if head == "L":
        return (rotate_right(tree[0], tuple(tail)), tree[1])
    return (tree[0], rotate_right(tree[1], tuple(tail)))


class Registry:
    """Symbolic local F entries with strict-unit normalization."""

    def __init__(self):
        self.symbols = {}

    def entry(self, a, b, c, d, e, alpha, beta, f, mu, nu):
        # Strict-unit associators are canonical identity maps, including
        # multiplicity indices inherited from the non-unit fusion vertex.
        if a == ONE:
            return sp.Integer(e == b and alpha == 0 and f == d and nu == 0 and mu == beta)
        if b == ONE:
            return sp.Integer(e == a and alpha == 0 and f == c and mu == 0 and nu == beta)
        if c == ONE:
            return sp.Integer(e == d and beta == 0 and f == b and mu == 0 and nu == alpha)

        src = []
        for ee in OBJECTS:
            for aa in range(N(a, b, ee)):
                for bb in range(N(ee, c, d)):
                    src.append((ee, aa, bb))
        tgt = []
        for ff in OBJECTS:
            for mm in range(N(b, c, ff)):
                for nn in range(N(a, ff, d)):
                    tgt.append((ff, mm, nn))
        ci = src.index((e, alpha, beta))
        ri = tgt.index((f, mu, nu))
        skey = ((a, b, c, d), ri, ci)
        if skey not in self.symbols:
            self.symbols[skey] = sp.Symbol("F_" + "_".join((a, b, c, d)) + f"_{ri}{ci}")
        return self.symbols[skey]


def reassoc_matrix(source, path, total, leaf_labels, registry):
    target = rotate_right(source, path)

    def sortkey(st):
        return tuple(sorted(st.items()))

    sb = sorted(enum_states(source, leaf_labels, total), key=sortkey)
    tb = sorted(enum_states(target, leaf_labels, total), key=sortkey)
    mat = sp.zeros(len(tb), len(sb))

    pa = path + ("L", "L")
    pb = path + ("L", "R")
    pc = path + ("R",)
    pold = path + ("L",)
    pout = path
    pnew = path + ("R",)

    def leaves(node):
        if isinstance(node, str):
            return frozenset([node])
        return leaves(node[0]) | leaves(node[1])

    local_leafset = leaves(subtree_at(source, path))

    for j, ss in enumerate(sb):
        a = root_label(source, ss, leaf_labels, pa)
        b = root_label(source, ss, leaf_labels, pb)
        c = root_label(source, ss, leaf_labels, pc)
        e, alpha = ss[pold]
        d, beta = ss[pout]
        ssets = leafsets_state(source, ss)

        for i, ts in enumerate(tb):
            tsets = leafsets_state(target, ts)
            common = ssets.keys() & tsets.keys()
            if any(ssets[x] != tsets[x] for x in common if x != local_leafset):
                continue
            f, mu = ts[pnew]
            dd, nu = ts[pout]
            # States with a different local output belong to a different
            # associator block and must be skipped, not asserted equal.
            if dd != d:
                continue
            mat[i, j] = registry.entry(a, b, c, d, e, alpha, beta, f, mu, nu)

    return target, mat


def pentagon(labels, total):
    registry = Registry()
    _, m01 = reassoc_matrix(P0, ("L",), total, labels, registry)
    _, m12 = reassoc_matrix(P1, (), total, labels, registry)
    _, m23 = reassoc_matrix(P2, ("R",), total, labels, registry)
    _, m04 = reassoc_matrix(P0, (), total, labels, registry)
    _, m43 = reassoc_matrix(P4, (), total, labels, registry)
    diff = sp.expand(m23 * m12 * m01 - m43 * m04)
    return registry, (m01, m12, m23, m04, m43), diff
