# R(2,2) Phases 1--4 closure

**Status:** `CANDIDATE-NEW / EXACT STAGE CLOSURE / final nonlinear pentagons remain`

This note freezes the fresh canonical replay through the F-linear gate.  It supersedes any earlier branch-level conclusions that depended on mutable notebook state or on a single chosen E representative.

## Phase 1 — chirality localization

The deep epsilon-minus scalar frontier is

\[
\boxed{5,7,13,15}.
\]

For each component the original multiplicity-aware D pentagon engine replays all

\[
2^8=256
\]

Clifford chirality assignments and gives exactly

\[
\boxed{256=192\;\text{structural}+60\;\text{phase-conflict}+4\;\text{survivors}}.
\]

The four survivors are

\[
\boxed{0,105,150,255}.
\]

The structural and phase-conflict reductions have local pentagon provenance; no learned score or numerical solver is used for pruning.

The PAL/PCRG edge-relation observable on the two parity K4 history graphs independently produces projective-overlap values

\[
0,\;1/9,\;1
\]

with multiplicities

\[
192,\;60,\;4,
\]

and therefore exactly matches the verifier partition.  This geometric observation is auxiliary and is not used as a proof gate.

## Phase 2 — exact D-amplitude closure

All

\[
4\text{ scalar components}\times4\text{ chirality survivors}=16
\]

branches admit explicit nonzero D-amplitude witnesses already in

\[
\mu_4=\{1,i,-1,-i\}.
\]

Every witness is substituted back into the original characteristic-zero D pentagons.  Each branch verifies all 1728 D-layer matrix entries exactly.

No Phase-1 survivor requires mu8.

## Phase 3 — complete E layer

For all 16 branches the corrected E layer, including vacuum output 1, has

\[
128\text{ entries},\qquad1536\text{ nonzero linear equations},
\]

all equations have support two, and

\[
\operatorname{rank}A_E=126,\qquad\dim\ker A_E=2.
\]

All 32 required 2x2 determinant polynomials are nonzero.  More precisely, after the exact weighted-component parametrization by p,q,

\[
16\text{ determinants}=c_jp^2,\qquad
16\text{ determinants}=d_jq^2,
\]

with nonzero Gaussian-rational constants.  Hence the E-invertible locus is the genuine algebraic torus

\[
\boxed{pq\ne0}.
\]

A separate audit rejects the earlier guess that these two directions are explained by the naive parity-orbit scalar gauge: every nonzero E entry has trivial character under that proposed gauge.  Therefore Phase 4 must retain p,q symbolically.

## Phase 4 — parametric F-linear gate

It is enough to run chirality representatives 0 and 105 because global chirality flip gives the complex-conjugate classes

\[
0\leftrightarrow255,\qquad105\leftrightarrow150
\]

for the real scalar representatives.

For each of components 5,7,13,15 and masks 0,105, the F-linear system contains

\[
15744
\]

nonzero equations, all of support two, on the 1312 entries of the sixteen large F blocks.

The analysis is parametric over the full E torus, not at one selected E point.  The weighted graph and exact determinant-polynomial test show a nonempty simultaneous-invertibility locus for all sixteen required 8x8/10x10 blocks on the generic E-ratio stratum and on all four fourth-root strata.

Observed free weighted-component counts are:

- components 5 and 13: 21 free F components;
- components 7 and 15: 17 free F components plus 4 coherence-forced-zero components.

In every case the required determinant polynomials remain nonzero.

Thus every fresh deep branch passes the F-linear gate.

## Stage conclusion

The fresh audit therefore does **not** support an obstruction before the final nonlinear coherence layer.  After exact localization, D closure, the full E system, and parametric F-linear coherence, all sixteen deep epsilon-minus branches retain invertible associator loci.

The unresolved mathematical content has been localized to Phase 5:

\[
\boxed{\text{pentagons with four noninvertible external inputs}.}
\]

The next step is to quotient the F-linear relations first and compile these final pentagons into a small exact polynomial kernel.  No Groebner computation should begin before the kernel size, degree distribution, monomial structure, and local contradiction opportunities are audited.
