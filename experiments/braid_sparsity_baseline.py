"""Direct fusion-path baseline for Fibonacci braid generators.

This file is intentionally independent of the history-graph bookkeeping.  It
asks two red-team questions:

1. Does the Artin braid relation alone determine the R-symbols?  No.
2. Does the explicit-history compiler obtain a sparsity advantage unavailable
   to an optimized categorical fusion-path implementation?  At this benchmark,
   no: both have the same 1x1/2x2 block locality and O(d) nonzeros per generator.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Tuple

import sympy as sp

ONE = "1"
TAU = "t"
alpha, s, r1, rt = sp.symbols("alpha s r1 rt", nonzero=True)


def fuse(a: str, b: str) -> Tuple[str, ...]:
    if a == ONE:
        return (b,)
    if b == ONE:
        return (a,)
    return (ONE, TAU)


def fusion_paths(n: int, total: str) -> List[Tuple[str, ...]]:
    """Charges q_1,...,q_n in the left-comb fusion-path basis, q_1=tau."""
    if n < 1:
        raise ValueError(n)
    paths = [(TAU,)]
    for _ in range(2, n + 1):
        paths = [path + (out,) for path in paths for out in fuse(path[-1], TAU)]
    return [path for path in paths if path[-1] == total]


def generator_block_profile(n: int, total: str, i: int) -> Dict[str, int]:
    """Block/nnz profile of sigma_i, 1 <= i < n, without materializing it."""
    if not (1 <= i < n):
        raise ValueError((n, i))
    paths = fusion_paths(n, total)
    dimension = len(paths)

    if i == 1:
        return {
            "dimension": dimension,
            "one_blocks": dimension,
            "two_blocks": 0,
            "nnz": dimension,
            "dense_entries": dimension * dimension,
        }

    # sigma_i only mixes q_i while q_{i-1}, q_{i+1}, and all other path
    # charges are fixed.  Hence every local block has size at most two.
    q_i_index = i - 1
    groups: Dict[Tuple[str, ...], int] = {}
    for path in paths:
        key = path[:q_i_index] + path[q_i_index + 1 :]
        groups[key] = groups.get(key, 0) + 1

    sizes = Counter(groups.values())
    assert set(sizes) <= {1, 2}
    one_blocks = sizes[1]
    two_blocks = sizes[2]
    nnz = one_blocks + 4 * two_blocks
    assert dimension == one_blocks + 2 * two_blocks
    assert nnz == dimension + 2 * two_blocks
    assert nnz <= 2 * dimension

    return {
        "dimension": dimension,
        "one_blocks": one_blocks,
        "two_blocks": two_blocks,
        "nnz": nnz,
        "dense_entries": dimension * dimension,
    }


def fibonacci_dimensions(max_n: int = 14) -> List[Tuple[int, int, int]]:
    """Return (n, dim total=1, dim total=tau); these follow Fibonacci numbers."""
    return [(n, len(fusion_paths(n, ONE)), len(fusion_paths(n, TAU))) for n in range(2, max_n + 1)]


def braid_relation_only_factor() -> sp.Expr:
    """Show that Yang--Baxter/Artin alone is weaker than the hexagon system.

    On the three-tau total-tau sector use F=[[a,s],[s,-a]],
    D=diag(r1,rt), sigma1=D, sigma2=F D F.  Reduce the matrix braid relation
    modulo only the frozen F-relations a^2+a-1=0 and s^2=a.

    Every nonzero entry has a common factor (r1-rt)*Q.  In particular the
    branch r1=rt satisfies the braid relation but not the Fibonacci hexagon
    ideal, so braid-group representation consistency alone cannot reconstruct
    the braided fusion structure.
    """
    F = sp.Matrix([[alpha, s], [s, -alpha]])
    D = sp.diag(r1, rt)
    sigma1 = D
    sigma2 = F * D * F
    residual = sigma1 * sigma2 * sigma1 - sigma2 * sigma1 * sigma2

    Gf = sp.groebner([alpha**2 + alpha - 1, s**2 - alpha], r1, rt, s, alpha, order="lex")
    reduced = [sp.factor(Gf.reduce(sp.expand(entry))[1]) for entry in residual if entry != 0]
    reduced = [entry for entry in reduced if entry != 0]
    assert reduced

    Q = (2 * alpha - 1) * (r1**2 + rt**2) + (2 - 3 * alpha) * r1 * rt
    for entry in reduced:
        quotient = sp.factor(entry / ((r1 - rt) * Q))
        assert quotient in (1, -1, s, -s)
    return sp.factor((r1 - rt) * Q)


def verify_linear_sparsity(max_n: int = 14) -> None:
    for n in range(3, max_n + 1):
        for total in (ONE, TAU):
            for i in range(1, n):
                profile = generator_block_profile(n, total, i)
                assert profile["nnz"] <= 2 * profile["dimension"]


def main() -> None:
    print("braid-relation-only common factor:")
    print(" ", braid_relation_only_factor())

    print("\nfusion-space dimensions:")
    for row in fibonacci_dimensions():
        print(" ", row)

    verify_linear_sparsity()
    print("\nlinear sparsity bound: PASS")

    print("\nselected total-tau generator profiles:")
    for n in (4, 6, 8, 10, 12, 14):
        dim = len(fusion_paths(n, TAU))
        profiles = [generator_block_profile(n, TAU, i) for i in range(1, n)]
        max_nnz = max(p["nnz"] for p in profiles)
        print(f"  n={n}: d={dim}, max_nnz={max_nnz}, dense={dim*dim}")


if __name__ == "__main__":
    main()
