# R(2,2) categorification attack — integrated report through component-5 Phase 5

**Status:** `INTEGRATED / EXACT WHERE MARKED / GLOBAL R(2,2) PROBLEM STILL OPEN`

This note consolidates the fresh exact R(2,2) categorification work after the canonical Phase-1–4 replay and the first two complete Phase-5 closures.  It is intended as the current high-level reference for theorem boundaries, exact certificates, computational reductions, and the next research frontier.

The detailed source notes remain:

- `notes/23-r22-phases1-4-closure.md` — canonical Phase 1–4 closure;
- `notes/25-r22-phase5-z0-certificate.md` — first mask-0 `z0 != 0` certificate;
- `notes/26-r22-component5-mask0-phase5-closure.md` — complete component-5/mask-0 Phase-5 closure;
- `notes/27-r22-component5-mask105-phase5-closure.md` — complete component-5/mask-105 Phase-5 closure.

No statement below upgrades an exploratory observation to a theorem unless an exact replay or local certificate has already been recorded.

---

## 1. Executive summary

The current strongest exact conclusion is:

\[
\boxed{
\text{R(2,2) has no obstruction through D/E/F-linear coherence,}
}
\]

but genuine obstructions appear in the final nonlinear pentagons.

For the epsilon-minus scalar component `5`, two chirality survivors have now been closed independently:

\[
\boxed{
\text{component 5 / mask 0 is non-categorifiable},
}
\]

and

\[
\boxed{
\text{component 5 / mask 105 is non-categorifiable}.
}
\]

Both closures are exact and use only finite algebraic stratification, affine elimination, and a handful of final-pentagon entries.  Neither uses a Gröbner basis, global nonlinear solver, floating-point root search, or numerical continuation.

The global theorem

\[
\boxed{R(2,2)\text{ is non-categorifiable}}
\]

is **not yet proved**.  The remaining open work is:

1. component `5`, chirality masks `150` and `255`;
2. the Phase-5 branches for scalar components `7`, `13`, and `15`.

A direct coordinatewise complex-conjugation audit of

```text
0   <-> 255
105 <-> 150
```

has now been run and **fails**.  Therefore masks `150` and `255` cannot currently be closed merely by saying that they are the complex conjugates of the already-closed branches.  A nontrivial coordinate/gauge map must be derived, or the two branches must be replayed fresh.

---

## 2. The theorem boundary

The object under study is the Meng–Yu rank-six self-dual fusion ring `R(2,2)`.

The epsilon-plus half has already been excluded independently by the local-F determinant obstruction.  For epsilon-minus, the deep scalar frontier is

\[
\boxed{5,7,13,15}.
\]

For each scalar component, Phase 1 leaves four chirality survivors:

\[
\boxed{0,105,150,255}.
\]

Thus the deep epsilon-minus theorem problem contains

\[
4\times4=16
\]

branches before Phase-5 obstruction analysis.

A final non-categorifiability theorem requires an exact obstruction for all of them, modulo only symmetries that are themselves proved on the complete coherence quotient.

---

## 3. Canonical Phase 1–4 backbone

The Phase 1–4 results are frozen in `notes/23-r22-phases1-4-closure.md` and are the accepted starting point for Phase 5.

### 3.1 Phase 1 — chirality localization

For every deep scalar component, all

\[
2^8=256
\]

chirality assignments split exactly as

\[
\boxed{
256
=
192\;\text{structural failures}
+
60\;\text{phase conflicts}
+
4\;\text{survivors}.
}
\]

The survivors are always

\[
\boxed{0,105,150,255}.
\]

The pruning is produced by exact pentagon provenance, not by a learned score or approximate solver.

### 3.2 Phase 2 — D amplitude

All

\[
4\text{ scalar components}\times4\text{ chirality survivors}=16
\]

branches admit explicit nonzero D-amplitude witnesses already in

\[
\mu_4=\{1,i,-1,-i\}.
\]

Each witness has been substituted back into the original characteristic-zero D pentagons, and all

\[
\boxed{1728}
\]

D-layer matrix entries verify exactly on every branch.

Hence there is no D-amplitude obstruction on the deep epsilon-minus frontier.

### 3.3 Phase 3 — E layer

For all 16 branches the corrected E layer has

\[
128\text{ entries},\qquad1536\text{ support-two equations},
\]

with

\[
\boxed{
\operatorname{rank}A_E=126,
\qquad
\dim\ker A_E=2.
}
\]

The two free directions are not the previously conjectured residual scalar gauge.  In exact weighted coordinates `p,q`, all 32 required E determinants are nonzero monomials:

\[
16\times c_jp^2,
\qquad
16\times d_jq^2,
\qquad c_j,d_j\neq0.
\]

Therefore the genuine E-invertible locus is

\[
\boxed{pq\neq0}.
\]

### 3.4 Phase 4 — parametric F-linear coherence

The F-linear quotient contains

\[
15744
\]

nonzero support-two equations on the 1312 entries of the sixteen required large F blocks.

The resulting weighted-component counts are:

- components `5` and `13`: 21 free F components;
- components `7` and `15`: 17 free F components plus 4 coherence-forced-zero components.

The forced zeros for components 7 and 15 do not make any required `8x8` or `10x10` associator determinant identically zero.  Exact determinant-polynomial audits retain a nonempty simultaneous-invertibility locus.

Thus:

\[
\boxed{
\text{there is no obstruction in D/E/F-linear coherence}.
}
\]

The unresolved content is therefore localized to the final pentagons with four noninvertible external inputs.

---

## 4. Phase 5: from tens of thousands of scalar equations to a small exact kernel

For component 5, the Phase-4 quotient has

\[
p,q,z_0,\ldots,z_{20},
\]

so the effective nonlinear kernel begins with

\[
\boxed{23\text{ parameters}}.
\]

The final-pentagon compiler considers only blocks with four noninvertible external inputs.  There are

\[
\boxed{96\text{ final pentagon blocks}}
\]

with dimension profile

\[
32\times8,
\qquad
32\times10,
\qquad
32\times40.
\]

Hence there are

\[
\boxed{56,448}
\]

scalar positions.  Of these,

\[
\boxed{50,880}
\]

are nonzero before canonical deduplication.

The sparse exact Laurent compiler reduces them to only

\[
\boxed{219}
\]

unique cubic polynomial equations.

This is the first decisive Phase-5 reduction:

\[
50,880\text{ nonzero scalar entries}
\longrightarrow
219\text{ exact cubic relations}.
\]

The useful next move was not a global Gröbner basis.  The short equations were instead used as local rewrite rules and branch separators.

---

## 5. Complete Phase-5 closure: component 5 / mask 0

This branch is recorded in full in `notes/26-r22-component5-mask0-phase5-closure.md`.

### 5.1 First localization: `z0 != 0`

The four shortest final-pentagon equations are

\[
\begin{aligned}
p^2z_0+i z_2z_3&=0,\\
p z_2z_3-\frac{1+i}{4}z_0&=0,\\
q z_1z_8+\frac{1-i}{4}z_0&=0,\\
q^2z_0-i z_1z_8&=0.
\end{aligned}
\]

Assuming `z0=0` yields four product-zero patterns.  Two are killed by required F-block invertibility; the other two reduce through a very small number of final pentagon cells to nonzero constants.  Therefore

\[
\boxed{z_0\neq0}.
\]

### 5.2 Continuous parameters collapse to 18 finite strata

Because `z0 != 0`, the four binomials can be divided legitimately, giving

\[
\boxed{
p^3=\frac{1-i}{4},
\qquad
q^3=-\frac{1+i}{4},
}
\]

and

\[
z_2z_3=i p^2z_0,
\qquad
z_1z_8=-i q^2z_0.
\]

Hence

\[
z_1z_2z_3z_8\neq0.
\]

A fifth local relation gives

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

Thus the formerly continuous `(p,q,z0)` sector becomes exactly

\[
\boxed{3\times3\times2=18}
\]

finite algebraic branches.

### 5.3 Exact `10 + 8` stratification

Ten branches lie on an affine rank-11 stratum and are excluded by short diagnostic cells.

The remaining eight lie on a rank-10 stratum.  After safe affine elimination and the already-proved nonzero product identities, the residual kernel is carried by

\[
\boxed{
z_1,z_2,z_4,z_5,z_{11},z_{12},z_{19},z_{20}
}
\]

with `z1*z2 != 0`.

The genuinely nonlinear part then collapses further to

\[
x=z_{19},
\qquad
y=z_{20}.
\]

For four rank-drop branches, three local `(XXXX;g)` entries already give an exact contradiction.  The remaining four cube/root branches are forced to

\[
\boxed{x=-y},
\qquad
\boxed{y^2=-\frac18}.
\]

The last sign ambiguity is killed by the adjacent cell

```text
(XXXX;g)_(0,1)
```

which becomes the nonzero constant equation

\[
\boxed{1=0}.
\]

Therefore

\[
\boxed{
\text{component 5 / mask 0 is non-categorifiable}.
}
\]

---

## 6. Complete Phase-5 closure: component 5 / mask 105

This branch is recorded independently in `notes/27-r22-component5-mask105-phase5-closure.md`.

Mask 105 is not just mask 0 with the same equations renamed.  Its 219-polynomial term-count fingerprint differs, and its p-side finite relation changes phase.

### 6.1 Zero branch and five local relations

Fresh replay again proves

\[
\boxed{z_0\neq0}.
\]

The five exact relations are now

\[
\boxed{
p^3=\frac{1+i}{4},
\qquad
q^3=-\frac{1+i}{4},
}
\]

\[
\boxed{
z_2z_3=-ip^2z_0,
\qquad
z_1z_8=-iq^2z_0,
}
\]

and

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

Again the continuous torus collapses to

\[
\boxed{18}
\]

finite `(p,q,z0)` strata.

The five-relation rewrite reduces 219 kernel polynomials to 210 unique residual polynomials, but produces no immediate singleton or small-support full-rank contradiction.  Therefore finite-stratum analysis is genuinely required.

### 6.2 The same coarse `10 + 8` geometry reappears

Fresh affine closure gives:

- 10 rank-11 branches, all killed by three diagnostic final cells;
- 8 rank-10 branches, corresponding to

```text
(a,b) = (1,1), (2,1), (1,2), (2,2)
```

for both roots of `z0`.

Again the hard core reduces to

\[
x=z_{19},
\qquad y=z_{20}.
\]

### 6.3 Off-diagonal branches: two-cell certificates

For `(a,b)=(2,1)` and `(1,2)`, the cell

```text
G0 = (XXXX;g)_(0,0)
```

is a nonzero scalar multiple of

\[
(x-y)^2.
\]

Thus `x=y`.  The adjacent cell

```text
G2 = (XXXX;g)_(0,2)
```

gives

\[
4xy-4y^2-1=0,
\]

which on `x=y` becomes

\[
\boxed{-1=0}.
\]

Thus four branches close with only two local pentagon cells each.

### 6.4 Diagonal branches: three-cell certificates

For `(a,b)=(1,1)` and `(2,2)`, two cells give

\[
4xy-4y^2-1=0
\]

and

\[
4x^2-4xy+1=0.
\]

Adding them yields

\[
4(x-y)(x+y)=0.
\]

The `x=y` branch contradicts the first equation, so

\[
\boxed{x=-y},
\qquad
\boxed{y^2=-\frac18}.
\]

The third cell then evaluates to

\[
\frac{-\sqrt3+i}{4}\neq0
\]

or

\[
\frac{-\sqrt3-i}{4}\neq0,
\]

depending on the cube pair.

Therefore all eight rank-drop branches close and

\[
\boxed{
\text{component 5 / mask 105 is non-categorifiable}.
}
\]

---

## 7. Chirality conjugation audit: what failed, and what remains open

Phase 2 and Phase 4 suggest natural chirality pairings

```text
0   <-> 255
105 <-> 150
```

so the next question was whether the full Phase-5 quotient inherits a simple coefficientwise complex-conjugation symmetry.

A dedicated exact audit tested the coordinate map

```text
p -> p
q -> q
z_j -> z_j
coefficients -> complex conjugates
```

while rebuilding the complete non-unit lower associator data, the required F blocks, and the final 219-polynomial kernels.

The answer is negative.

### 7.1 Pair `0 <-> 255`

Under the naive coordinatewise conjugation:

- 1881 non-unit lower associator entries were checked;
- 288 of the 1312 required F entries mismatch;
- the required F blocks are therefore not entrywise conjugate in this coordinate system;
- the final 219-polynomial kernel sets are not equal after coefficient conjugation.

Thus

\[
\boxed{
0\leftrightarrow255
\text{ is not proved by the identity-coordinate conjugation map.}
}
\]

### 7.2 Pair `105 <-> 150`

The mismatch is even stronger under the same map:

- all 1312 required F entries mismatch;
- the final conjugated kernel set again does not match the target 219-polynomial set.

Thus

\[
\boxed{
105\leftrightarrow150
\text{ is not proved by the identity-coordinate conjugation map.}
}
\]

### 7.3 Correct interpretation

This negative audit does **not** prove that the paired chiralities are mathematically unrelated.  It proves only that the obvious coordinate map is insufficient after the Phase-4 quotient.

Two possibilities remain:

1. there is a nontrivial signed/permuted/monomial coordinate transformation on `p,q,z_j` implementing chirality conjugation;
2. there is no useful full-Phase-5 conjugation symmetry, and masks `150` and `255` must be replayed fresh.

Until one of these is established, masks `150` and `255` remain open.

---

## 8. Current exact theorem-state table

| Sector | Current status |
|---|---|
| epsilon-plus | **CLOSED** by local-F determinant obstruction |
| epsilon-minus Phase 1–4 | **CLOSED exactly** for all 16 deep branches |
| component 5 / mask 0 | **CLOSED / non-categorifiable** |
| component 5 / mask 105 | **CLOSED / non-categorifiable** |
| component 5 / mask 255 | **OPEN at Phase 5**; naive conjugation from mask 0 failed |
| component 5 / mask 150 | **OPEN at Phase 5**; naive conjugation from mask 105 failed |
| component 7 / masks 0,105,150,255 | **OPEN at Phase 5** |
| component 13 / masks 0,105,150,255 | **OPEN at Phase 5** |
| component 15 / masks 0,105,150,255 | **OPEN at Phase 5** |
| global `R(2,2)` categorifiability | **OPEN** |

The strongest theorem-level statement currently justified is therefore branch-local, not yet ring-global.

---

## 9. The central structural discovery: relation-space stratification

The most important outcome of the work is not merely that two branches are obstructed.  It is the form of the obstruction search.

A raw nonlinear coherence problem with tens of thousands of scalar equations repeatedly collapses as

\[
\boxed{
\begin{array}{c}
\text{large coherence system}\\
\Downarrow\\
\text{linear quotient}\\
\Downarrow\\
23\text{-parameter Laurent kernel}\\
\Downarrow\\
219\text{ cubic relations}\\
\Downarrow\\
z_0\neq0\\
\Downarrow\\
5\text{ exact local identities}\\
\Downarrow\\
18\text{ finite algebraic strata}\\
\Downarrow\\
10+8\text{ affine-rank stratification}\\
\Downarrow\\
(x,y)=(z_{19},z_{20})\text{ two-variable core}\\
\Downarrow\\
2\text{--}4\text{ local pentagon cells}\\
\Downarrow\\
\text{exact contradiction.}
\end{array}
}
\]

This suggests a general methodological principle:

> The difficult object is often not the raw equation system itself, but the choice of representation.  After passage to the correct relation space, the coherence locus may be sharply stratified and much lower-dimensional than the original search space suggests.

This is presently an experimentally supported research principle, not a general theorem.

---

## 10. PAL/PCRG geometry: an independent signal of the same phenomenon

The Phase-1 chirality search gives the exact verifier partition

\[
192,\qquad60,\qquad4.
\]

Independently, the PAL/PCRG edge-relation observable

\[
\eta_{uv}=c_uc_v
\]

on the two parity-`K4` history graphs produces projective-overlap values

\[
\boxed{0,\quad\frac19,\quad1}
\]

with multiplicities

\[
\boxed{192,\quad60,\quad4}.
\]

The correspondence is mask-by-mask, not merely a histogram coincidence.

The correct current interpretation is:

\[
\boxed{
\text{exact verifier filtration}
\approx
\text{projective relation-space stratification}
}
\]

for this finite history system.

This PAL/PCRG observation is auxiliary and is not used as a proof gate.  Its importance is conceptual: it independently points toward the same move that succeeds in Phase 5 — leave the raw history/search representation and work in a relation space where the strata become visible.

---

## 11. Computational lessons

### 11.1 Exactness mattered

The decisive certificates are algebraic identities such as

\[
p^3=\frac{1\mp i}{4},
\qquad
2z_0^2+4z_0-1=0,
\qquad
z_{20}^2=-\frac18,
\]

followed by exact nonzero remainders.  Floating-point continuation would be a poor proof substrate for this stage.

### 11.2 Symbolic blow-up was a representation failure, not a mathematical signal

Generic SymPy expansion over algebraic-number fields became a bottleneck on the rank-drop branches.  The computation was therefore rewritten over

\[
K=\mathbf Q(i,\sqrt2,\sqrt3)
\]

using an eight-dimensional rational basis and sparse Laurent arithmetic.

This reduced the exact residual compilation from repeated timeout behavior to a routine sub-gate computation without changing the 10-minute research budget.

### 11.3 Gröbner bases were unnecessary

The full closures of masks 0 and 105 were obtained without a global Gröbner computation.  The successful pattern was:

1. exact localize only by quantities already proved nonzero;
2. extract short equations;
3. reduce continuous torus parameters to finite algebraic choices;
4. classify affine rank strata;
5. project onto a small residual relation space;
6. search for the shortest local contradiction certificate.

This is both more auditable and more informative than treating the 219 equations as one opaque polynomial ideal from the start.

---

## 12. What the current results say about AEG-style process representation

The present experiment gives a concrete version of a broader AEG intuition: operation history and representation choice can hide a much smaller relational geometry.

Two independent examples now show the same qualitative behavior.

### Phase 1

\[
256\text{ chirality histories}
\longrightarrow
3\text{ projective relation strata}.
\]

### Phase 5

\[
219\text{ nonlinear relations}
\longrightarrow
18\text{ finite strata}
\longrightarrow
10+8
\longrightarrow
2\text{-variable cores}
\longrightarrow
\text{local certificates}.
\]

This motivates the working hypothesis:

\[
\boxed{
\text{complex exact search may be high-dimensional in representation space}
\text{ but low-dimensional and stratified in a suitable relation space.}
}
\]

The hypothesis is not yet a theorem of AEG or PAL.  The value of the R(2,2) experiment is that it supplies a nontrivial exact setting in which this representation-to-relation transition is visible and operationally useful.

---

## 13. Next research program

The next work should be ordered by information gain rather than by brute-force branch count.

### 13.1 Resolve component-5 chirality pairing

For `0 <-> 255` and `105 <-> 150`, inspect the lower-entry mismatch pattern to determine whether there is a structured coordinate map involving:

- signed permutations of the 21 F components;
- monomial rescalings by powers of `p,q`;
- possible reindexing of multiplicity bases;
- conjugation combined with a gauge transformation.

If a single exact map explains the full lower quotient and determinant locus, masks 150 and 255 can close by theorem.  If not, replay them fresh using the already-developed sparse Phase-5 machinery.

### 13.2 Move to component 13

Component 13 shares the Phase-4 count of 21 free F components with component 5.  It is therefore the cleanest next test of whether the component-5 `23 -> 219 -> finite strata -> local certificate` geometry persists across scalar components.

### 13.3 Then attack components 7 and 15

These branches are structurally different already at Phase 4:

\[
17\text{ free F components}+4\text{ forced-zero components}.
\]

Their Phase-5 kernels may therefore exhibit a genuinely different obstruction geometry.  They are particularly valuable as a test of whether the observed relation-space method is robust rather than component-5-specific.

### 13.4 Global theorem target

Only after every surviving epsilon-minus branch is closed can one state

\[
\boxed{R(2,2)\text{ is non-categorifiable}.}
\]

Until then, branch-level obstruction theorems and structural method claims must remain explicitly separated from the global statement.

---

## 14. Results that are safe to cite now

### Exact result A — canonical Phase 1–4 closure

All 16 deep epsilon-minus branches survive D, E, and F-linear coherence with an invertible locus.  The obstruction, if any, is confined to the final four-noninvertible pentagons.

### Exact result B — component 5 / mask 0

\[
\boxed{\text{non-categorifiable at Phase 5}.}
\]

The proof reduces the 219-polynomial kernel to 18 finite algebraic branches and closes all of them by local certificates.

### Exact result C — component 5 / mask 105

\[
\boxed{\text{non-categorifiable at Phase 5}.}
\]

This is an independent fresh replay with a different p-side relation and different kernel fingerprint.  Its final rank-drop branches close with two- and three-cell certificates.

### Exact negative result D — naive full chirality conjugation

The identity-coordinate coefficient-conjugation maps

```text
0   -> 255
105 -> 150
```

fail on the complete Phase-4 quotient and on the final 219-polynomial kernel.  Therefore the remaining two component-5 masks are not closed by this naive symmetry argument.

### Auxiliary structural result E — PAL/PCRG correspondence

The projective-overlap strata `0,1/9,1` reproduce the exact `192/60/4` Phase-1 verifier partition mask-by-mask.  This is exact computational evidence, but it is not yet used as a theorem gate.

---

## 15. SCM and reproducibility boundary

The accepted Phase-1–4 checkpoint remains on `main`; the dependency-complete canonical mainline checkpoint is

```text
9a1658dc9f1573dd61229d2e643ac8b9ef828228
```

while Phase-5 work remains on

```text
agent/r22-phase5-final-kernel
```

inside draft PR `#6`.

This separation is intentional:

- `main` records accepted reproducible research state;
- the Phase-5 branch records the open frontier, exact closures, audits, and potentially supersedable coordinate hypotheses;
- no global `R(2,2)` theorem should be merged merely because component 5 has two closed masks.

The preferred next stage closure is either:

1. all four component-5 masks closed, with the remaining two obtained by a proved coordinate symmetry or fresh replay; or
2. a broader closure that simultaneously establishes a reusable Phase-5 obstruction schema for components 5 and 13.

---

## 16. Final perspective

The strongest lesson of the current work is methodological.

The original coherence problem appears as a large nonlinear system.  The successful exact attack did not solve that system globally.  Instead it repeatedly changed representation until the relevant geometry became visible:

\[
\boxed{
\text{search space}
\longrightarrow
\text{relation space}
\longrightarrow
\text{finite strata}
\longrightarrow
\text{low-dimensional core}
\longrightarrow
\text{local certificate}.
}
\]

This mechanism has now succeeded independently on component-5 masks 0 and 105.  The next decisive question is whether components 7, 13, and 15 exhibit the same kind of stratified relation geometry.

If they do, the R(2,2) project will have produced something stronger than a single categorification obstruction: it will have produced a reproducible method for turning a large exact coherence search into a small geometric certificate problem.
