"""Measure how far *label symmetry alone* reduces the R(2,2) associator problem.

This is a red-team experiment.  It distinguishes two very different ideas:

1. ordinary deduplication of F/pentagon boundary labels under based-ring
   automorphisms;
2. the stronger project goal: solving the monoidal-lift/tensorator coherence
   which couples alpha(F) to the restricted gauge orbit of F.

The first gives only constant-factor reduction and is not considered a
breakthrough.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
from typing import Callable, Dict, Mapping, Tuple

from r22_open_attack import OBJECTS, fusion_R, N

Obj = str


def alpha(x: Obj) -> Obj:
    return {"X": "Y", "Y": "X"}.get(x, x)


def beta(x: Obj) -> Obj:
    return {"g": "k", "k": "g"}.get(x, x)


def fusion_equal_after_map(mapping: Mapping[Obj, Obj]) -> bool:
    fusion = lambda a, b: fusion_R(2, 2, a, b)
    for a, b in product(OBJECTS, repeat=2):
        mapped_product = Counter({mapping[c]: m for c, m in fusion(a, b).items()})
        target = fusion(mapping[a], mapping[b])
        if mapped_product != target:
            return False
    return True


def based_ring_automorphisms() -> Tuple[Dict[Obj, Obj], ...]:
    """COMPUTATIONAL-CLAIM: enumerate all based-ring automorphisms fixing 1."""
    rest = tuple(x for x in OBJECTS if x != "1")
    result = []
    for perm in permutations(rest):
        mapping = {"1": "1", **dict(zip(rest, perm))}
        if fusion_equal_after_map(mapping):
            result.append(mapping)
    return tuple(result)


def f_block_dim(a: Obj, b: Obj, c: Obj, d: Obj) -> int:
    fusion = lambda x, y: fusion_R(2, 2, x, y)
    return sum(N(fusion, a, b, e) * N(fusion, e, c, d) for e in OBJECTS)


def pentagon_dim(a: Obj, b: Obj, c: Obj, d: Obj, target: Obj) -> int:
    fusion = lambda x, y: fusion_R(2, 2, x, y)
    return sum(
        N(fusion, a, b, x) * N(fusion, x, c, y) * N(fusion, y, d, target)
        for x, y in product(OBJECTS, repeat=2)
    )


def orbit_profile(
    tuples_with_dim,
    automorphisms: Tuple[Mapping[Obj, Obj], ...],
):
    lookup = dict(tuples_with_dim)
    seen = set()
    orbit_hist = Counter()
    representative_matrix_entries = 0

    for boundary, dim in tuples_with_dim:
        if boundary in seen:
            continue
        orbit = {
            tuple(mapping[x] for x in boundary)
            for mapping in automorphisms
        }
        assert all(lookup[item] == dim for item in orbit)
        seen.update(orbit)
        orbit_hist[(len(orbit), dim)] += 1
        representative_matrix_entries += dim * dim

    return {
        "orbits": sum(orbit_hist.values()),
        "orbit_size_and_block_dim_histogram": dict(sorted(orbit_hist.items())),
        "representative_matrix_entry_proxy": representative_matrix_entries,
    }


def main() -> None:
    autos = based_ring_automorphisms()
    assert len(autos) == 4

    alpha_map = {x: alpha(x) for x in OBJECTS}
    beta_map = {x: beta(x) for x in OBJECTS}
    assert fusion_equal_after_map(alpha_map)
    assert fusion_equal_after_map(beta_map)

    # The four maps are id, alpha, beta, alpha beta; hence Aut_based(R22)=C2 x C2.
    print("based-ring automorphisms:", len(autos))
    for mapping in autos:
        print(" ", mapping)

    f_blocks = []
    for boundary in product(OBJECTS, repeat=4):
        dim = f_block_dim(*boundary)
        if dim:
            f_blocks.append((boundary, dim))

    pentagon_blocks = []
    for boundary in product(OBJECTS, repeat=5):
        dim = pentagon_dim(*boundary)
        if dim:
            pentagon_blocks.append((boundary, dim))

    identity = {x: x for x in OBJECTS}
    alpha_group = (identity, alpha_map)

    print("\nF blocks: raw", len(f_blocks))
    print("alpha quotient", orbit_profile(f_blocks, alpha_group))
    print("full Aut_based quotient", orbit_profile(f_blocks, autos))

    print("\npentagon blocks: raw", len(pentagon_blocks))
    print("alpha quotient", orbit_profile(pentagon_blocks, alpha_group))
    print("full Aut_based quotient", orbit_profile(pentagon_blocks, autos))

    # Fixed expected values make regressions visible.
    assert orbit_profile(f_blocks, alpha_group)["orbits"] == 232
    assert orbit_profile(f_blocks, alpha_group)["representative_matrix_entry_proxy"] == 1072
    assert orbit_profile(f_blocks, autos)["orbits"] == 152
    assert orbit_profile(f_blocks, autos)["representative_matrix_entry_proxy"] == 944

    assert orbit_profile(pentagon_blocks, alpha_group)["orbits"] == 1712
    assert orbit_profile(pentagon_blocks, alpha_group)["representative_matrix_entry_proxy"] == 42176
    assert orbit_profile(pentagon_blocks, autos)["orbits"] == 1032
    assert orbit_profile(pentagon_blocks, autos)["representative_matrix_entry_proxy"] == 37536


if __name__ == "__main__":
    main()
