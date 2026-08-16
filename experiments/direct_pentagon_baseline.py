"""Independent direct categorical baseline for the blind Fibonacci pentagon.

This file intentionally does not import fibonacci_pentagon.py. It implements
only the multiplicity-free fusion grammar, strict-unit F data, and the standard
pentagon coefficient identity. The purpose is to compare the algebraic system
produced by a direct categorical formulation with the sparse history-complex
formulation, not to supply known Fibonacci values.
"""

from itertools import product
import sympy as sp

ONE, TAU = "1", "t"
LABELS = (ONE, TAU)
a, b, c, d, g = sp.symbols("a b c d g")
TABLE = {(ONE, ONE): a, (ONE, TAU): b, (TAU, ONE): c, (TAU, TAU): d}


def fuse(x, y):
    if x == ONE:
        return (y,)
    if y == ONE:
        return (x,)
    if x == TAU and y == TAU:
        return (ONE, TAU)
    raise ValueError((x, y))


def F(x, y, z, out, old, new):
    """Coefficient [F_out^{xyz}]_{old,new}; zero if either tree is inadmissible."""
    if old not in fuse(x, y):
        return sp.Integer(0)
    if out not in fuse(old, z):
        return sp.Integer(0)
    if new not in fuse(y, z):
        return sp.Integer(0)
    if out not in fuse(x, new):
        return sp.Integer(0)
    if ONE in (x, y, z):
        return sp.Integer(1)
    if out == ONE:
        return g if old == TAU and new == TAU else sp.Integer(0)
    if out == TAU:
        return TABLE[(old, new)]
    return sp.Integer(0)


def globally_admissible(values):
    """Boundary data for a four-object pentagon.

    values = (A,B,C,D,E,F,G,K,L) with source history
      (((A B)_F C)_G D)_E
    and target history
      (A (B (C D)_L)_K)_E.
    """
    A, B, C, D, E, FF, G, K, L = values
    return (
        FF in fuse(A, B)
        and G in fuse(FF, C)
        and E in fuse(G, D)
        and L in fuse(C, D)
        and K in fuse(B, L)
        and E in fuse(A, K)
    )


def pentagon_polynomial(values):
    """CLASSICAL: direct coefficient pentagon, short path minus long path."""
    A, B, C, D, E, FF, G, K, L = values
    short = F(FF, C, D, E, G, L) * F(A, B, L, E, FF, K)
    long = sp.Integer(0)
    for H in LABELS:
        long += (
            F(A, B, C, G, FF, H)
            * F(A, H, D, E, G, K)
            * F(B, C, D, K, H, L)
        )
    return sp.factor(sp.expand(short - long))


def canonical_up_to_sign(expr):
    poly = sp.Poly(sp.expand(expr), a, b, c, d, g)
    _content, primitive = poly.primitive()
    expr = sp.expand(primitive.as_expr())
    terms = sp.Poly(expr, a, b, c, d, g).terms()
    if terms and terms[0][1] < 0:
        expr = -expr
    return sp.factor(expr)


def equation_system():
    admissible = [v for v in product(LABELS, repeat=9) if globally_admissible(v)]
    raw = []
    for values in admissible:
        polynomial = pentagon_polynomial(values)
        if polynomial != 0:
            raw.append(polynomial)
    unique = []
    for polynomial in raw:
        normalized = canonical_up_to_sign(polynomial)
        if normalized not in unique:
            unique.append(normalized)
    return admissible, raw, unique


def main():
    admissible, raw, unique = equation_system()
    print("globally admissible boundary configurations:", len(admissible))
    print("nonzero polynomial instances:", len(raw))
    print("unique polynomials up to sign:", len(unique))
    for polynomial in unique:
        print(polynomial, "= 0")

    assert len(admissible) == 50
    assert len(raw) == 13
    assert len(unique) == 12


if __name__ == "__main__":
    main()
