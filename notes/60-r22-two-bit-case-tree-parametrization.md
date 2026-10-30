# R(2,2) theorem audit — two-bit parametrisation of the scalar quotient and the singularity/winding dichotomy

**Status:** `REFORMULATION + COMPUTATIONAL-CLAIM` — replaces two hardcoded lists with a derived
criterion; changes no verdict and no certificate.

This note records a structural clarification of the finite case tree.  It removes two literal
lists, identifies the scalar that controls the shallow/deep split, and states the obstruction
dichotomy that the leaf census `12 + 32 = 44` has been encoding without saying so.

---

## 1. What was frozen

`experiments/r22_epsminus_shallow_local_f_obstruction.py` split the `ε = −1` scalar components by
two literals with no stated reason:

```python
SHALLOW = (4, 6, 12, 14)      # det(F^{XXX}_X) identically zero
DEEP    = (5, 7, 13, 15)      # det(F^{XXX}_X) nonzero, survive to Phase 5
```

By contrast `ε` itself was already derived, as the sign of one scalar:

```python
EPS_INDEX = SC_INDEX[("h", "X", "h", "X")]
EPS_PLUS  = [i for i, r in enumerate(COMPONENT_REPS) if ((r >> EPS_INDEX) & 1) == 0]
```

So of the two bits that organise the case tree, one was derived and the other was a magic list.

## 2. The missing bit is also a single scalar sign

Each scalar component is a 153-bit vector over `SC_KEYS`.  Define

\[
\chi(c)=\operatorname{sign}\big(\text{scalar at key }(X,X,h,1)\big)\in\{\pm1\}.
\]

Then exactly

\[
\boxed{\ \text{shallow}\iff \varepsilon=-1\ \text{and}\ \chi=+1,\qquad
        \text{deep}\iff \varepsilon=-1\ \text{and}\ \chi=-1\ }
\]

This is not an artefact of one key: a search over all 153 scalars finds **eight** with the
identical separator,

\[
(X,X,h,1),\ (X,X,h,h),\ (X,Y,h,g),\ (X,Y,h,k),\ (Y,X,h,g),\ (Y,X,h,k),\ (Y,Y,h,1),\ (Y,Y,h,h),
\]

in two orbits of four.  The code now asserts that each of the eight reproduces the same partition.

## 3. The two-bit criterion

\[
\boxed{\ \det\!\big(F^{XXX}_X\big)\equiv0\iff \varepsilon=+1\ \ \text{or}\ \ \chi=+1\ }
\]

| class | count | fate | mechanism |
| :--- | ---: | :--- | :--- |
| `ε = +1` (any `χ`) | 8 | killed at local-F | block forced singular |
| `ε = −1`, `χ = +1` | 4 | killed at local-F | block forced singular |
| `ε = −1`, `χ = −1` | 4 | survives to Phase 5 | ratio system infeasible |

`ε` and `χ` are **independent** (all four sign combinations occur among the 16 components), so the
parametrisation is genuinely two bits and not one bit twice.

## 4. The 44 leaves, and the dichotomy

| bits | factor | leaves | obstruction |
| :--- | :--- | ---: | :--- |
| `ε = +1` | `8 × 1` | 8 | **singularity** |
| `ε = −1, χ = +1` | `4 × 1` | 4 | **singularity** |
| `ε = −1, χ = −1` | `4 × 4 masks × 2 D classes` | 32 | **winding** |
| | | **44** | |

The two obstruction types are dual in kind:

* **SINGULARITY** (12 leaves) — a block that pentagon coherence requires to be **invertible** is
  forced **singular**.  A multiplicative/rank obstruction, certified by the determinant polynomial
  vanishing identically.
* **WINDING** (32 leaves) — a system of amplitude **ratios** that must be consistent is
  infeasible.  An additive/holonomy obstruction, certified at Phase 5 by a circulation whose
  holonomy is non-trivial.

`χ` is a `Z/2` datum — rank one, the cheapest possible invariant — while the deep obstruction is a
`Z/4` cycle holonomy.  **The whole case tree is therefore organised by two `Z/2` signs, and the
only `Z/4` structure in the theorem lives on the 32-leaf deep frontier.**

## 5. What changed in the repository

1. `experiments/r22_epsminus_shallow_local_f_obstruction.py`
   `SHALLOW` and `DEEP` are now **derived** as `{c ∈ ε−1 : χ(c) = +1}` and `{c ∈ ε−1 : χ(c) = −1}`.
   The historical tuples are retained but only as regression assertions, so the file fails loudly if
   the derivation and the frozen lists ever disagree.  `CHI_KEY`, `CHI_EQUIVALENT_KEYS`, `chi()`
   and `EPS_MINUS` are exported.
2. `experiments/r22_theorem_case_ledger.py`
   The parametrisation is now **executable**: the ledger asserts that `ε₊`, `SHALLOW`, `DEEP` are
   disjoint and cover all 16 components, that `χ` is constant `+1`/`−1` on them as claimed, that the
   two bits are independent, that `OBSTRUCTION[c] ∈ {singularity, winding}`, and that
   `12 + 32 = 44`.
3. This note.

Nothing about any certificate, any mask, any D class or any leaf changed.  `r22_theorem_case_ledger.py`
replays to the identical `44`-leaf result, and
`r22_epsminus_shallow_local_f_obstruction.py` replays to the identical verdict
(components 4,6,12,14 obstructed for all 64 canonical Clifford patterns; the 16 deep Phase-1
survivors remain locally invertible).

## 6. Boundary

This is a **bookkeeping and derivation** improvement, not new mathematics about the theorem:

* it does not shorten the proof;
* it does not re-prove the determinant identities — those come from the frozen gates, which are
  replayed above and unchanged;
* it changes no verdict.

Its value is that the two bits are now named, derived and asserted rather than half-remembered, and
that the `12 / 32` split is stated as a dichotomy of obstruction kinds instead of a leaf count.

## 7. Reproduce

```bash
cd ~/AEG/aeg-topological-order/experiments
python3 r22_theorem_case_ledger.py                      # 44 leaves, now with the two-bit assertions
python3 r22_epsminus_shallow_local_f_obstruction.py     # shallow obstructed / deep control invertible
```
