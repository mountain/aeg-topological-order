"""Structure of the X<->Y swap lift for the unresolved ring R(2,2).

The aim is not to solve the associator yet.  We identify which fusion-space
vertices are fixed by the ring involution alpha and which occur in free C2
orbits.  Free orbits can absorb tensorator matrices by paired basis choices;
fixed vertices are where genuine C2 coherence data can survive.

We also verify the group-theoretic kernel constraint for the conditional
near-group equivariantization with invertible group C4 x C2.

Labels:
- CLASSICAL: elementary fusion-space and group-action facts.
- COMPUTATIONAL-CLAIM: finite enumeration performed here.
- CANDIDATE-NEW: use of this fixed-locus reduction as the front end of the
  R(2,2) categorification attack.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from typing import Dict, Iterable, Mapping, Tuple

from r22_open_attack import OBJECTS, fusion_R

Obj = str
Triple = Tuple[Obj, Obj, Obj]


def alpha(x: Obj) -> Obj:
    return {"X": "Y", "Y": "X"}.get(x, x)


def multiplicity(a: Obj, b: Obj, c: Obj) -> int:
    return fusion_R(2, 2, a, b).get(c, 0)


def fusion_vertices(strict_unit: bool = False) -> Tuple[Tuple[Triple, int], ...]:
    result = []
    for a, b, c in product(OBJECTS, repeat=3):
        n = multiplicity(a, b, c)
        if not n:
            continue
        if strict_unit and (a == "1" or b == "1"):
            continue
        result.append(((a, b, c), n))
    return tuple(result)


def orbit_decomposition(strict_unit: bool = False) -> Dict[str, object]:
    vertices = dict(fusion_vertices(strict_unit))
    seen = set()
    fixed = []
    free = []

    for triple, n in vertices.items():
        if triple in seen:
            continue
        image = tuple(alpha(x) for x in triple)
        assert vertices[image] == n
        if image == triple:
            fixed.append((triple, n))
            seen.add(triple)
        else:
            free.append((tuple(sorted((triple, image))), n))
            seen.add(triple)
            seen.add(image)

    return {
        "vertices": len(vertices),
        "multiplicity_histogram": dict(sorted(Counter(vertices.values()).items())),
        "fixed_orbits": tuple(sorted(fixed)),
        "free_orbits": tuple(sorted(free)),
        "fixed_count": len(fixed),
        "free_orbit_count": len(free),
    }


def fixed_locus_is_pointed() -> bool:
    data = orbit_decomposition(strict_unit=True)
    return all(all(x in ("1", "g", "h", "k") for x in triple) for triple, _ in data["fixed_orbits"])


def multiplicity_two_vertices_are_free() -> bool:
    data = orbit_decomposition(strict_unit=True)
    for triple, n in data["fixed_orbits"]:
        if n == 2:
            return False
    return all(n == 2 for _, n in data["free_orbits"] if n == 2)


# ----- C4 x C2 kernel calculation ---------------------------------------

C4xC2Element = Tuple[int, int]  # first coordinate mod 4, second mod 2


def add_G(x: C4xC2Element, y: C4xC2Element) -> C4xC2Element:
    return ((x[0] + y[0]) % 4, (x[1] + y[1]) % 2)


def subgroup_generated(z: C4xC2Element) -> Tuple[C4xC2Element, ...]:
    current = (0, 0)
    result = []
    while current not in result:
        result.append(current)
        current = add_G(current, z)
    return tuple(result)


def order_two_elements() -> Tuple[C4xC2Element, ...]:
    elements = ((a, b) for a in range(4) for b in range(2))
    return tuple(
        x for x in elements
        if x != (0, 0) and add_G(x, x) == (0, 0)
    )


def quotient_cosets(kernel_generator: C4xC2Element):
    H = set(subgroup_generated(kernel_generator))
    elements = {(a, b) for a in range(4) for b in range(2)}
    cosets = []
    unseen = set(elements)
    while unseen:
        x = min(unseen)
        coset = frozenset(add_G(x, h) for h in H)
        cosets.append(coset)
        unseen -= set(coset)
    return tuple(cosets)


def quotient_type(kernel_generator: C4xC2Element) -> str:
    cosets = quotient_cosets(kernel_generator)
    zero = next(c for c in cosets if (0, 0) in c)

    def qadd(A, B):
        x = next(iter(A))
        y = next(iter(B))
        z = add_G(x, y)
        return next(c for c in cosets if z in c)

    order_hist = Counter()
    for A in cosets:
        current = zero
        for n in range(1, 9):
            current = qadd(current, A)
            if current == zero:
                order_hist[n] += 1
                break
    signature = tuple(sorted(order_hist.items()))
    if signature == ((1, 1), (2, 3)):
        return "V4"
    if signature == ((1, 1), (2, 1), (4, 2)):
        return "C4"
    raise AssertionError(signature)


def c4xc2_kernel_profile() -> Dict[C4xC2Element, str]:
    return {z: quotient_type(z) for z in order_two_elements()}


def main() -> None:
    all_data = orbit_decomposition(strict_unit=False)
    strict_data = orbit_decomposition(strict_unit=True)

    print("all nonzero fusion vertices:")
    print("  count", all_data["vertices"])
    print("  multiplicities", all_data["multiplicity_histogram"])
    print("  fixed", all_data["fixed_count"])
    print("  free C2 orbits", all_data["free_orbit_count"])

    print("\nstrict-unit-reduced fusion vertices:")
    print("  count", strict_data["vertices"])
    print("  multiplicities", strict_data["multiplicity_histogram"])
    print("  fixed", strict_data["fixed_count"])
    print("  free C2 orbits", strict_data["free_orbit_count"])
    print("  fixed locus", strict_data["fixed_orbits"])

    assert all_data["vertices"] == 48
    assert all_data["multiplicity_histogram"] == {1: 40, 2: 8}
    assert strict_data["vertices"] == 37
    assert strict_data["multiplicity_histogram"] == {1: 29, 2: 8}
    assert strict_data["fixed_count"] == 9
    assert strict_data["free_orbit_count"] == 14
    assert fixed_locus_is_pointed()
    assert multiplicity_two_vertices_are_free()

    expected_fixed = {
        (("g", "g", "1"), 1),
        (("g", "h", "k"), 1),
        (("g", "k", "h"), 1),
        (("h", "g", "k"), 1),
        (("h", "h", "1"), 1),
        (("h", "k", "g"), 1),
        (("k", "g", "h"), 1),
        (("k", "h", "g"), 1),
        (("k", "k", "1"), 1),
    }
    assert set(strict_data["fixed_orbits"]) == expected_fixed

    print("\nC4 x C2 order-two kernels:")
    kernels = c4xc2_kernel_profile()
    for z, quotient in sorted(kernels.items()):
        print(" ", z, "->", quotient)
    assert kernels == {(0, 1): "C4", (2, 0): "V4", (2, 1): "C4"}
    print("unique kernel giving V4 quotient: (2,0) = square of the C4 generator")


if __name__ == "__main__":
    main()
