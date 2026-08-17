"""Specialized center/FS arithmetic for the open R(2,2) problem.

This file specializes Meng--Yu Section 3 to m=n=2 and adds two elementary
constraints that are easy to lose in the general asymptotic argument:

1. exact parity/minimum information for the induction multiplicities;
2. Galois triangle bounds for the weighted root-of-unity sum.

Together with Larson's lower bound for expressing a+b*sqrt(c) as a sum of
roots of unity, the nu_2(g)=nu_2(gh)=+1 branch is sharpened as follows:

  - Delta=+2 dim(C) is impossible;
  - Delta=0 is impossible;
  - only Delta=-2 dim(C) survives;
  - hence nu_2(X)=nu_2(Y)=-1 in this pointed-indicator branch;
  - S=sum_s (z_s+z'_s)^2 must be one of 34,36,38,40,42,44,46.

The script does NOT yet prove non-categorifiability.  It produces the finite
candidate set for the next integer/cyclotomic solver.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from math import prod
from typing import Dict, Iterable, Tuple

import sympy as sp

sqrt6 = sp.sqrt(6)
d = 2 + sqrt6
DIM = 24 + 8 * sqrt6
M_PLUS_N = 4


def compositions(total: int, length: int) -> Iterable[Tuple[int, ...]]:
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def z_pair_square_upper_bound() -> int:
    # Meng--Yu Proposition 3.11:
    # S <= 16 + 15/8 (m+n)^2 = 46 for m+n=4.
    value = sp.Integer(16) + sp.Rational(15, 8) * M_PLUS_N**2
    assert value == 46
    return int(value)


def pair_sum_square_distribution() -> Counter[int]:
    """Enumerate t_i=x_i+y_i for i=6,...,19 using only their forced sums.

    For m=n=2, Meng--Yu's linear constraints imply

      sum_{6..9} t_i = 4,
      sum_{10..11} t_i = 4,
      sum_{12..15} t_i = 4,
      sum_{16..19} t_i = 4.

    Let P=sum_{6..19} t_i^2.  Equation (3.19) is P+S=66.
    """
    A = tuple(compositions(4, 4))
    B = tuple(compositions(4, 2))
    dist: Counter[int] = Counter()
    for a, b, c, e in product(A, B, A, A):
        P = sum(x * x for x in a + b + c + e)
        dist[P] += 1
    return dist


def possible_S_from_induction() -> Tuple[int, ...]:
    dist = pair_sum_square_distribution()
    out = tuple(sorted(66 - P for P in dist if 0 <= 66 - P <= z_pair_square_upper_bound()))
    assert all(S % 2 == 0 for S in out)
    assert max(out) == 46
    return out


def root_sum_target(S: int, Delta: sp.Expr) -> sp.Expr:
    """Meng--Yu Eq. (3.21), solved for sum theta_s^2 w_s^2.

    w_s=z_s+z'_s and S=sum w_s^2.
    For m+n=4:

      -sum theta_s^2 w_s^2 = 80 + (Delta+32)/d - S.
    """
    return sp.expand(sp.simplify(S - 80 - (Delta + 32) / d))


def quadratic_coefficients(expr: sp.Expr, S_symbol: sp.Symbol) -> Tuple[sp.Expr, sp.Expr]:
    """Return a,b for expr=a+b*sqrt(6), allowing a to depend on S."""
    expanded = sp.expand(expr)
    b = sp.expand(expanded.coeff(sqrt6))
    a = sp.expand(expanded - b * sqrt6)
    return a, b


def larson_min_root_count(b: int) -> int:
    """Larson Theorem 1.3: n >= |b| phi(2c), c=6."""
    return abs(b) * int(sp.totient(12))


def galois_triangle_ok(S: int, a: sp.Expr, b: int) -> bool:
    """Every embedding sends each root of unity to unit modulus.

    If S roots sum to a+b*sqrt(6), both real quadratic conjugates must have
    absolute value at most S.
    """
    vals = [sp.Abs(a + b * sqrt6), sp.Abs(a - b * sqrt6)]
    return all(bool(sp.N(v) <= S) for v in vals)


def positive_pointed_indicator_branches() -> Dict[str, Dict[str, object]]:
    """Analyze nu_2(g)=nu_2(gh)=+1 via Eq. (3.21)."""
    Ssym = sp.Symbol("S", integer=True, nonnegative=True)
    deltas = {
        "both_XY_negative": -2 * DIM,
        "opposite_XY_indicators": sp.Integer(0),
        "both_XY_positive": 2 * DIM,
    }
    possible_induction_S = set(possible_S_from_induction())
    report: Dict[str, Dict[str, object]] = {}

    for name, Delta in deltas.items():
        expr = root_sum_target(Ssym, Delta)
        a, b_expr = quadratic_coefficients(expr, Ssym)
        b = int(b_expr)
        min_roots = larson_min_root_count(b)

        survivors = []
        for S in sorted(possible_induction_S):
            if S < min_roots:
                continue
            ai = sp.expand(a.subs(Ssym, S))
            if galois_triangle_ok(S, ai, b):
                survivors.append(S)

        report[name] = {
            "Delta": sp.expand(Delta),
            "root_sum": expr,
            "sqrt6_coefficient": b,
            "Larson_min_roots": min_roots,
            "surviving_S": tuple(survivors),
        }

    assert report["both_XY_positive"]["surviving_S"] == ()
    assert report["opposite_XY_indicators"]["surviving_S"] == ()
    assert report["both_XY_negative"]["surviving_S"] == (34, 36, 38, 40, 42, 44, 46)
    return report


def high_S_pair_profiles() -> Dict[int, int]:
    """Number of ordered t_i profiles surviving for each final S candidate."""
    dist = pair_sum_square_distribution()
    result = {S: dist[66 - S] for S in positive_pointed_indicator_branches()["both_XY_negative"]["surviving_S"]}
    assert result[46] == 1
    assert result[44] == 38
    return result


def main() -> None:
    print("R(2,2) center arithmetic")
    print("  d =", d)
    print("  dim(C) =", DIM)
    print("  Meng--Yu bound S <=", z_pair_square_upper_bound())
    print("  induction-compatible S values:", possible_S_from_induction())

    print("\nnu2(g)=nu2(gh)=+1 branch")
    for name, data in positive_pointed_indicator_branches().items():
        print(" ", name)
        for key, value in data.items():
            print(f"    {key}: {value}")

    print("\nremaining t_i profile counts by S")
    for S, count in high_S_pair_profiles().items():
        print(f"  S={S}: {count}")

    print("\nCOMPUTATIONAL-CLAIM:")
    print("  in the +1 pointed-indicator branch, only nu2(X)=nu2(Y)=-1 survives")
    print("  next solver only needs S in {34,36,38,40,42,44,46}")


if __name__ == "__main__":
    main()
