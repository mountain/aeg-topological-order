# R(2,2) complete research schedule

**Status:** `RESEARCH SCHEDULE / canonical execution order`

This note freezes the remaining research order for the `R(2,2)` open categorification attack.  The purpose is to prevent premature theorem claims, ad-hoc timeout increases, or a learned search policy from silently changing the proof path.

## Principle

The exact categorical/pentagon solver is authoritative.  PAL is a sidecar used only to order or diagnose branches.  No learned score may hard-prune a branch or certify a mathematical statement.

A timeout changes representation or implementation; it does not automatically increase the compute budget.

---

## Phase 0 — frozen inputs and clean replay

Required:

- based ring and fusion grammar;
- strict-unit convention;
- full-`C*` scalar gauge quotient and 16 canonical scalar components;
- corrected A--F block layering;
- independent `epsilon=+1` local-F obstruction;
- clean GitHub Actions replay of scale/D-structure experiments.

Gate: all frozen smoke tests pass in a clean checkout.

Current status: **PASS** for scale audit, D structural audit, and PAL edge-relation geometry.  `epsilon=+1` is independently closed.

---

## Phase 1 — fresh epsilon-minus chirality trace

Canonical epsilon-minus scalar components:

\[
4,5,6,7,12,13,14,15.
\]

Four components `4,6,12,14` already have an independent local-F determinant obstruction.  The deep verification frontier is

\[
\boxed{5,7,13,15}.
\]

For each frontier component, replay all

\[
2^8=256
\]

Clifford chirality assignments from the original multiplicity-aware D pentagons.

For every mask record:

1. projective-D nullity/invertibility;
2. first structural one-monomial obstruction, if any;
3. first exact phase-conflict certificate, if any;
4. surviving amplitude-ratio constraints.

Target candidate trace, to be proved rather than assumed:

\[
256\to64\to4,
\]

with four orbit-constant masks

\[
0,105,150,255.
\]

Gate: the trace is reproduced for all four frontier scalar components, with stored local pentagon provenance for both the `256 -> 64` and `64 -> 4` reductions.

---

## Phase 2 — exact D-amplitude closure on survivors

Only branches surviving Phase 1 may enter.

For each survivor:

- solve the multiplicative D-amplitude system exactly;
- prefer direct monomial/phase certificates;
- otherwise use Smith/root-of-unity lifting with an explicit completeness argument;
- substitute the resulting amplitudes back into every D-layer pentagon in characteristic zero.

Gate: every surviving branch has either an exact D obstruction or a fully verified nonzero D-amplitude solution.

Expected upper bound after Phase 1:

\[
4\text{ scalar components}\times4\text{ chirality classes}=16\text{ branches}.
\]

---

## Phase 3 — E-layer linear/projective filter

For each D survivor:

- compile all 32 corrected E blocks, including vacuum output `1`;
- solve the complete sparse linear E system;
- compute nullity and determinant polynomials for every required `2 x 2` block;
- reject a branch only by characteristic-zero rank/determinant certificate or a valid nonzero-minor argument.

Gate: all E survivors admit a simultaneous open set of invertible E blocks.

---

## Phase 4 — F-linear weighted-component filter

For each E survivor:

- compile the 16 large F blocks (eight `8 x 8`, eight `10 x 10`);
- use sparse support-one/support-two equations and weighted-component graphs before generic linear algebra;
- detect forced-zero components, parameter-independent row/column relations, or exact determinant-zero certificates;
- verify simultaneous invertibility is algebraically possible before entering nonlinear pentagons.

Gate: only branches with a proven nonempty simultaneous-invertibility locus proceed.

---

## Phase 5 — final four-noninvertible pentagon kernel

For each F-linear survivor:

- substitute all lower-layer exact data;
- quotient linear F relations first;
- compile the remaining four-noninvertible pentagons into a small polynomial kernel;
- search for local contradiction certificates before Groebner elimination;
- use numerical algebra only for discovery, followed by exact recognition/substitution.

Preferred result order:

1. two-entry or few-entry contradiction;
2. structural determinant/rank obstruction;
3. small exact elimination;
4. Groebner/Singular/Oscar only if the kernel is already genuinely small.

Gate: every branch is either exactly obstructed or supplies complete invertible associator data satisfying every pentagon.

---

## Phase 6 — independent theorem replay

No global theorem claim before this phase.

If all branches are obstructed:

- build a second implementation with different internal representation;
- replay scalar-component coverage and branch counts;
- verify each compact certificate directly in the original pentagon engine;
- audit gauge coverage, strict-unit convention, vacuum-output blocks, and branch completeness;
- reduce the computational proof to a human-readable finite chain wherever possible.

If a branch survives:

- freeze complete F-symbols;
- substitute into every pentagon independently;
- analyze gauge equivalence and relation to known constructions.

Only after this gate may `R(2,2)` noncategorifiability/categorifiability be promoted to a theorem candidate.

---

## Phase 7 — PAL search experiment

PAL remains auxiliary throughout Phases 1--6.

Trace every exact branch with:

- pre-verification history features;
- first certified failure layer;
- structural-obstruction count;
- phase-conflict count;
- D/E/F survival diagnostics;
- exact symbolic cost.

Train on graded continuation mass

\[
H_\beta(s)=\sum_{\ell\succeq s}e^{-\beta d(\ell)}
\]

rather than a terminal success bit.

Compare:

- Complex-Hermitian PAL;
- real MLP;
- linear model;
- nearest-neighbor/memory baseline;
- cheap exact handcrafted ordering.

Primary metric is not classification accuracy.  It is exact work saved before reaching the deepest viable branch:

\[
\boxed{\text{pentagon/algebra calls to first deep survivor}.}
\]

Secondary metrics include top-k continuation-mass enrichment, mass@k, scorer overhead, and wall-clock cost.

---

## Phase 8 — theoretical synthesis if PAL is empirically useful

The theory question is not merely whether a neural scorer works.

Test the following hierarchy:

\[
\text{history}
\to
\text{relation-space lift}
\to
\text{contextual continuation residual}
\to
\text{projective condensation}
\to
\text{continuation-mass concentration}.
\]

The current Clifford `K_4` toy calculation supplies an exact local model:

\[
\eta_{uv}=c_uc_v
\]

followed by projective overlap with the coherent edge predicate.  This exactly separates the candidate `192/60/4` viability levels.

Promote the PAL/PCRG interpretation only if the learned representation on the full trace exhibits both:

1. projective proximity predicting similar future continuation profiles;
2. radial/other scalar coordinates tracking continuation mass or an equivalent future potential.

The intended theoretical endpoint is a statement about learned low-dimensional approximations to future-residual geometry, not a complexity-class claim.
