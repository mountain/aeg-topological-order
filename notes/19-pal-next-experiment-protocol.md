# PAL follow-up protocol on the fresh epsilon-minus trace

**Status:** `RESEARCH PLAN / auxiliary soft-search workstream`

The first PAL sidecar calibration in `notes/18-pal-projective-continuation-probe.md` shows that graded viability targets remain informative when the exact binary target is all negative.  The decisive follow-up must use the fresh canonical `epsilon=-1` audit, because that search has genuinely sparse branch survival and multiple exact failure depths.

## 1. No coupling to the proof path

The PAL scorer must never hard-prune.  The exact D/E/F/final-pentagon machinery remains authoritative.  Every learned evaluation is replayable with the scorer removed.

## 2. Trace schema

For each canonical scalar component and each chirality branch, export only after the exact audit has stabilized:

- scalar component id and stage-visible scalar-sign features;
- raw eight chirality bits;
- parity-orbit summaries and history-graph incidence features;
- first certified failure stage;
- structural monomial-obstruction count;
- phase-conflict count;
- D amplitude survivor flag;
- E nullity / required-block invertibility status;
- F weighted-component count and forced-zero count;
- final certificate type, if reached.

Verifier-derived quantities are labels/diagnostics, not input features in the strict no-leakage regime.

## 3. Graded terminal utility

Do not use only a final success bit.  Define a declared defect vector such as

\[
D(\ell)=
(\text{failure layer},\text{rank defect},\text{certificate size}).
\]

Start with a scalar utility

\[
u_\beta(\ell)=\exp[-\beta d(\ell)]
\]

where `d` is a monotone encoding of the exact failure hierarchy.  Preserve the full defect vector in storage so alternative orderings can be audited later.

## 4. Continuation mass

For every partial search state `s`, define

\[
H_\beta(s)=\sum_{\ell\succeq s}u_\beta(\ell).
\]

Parent-local supervision is

\[
q(c\mid s)=H_\beta(c)/H_\beta(s).
\]

This generalizes the completion-mass teacher used successfully in the domino/X3C PAL experiments and remains non-degenerate even when no final solution exists.

## 5. Model comparison

At controlled capacity compare:

1. Complex-Hermitian PAL;
2. real MLP;
3. linear scorer;
4. nearest-neighbor / memory baseline;
5. cheap exact handcrafted ordering if available.

Primary metrics:

- top-k continuation-mass enrichment;
- mass@1 / mass@k on held-out parent groups;
- branches evaluated before reaching the deepest surviving branch;
- cumulative exact symbolic cost before that branch;
- scorer overhead and wall-clock cost.

Secondary metrics:

- global rank correlation;
- calibration;
- learned-projective residual consistency.

## 6. Transfer protocol

The key test is transfer, not memorization.  Hold out at least one of:

- complete scalar components;
- chirality parity classes;
- certificate families;
- depth-defined history subtrees.

A successful projective representation should preserve useful top-of-beam ordering under these shifts.

## 7. Theory diagnostics

Record both the projective direction `[z]` and radial coordinate `rho`.

Test:

\[
\rho(s)\stackrel{?}{\sim}\log H_\beta(s),
\]

and whether states close in projective distance have similar normalized distributions over future failure/certificate outcomes.

If both hold, the empirical interpretation becomes:

- projective direction encodes future-behavior type;
- radius encodes remaining continuation mass;
- PAL approximates a selected contextual residual quotient.

This is the threshold for promoting the interpretation from a useful analogy to a substantive theory claim.
