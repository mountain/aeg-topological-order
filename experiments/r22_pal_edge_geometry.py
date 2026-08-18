"""Exact projective geometry on the epsilon=-1 D-history chirality field.

This is an auxiliary geometry experiment, not a pentagon proof by itself.
It takes the two four-vertex transport orbits exposed by r22_d_layer_probe.py
and studies a chirality field c_v in {+1,-1} on their K4 history graphs.

Lift vertex chirality to edge relations eta_uv = c_u c_v.  Against the
constant coherent edge predicate 1_E, define the PAL/PCRG-style normalized
projective overlap

    q(c) = |<1_E, eta>|^2 / (||1_E||^2 ||eta||^2).

For K4 this has exactly three values:
  constant chirality     -> 1
  two-plus / two-minus   -> 1/9
  one-plus / three-minus -> 0

Taking min over the two Y-parity transport orbits produces the three-level
geometry underlying the candidate fresh D trace 256 -> 64 -> 4.  The exact
pentagon re-audit remains authoritative for deciding whether that candidate
trace is valid; this file only identifies the geometric encoding once those
stages are declared.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product

from r22_d_layer_probe import transport_orbits
from r22_scale_audit import M


SPACES = [(a, b, c) for a, b, c in product(M, repeat=3)]
SPACE_INDEX = {s: i for i, s in enumerate(SPACES)}
ORBITS = sorted((sorted(comp) for comp in transport_orbits()), key=lambda c: sum(x == "Y" for x in c[0]) % 2)
assert len(ORBITS) == 2 and all(len(c) == 4 for c in ORBITS)


def sign(mask: int, space) -> int:
    return -1 if ((mask >> SPACE_INDEX[space]) & 1) else 1


def orbit_edge_lift(mask: int, orbit) -> tuple[int, ...]:
    c = [sign(mask, v) for v in orbit]
    return tuple(c[i] * c[j] for i, j in combinations(range(4), 2))


def projective_overlap(edge_lift: tuple[int, ...]) -> Fraction:
    # Both vectors have six entries of norm one, so the denominator is 36.
    s = sum(edge_lift)
    return Fraction(s * s, 36)


def score(mask: int) -> Fraction:
    return min(projective_overlap(orbit_edge_lift(mask, o)) for o in ORBITS)


def compressed_stage(mask: int) -> str:
    """Geometry-induced three-level label.

    This is deliberately named compressed_stage rather than verifier_stage:
    the exact D-pentagon trace must be replayed independently.
    """
    q = score(mask)
    return {Fraction(0): "structural", Fraction(1, 9): "amplitude", Fraction(1): "survivor"}[q]


def main():
    q_counts = Counter(score(mask) for mask in range(256))
    stage_counts = Counter(compressed_stage(mask) for mask in range(256))
    survivors = [mask for mask in range(256) if score(mask) == 1]

    print("spaces in bit order:", SPACES)
    print("transport orbits:")
    for orbit in ORBITS:
        print(" ", orbit)
    print("projective-overlap counts:", dict(q_counts))
    print("compressed stage counts:", dict(stage_counts))
    print("q=1 masks:", survivors)

    assert q_counts == Counter({Fraction(0): 192, Fraction(1, 9): 60, Fraction(1): 4})
    assert survivors == [0, 105, 150, 255]
    assert stage_counts == Counter({"structural": 192, "amplitude": 60, "survivor": 4})

    print("RESULT: edge-relation projective geometry exactly separates 192 / 60 / 4 chirality classes")
    print("BOUNDARY: this is a representation theorem for the candidate D-stage partition, not a substitute for exact pentagon replay")


if __name__ == "__main__":
    main()
