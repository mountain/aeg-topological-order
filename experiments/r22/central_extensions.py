"""Central extensions 1 -> C2 -> Gtilde -> V4 -> 1 relevant to R(2,2).

If the based-ring involution tau lifts to a monoidal Z2 action, then
C^{Z2} has eight invertible simples. Their group maps onto V4 with kernel the
two characters of Z2. Since Aut(C2) is trivial, this is a central extension.
This script enumerates H^2(V4,C2) exactly and classifies the possible groups.

No categorical lift of tau is assumed or proved here.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Dict, Tuple

V4 = tuple(product((0, 1), repeat=2))
ZERO = (0, 0)
Elt = Tuple[int, int]
Cocycle = Tuple[int, ...]
PAIRS = tuple((a, b) for a in V4 for b in V4 if a != ZERO and b != ZERO)


def add(a: Elt, b: Elt) -> Elt:
    return (a[0] ^ b[0], a[1] ^ b[1])


def cocycle_from_bits(bits: Cocycle) -> Dict[Tuple[Elt, Elt], int]:
    f = {(a, b): 0 for a in V4 for b in V4}
    for pair, bit in zip(PAIRS, bits):
        f[pair] = bit
    return f


def is_cocycle(f: Dict[Tuple[Elt, Elt], int]) -> bool:
    for a, b, c in product(V4, repeat=3):
        if (f[b, c] ^ f[a, add(b, c)]) != (f[a, b] ^ f[add(a, b), c]):
            return False
    return True


def encode(f: Dict[Tuple[Elt, Elt], int]) -> Cocycle:
    return tuple(f[p] for p in PAIRS)


def normalized_cocycles() -> Tuple[Cocycle, ...]:
    out = []
    for bits in product((0, 1), repeat=len(PAIRS)):
        if is_cocycle(cocycle_from_bits(bits)):
            out.append(bits)
    assert len(out) == 16
    return tuple(out)


def coboundary(q: Dict[Elt, int]) -> Cocycle:
    f = {(a, b): q[a] ^ q[b] ^ q[add(a, b)] for a in V4 for b in V4}
    return encode(f)


def normalized_coboundaries() -> Tuple[Cocycle, ...]:
    out = set()
    nonzero = tuple(a for a in V4 if a != ZERO)
    for values in product((0, 1), repeat=3):
        q = {ZERO: 0}
        q.update(dict(zip(nonzero, values)))
        out.add(coboundary(q))
    assert len(out) == 2
    return tuple(sorted(out))


def xor_cocycles(a: Cocycle, b: Cocycle) -> Cocycle:
    return tuple(x ^ y for x, y in zip(a, b))


def cohomology_classes() -> Tuple[Tuple[Cocycle, ...], ...]:
    z2 = set(normalized_cocycles())
    b2 = normalized_coboundaries()
    classes = []
    while z2:
        rep = min(z2)
        cls = tuple(sorted(xor_cocycles(rep, b) for b in b2))
        classes.append(cls)
        z2.difference_update(cls)
    assert len(classes) == 8
    assert all(len(c) == 2 for c in classes)
    return tuple(classes)


ExtElt = Tuple[Elt, int]


def extension_elements() -> Tuple[ExtElt, ...]:
    return tuple((a, u) for a in V4 for u in (0, 1))


def multiply(f: Dict[Tuple[Elt, Elt], int], x: ExtElt, y: ExtElt) -> ExtElt:
    a, u = x
    b, v = y
    return (add(a, b), u ^ v ^ f[a, b])


def element_order(f: Dict[Tuple[Elt, Elt], int], x: ExtElt) -> int:
    identity = (ZERO, 0)
    y = identity
    for n in range(1, 9):
        y = multiply(f, y, x)
        if y == identity:
            return n
    raise AssertionError("order > 8 in a group of order 8")


def classify_extension(cocycle: Cocycle) -> str:
    f = cocycle_from_bits(cocycle)
    elems = extension_elements()
    for x, y, z in product(elems, repeat=3):
        assert multiply(f, multiply(f, x, y), z) == multiply(f, x, multiply(f, y, z))

    abelian = all(multiply(f, x, y) == multiply(f, y, x) for x, y in product(elems, repeat=2))
    orders = Counter(element_order(f, x) for x in elems)
    if abelian and orders == Counter({2: 7, 1: 1}):
        return "C2^3"
    if abelian and orders == Counter({4: 4, 2: 3, 1: 1}):
        return "C4xC2"
    if not abelian and orders == Counter({2: 5, 4: 2, 1: 1}):
        return "D8"
    if not abelian and orders == Counter({4: 6, 2: 1, 1: 1}):
        return "Q8"
    raise AssertionError((abelian, orders))


def extension_class_distribution() -> Counter[str]:
    dist: Counter[str] = Counter()
    for cls in cohomology_classes():
        kinds = {classify_extension(c) for c in cls}
        assert len(kinds) == 1
        dist[kinds.pop()] += 1
    expected = Counter({"C4xC2": 3, "D8": 3, "C2^3": 1, "Q8": 1})
    assert dist == expected
    return dist


def main() -> None:
    print("normalized 2-cocycles:", len(normalized_cocycles()))
    print("normalized 2-coboundaries:", len(normalized_coboundaries()))
    print("H^2(V4,C2) classes:", len(cohomology_classes()))
    print("extension-group distribution:")
    for group, count in sorted(extension_class_distribution().items()):
        print(f"  {group}: {count}")


if __name__ == "__main__":
    main()
