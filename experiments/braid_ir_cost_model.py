"""Cost model: explicit F/R history IR versus precompiled fusion-path blocks.

The point is deliberately red-team: once a local generator has been compiled,
a direct 2x2 block is cheaper to execute than replaying F -> R -> F^{-1}.
Both representations can share templates, so certificate metadata is O(number
of local blocks) in either case.  This suggests a two-level architecture:

    auditable history/proof IR -> optimized categorical execution IR.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from braid_sparsity_baseline import ONE, TAU, generator_block_profile


@dataclass(frozen=True)
class Cost:
    multiplications: int
    additions: int
    block_refs: int


def direct_execution_cost(n: int, total: str, i: int) -> Cost:
    """Precompiled local scalar/2x2 block applied once to a vector."""
    p = generator_block_profile(n, total, i)
    one = p["one_blocks"]
    two = p["two_blocks"]
    # scalar block: 1 multiply; dense 2x2 block: 4 multiplies + 2 additions.
    return Cost(one + 4 * two, 2 * two, one + two)


def history_replay_cost(n: int, total: str, i: int) -> Cost:
    """Replay primitive local history F -> R -> F^{-1} for each 2-block."""
    p = generator_block_profile(n, total, i)
    one = p["one_blocks"]
    two = p["two_blocks"]
    if i == 1:
        return Cost(one, 0, one)
    # Per 2-block: F (4M,2A), diagonal R (2M), F^{-1} (4M,2A).
    return Cost(one + 10 * two, 4 * two, one + two)


def compare(n: int, total: str, i: int) -> Dict[str, int | float]:
    direct = direct_execution_cost(n, total, i)
    history = history_replay_cost(n, total, i)
    return {
        "direct_mult": direct.multiplications,
        "history_mult": history.multiplications,
        "direct_add": direct.additions,
        "history_add": history.additions,
        "direct_block_refs": direct.block_refs,
        "history_block_refs": history.block_refs,
        "mult_ratio": history.multiplications / direct.multiplications,
    }


def verify_no_metadata_asymptotic_gain(max_n: int = 16) -> None:
    for n in range(3, max_n + 1):
        for total in (ONE, TAU):
            for i in range(1, n):
                direct = direct_execution_cost(n, total, i)
                history = history_replay_cost(n, total, i)
                # With shared global templates, both need one reference per
                # local block.  History does not compress this further.
                assert direct.block_refs == history.block_refs
                # Replaying the primitive path is never cheaper after a direct
                # block has already been compiled.
                assert direct.multiplications <= history.multiplications
                assert direct.additions <= history.additions


def main() -> None:
    verify_no_metadata_asymptotic_gain()
    print("two-level IR red-team checks: PASS")
    for n in (6, 10, 14):
        # Pick an interior generator with nontrivial 2x2 blocks.
        i = max(2, n // 2)
        print(f"n={n}, total=tau, sigma_{i}: {compare(n, TAU, i)}")


if __name__ == "__main__":
    main()
