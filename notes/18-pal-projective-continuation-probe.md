# PAL sidecar for categorification search: graded continuation and projective residual geometry

**Status:** `REFORMULATION + COMPUTATIONAL-CLAIM / auxiliary search experiment / never part of hard proof`

This note connects the current `R(2,2)` categorification search to the existing PAL/PCRG/AEG line.  The goal is not to replace the exact solver with a neural model.  The exact pentagon engine remains the sole source of mathematical pruning and certification.  PAL is attached only as a soft ordering sidecar.

The immediate empirical question is:

> When exact positive completions are absent or extremely sparse, does the PAL projective geometry learn a useful graded notion of future viability, and does that signal transfer across related scalar-cocycle branches?

The deeper theoretical question is:

> Is PAL better understood as learning a low-dimensional projective approximation to a future-continuation residual space, rather than as a generic binary classifier for NP-hard search?

---

## 1. Upstream PAL/PCRG lineage

### 1.1 PAL implementation

The relevant implementation is `mountain/domino-tiling`.

The structural feature encoder is:

- `paltorus/pal/features.py`, blob `28e9cc0451bc9ce337bb1154bb6214cd5afc3c1d`.

It explicitly separates topology-leakage regimes:

- regime A: no explicit topology;
- regime B: weak seam-use information;
- regime C: explicit flux and target-distance information.

The core PAL geometry is not the feature vector itself.  It is implemented in:

- `paltorus/pal/model.py`, blob `d2489c0874c50daa8a3bd8a82451b802bd6efcea`.

A concept/state encoder produces

\[
 z\in\mathbb C^d,
 \qquad \rho>0,
\]

while a predicate has a learned dual direction

\[
 c_\pi\in\mathbb C^d.
\]

The normalized Hermitian relation is

\[
\boxed{
q_\pi(C)
=
\frac{|c_\pi^\dagger z_C|^2}
{\|c_\pi\|^2\,\|z_C\|^2}.
}
\]

The calibrated score adds a radial term `u rho`.  Learned scores are soft only and never enter the certified hard-prune path.

The torus-dimer milestone report is:

- `design/pal-torus-dimer-flux-v0-milestone-report.md`, blob `b96c6d896e0c556bb31cda82023e8dac49a7eab4`.

The important empirical point is that the successful frozen construction used regime B rather than simply feeding the target winding distance to the model.  Deep parent-local training plus parent-normalized path scoring preserved target-reachable states to depth 69 and produced target leaves beyond the training leaves, while `Q_partial_eval=0` and learned scores remained outside hard pruning.

The later X3C path-distillation report also makes the search objective explicit: PAL learns a parent-local distribution over children, and the strongest teacher is completion mass rather than a raw global score.

### 1.2 PCRG / projective condensation

The conceptual bridge is explicit in `mountain/pcrg-paper`, especially:

- `notes/2026-06-22-epistemic-group-interpretation-of-condensation.md`, blob `109b11dc3c2a9cf420d240336f3b586e57a37a9e`;
- `notes/2026-06-17-finite-field-bivaluation-findings.md`, blob `4a62c597a6a0af5b3e56ea02bad944105159bf82`.

The rank-one condensation operator is

\[
\boxed{
\Pi_C
=
\frac{v_C\otimes\phi_C}{\phi_C(v_C)}.
}
\]

The arbitrary-field bivaluation core is an ordered pair of distinct projective directions

\[
(q_+,q_-)
\in
\mathbb P^1(K)^2\setminus\Delta,
\]

equivalently a rank-one idempotent projector whose image is `q_+` and kernel is `q_-`.

Thus the PAL point/predicate pairing was not merely a neural-network parameterization; it sits in the same projective point--dual / image--kernel geometry later made explicit in PCRG and AEG.

### 1.3 AEG contextual residuals

The canonical formulation is now in `mountain/aeg-paper` Paper IV:

- `paper-4/sections/04-condensation-and-continuation.tex`, blob `1eee34498fb02d24cfbd2fbe7dc4d2d6480a5457`;
- `paper-4/sections/05-contextual-residuals.tex`, blob `b51de3616cfa23556c2f8c840f1f11033227553a`.

At an interface `C`, two pasts are contextually equivalent exactly when every legal future continuation produces the same declared observation:

\[
p\equiv_Cp'
\iff
O_C(p\cdot\eta)=O_C(p'\cdot\eta)
\quad\forall\eta\in M_C.
\]

The quotient

\[
\mathcal R_C=P_C^\bot/\!\equiv_C
\]

is the canonical minimal exact state for that continuation experiment.

This gives a precise target for reinterpreting PAL: a useful learned representation should preserve future-relevant distinctions, not arbitrary details of the past.

---

## 2. Why binary supervision is wrong for the present calibration

The independently checked `epsilon=+1` theorem block in

- `experiments/r22_epsplus_local_f_obstruction.py`

contains

\[
8\times52^2=21632
\]

projective character-sheet branches.  Every branch is rigorously obstructed:

\[
\det F^{XXX}_X\equiv0.
\]

Therefore the exact binary target

\[
y(C)=\mathbf 1[\text{invertible extension exists}]
\]

is identically zero on this entire calibration set.

A binary learner has no semantic training signal here.  This is the extreme version of the class-imbalance issue that motivated the present probe.

Instead, define a *soft search diagnostic* from the same local weighted equation graph.  Give the remaining weighted-component parameters two deterministic nonzero assignments over a large prime field and let

\[
r_{\rm probe}(C)
\]

be the maximum observed rank of the required `10 x 10` block.  This is not used as a proof certificate.  It is a cheap soft observable of how close the local branch is to invertibility.

Define

\[
 d(C)=10-r_{\rm probe}(C),
\qquad
 u(C)=\exp(-d(C)/2).
\]

This turns the all-negative theorem family into a graded viability landscape without changing a single hard-prune decision.

---

## 3. Sidecar experiment

The frozen script is:

- `experiments/r22_pal_distance_probe.py`.

### 3.1 Inputs

A branch is represented only by pre-verification data:

1. the unordered character pair on each of the eight multiplicity-two history fibers, encoded symmetrically by bit means and XORs;
2. simple parity-component summaries;
3. the 72 C-layer scalar signs of the current canonical scalar component.

The model does **not** receive:

- local-F equations;
- local rank;
- forced-zero counts;
- determinant information;
- any exact obstruction certificate.

### 3.2 Transfer split

Train scalar components:

\[
\{0,1,8,9\}.
\]

Held-out scalar components:

\[
\{2,3,10,11\}.
\]

Thus the test is not only interpolation among branch assignments inside one scalar component.

### 3.3 Models

Two same-hidden-width scorers are compared:

1. `PAL-distance`: Complex-Hermitian point/predicate geometry faithful to the original PAL-II architecture, trained with the soft target `u(C)`;
2. `MLP-distance`: ordinary real MLP trained on exactly the same features and soft target.

The experiment is a ranking calibration, not a claim that one architecture is universally superior.

---

## 4. First replay result

A local replay of the frozen protocol used eight training seeds and 300 optimization steps per seed.

The held-out test distribution has

\[
\Pr[r_{\rm probe}=9]\approx0.1435,
\]

and mean probe rank approximately

\[
6.691.
\]

The mean results were:

| model | Spearman | top-20 rank-9 | top-50 rank-9 | top-100 rank-9 |
|---|---:|---:|---:|---:|
| PAL-distance | 0.717 | 0.750 | 0.723 | 0.623 |
| real MLP-distance | 0.746 | 0.500 | 0.490 | 0.497 |
| natural test prevalence | -- | 0.143 | 0.143 | 0.143 |

Standard deviation of Spearman across the eight seeds was about `0.024` for PAL and `0.031` for the MLP.  Top-k metrics had substantial seed variance, so these numbers are evidence for a follow-up, not a final benchmark.

### Interpretation

Two conclusions are already justified.

**COMPUTATIONAL-CLAIM 1.** Graded supervision is strongly informative where the exact binary target is completely degenerate.

**COMPUTATIONAL-CLAIM 2.** The projective PAL model is competitive with an ordinary real MLP and, in this transfer split, concentrates more of the highest-rank branches at the extreme top of the list.  The MLP has slightly better global rank correlation, so this experiment does **not** establish a generic representational advantage for the projective model.

The search-relevant question is top-of-beam concentration rather than global regression accuracy.  That is where the first signal in favor of PAL appears.

A small parent-local listwise pilot on the high-branching decisions showed that both PAL and the real MLP improve continuation-mass concentration over uniform choice, but neither clearly dominates.  Therefore the next decisive benchmark should use the fresh `epsilon=-1` sparse-survivor trace, where continuation mass is much more concentrated.

---

# Part II. Theoretical reinterpretation

## 5. Completion mass is not merely a training trick

Let a finite exact search DAG have state `s`, legal children `c`, and terminal descendants `\ell`.  Assign a nonnegative terminal utility `u(\ell)` and define the continuation mass

\[
\boxed{
H(s)=\sum_{\ell\succeq s}u(\ell).
}
\]

If the children partition the descendant terminals, then

\[
\boxed{
H(s)=\sum_{c\in\mathrm{Child}(s)}H(c).
}
\]

Whenever `H(s)>0`, this induces the exact parent-local law

\[
\boxed{
P^*(c\mid s)=\frac{H(c)}{H(s)}.
}
\]

This is exactly the form used by the successful PAL completion-count teacher in the domino/X3C experiments.

For the original target-completion problem,

\[
u(\ell)=\mathbf1[\ell\text{ is a target}],
\]

so `H(s)` is the number of target completions below `s`.

Along a path

\[
s_0\to s_1\to\cdots\to s_T,
\]

the ideal path probability telescopes:

\[
\prod_{t<T}P^*(s_{t+1}\mid s_t)
=
\frac{H(s_T)}{H(s_0)}.
\]

Thus the parent-normalized PAL path score is not an arbitrary calibration device.  With exact completion mass, it is the conditional path law induced by future target mass.  Algebraically this has the same form as a Doob `h`-transform on the search DAG.

## 6. The zero-positive generalization

If no successful terminal is known, the indicator utility makes `H=0` and loses all information.  The user's proposed distance target suggests the natural replacement.

Let `d(\ell)` be a certified or diagnostic defect/distance, for example:

- first coherence layer at which the branch fails;
- rank deficiency of a required associator;
- size of a minimal contradiction certificate;
- residual dimension after exact propagation;
- another declared verifier-derived defect.

Define a soft terminal utility

\[
\boxed{
u_\beta(\ell)=e^{-\beta d(\ell)}
}
\]

and the soft continuation partition function

\[
\boxed{
H_\beta(s)
=
\sum_{\ell\succeq s}e^{-\beta d(\ell)}.
}
\]

Then

\[
P_\beta^*(c\mid s)
=
\frac{H_\beta(c)}{H_\beta(s)}
\]

remains well defined even when every complete branch ultimately fails.

This is the principled version of "use a distance rather than binary positive/negative."  The distance is not merely a regression target; it induces a future-weighted path measure over the search tree.

The current `R(2,2)` probe is the simplest leaf-level version of this construction, with

\[
d=10-r_{\rm probe}.
\]

## 7. Relation to the contextual residual

Paper IV gives an exact equivalence relation:

\[
s\equiv s'
\iff
O(s\cdot\eta)=O(s'\cdot\eta)
\quad\forall\eta.
\]

For search, choose as observations one or several future functionals such as

\[
H_\pi(s),
\qquad
H_{\beta,\pi}(s),
\qquad
\text{failure-depth distribution},
\qquad
\text{future certificate type}.
\]

The exact contextual residual quotient is the minimal state retaining *all* declared future information.  In hard problems it may be too large or too expensive to construct explicitly.

This suggests the following reinterpretation.

> **PAL is a learned approximate condensation of the contextual continuation-residual space for selected future observables.**

The encoder does not need to reconstruct the complete past.  It needs to retain enough of the past to predict the future continuation law relevant to search.

## 8. Why projective geometry is a plausible representation

In PAL/PCRG language, a state supplies a projective point direction `[z]`, while a future predicate supplies a dual direction `[c_\pi]`.  Their normalized pairing measures incidence/compatibility:

\[
q_\pi(s)
=
\frac{|c_\pi^\dagger z_s|^2}
{\|c_\pi\|^2\|z_s\|^2}.
\]

This separates two kinds of information:

1. **projective direction `[z]`**: relational type -- which future predicates the state aligns with;
2. **radial variable `rho`**: intensity/mass -- how much continuation weight remains.

A natural future PAL model would therefore test the identification

\[
\rho(s)
\sim
\log H_\beta(s)
\]

or another monotone mass coordinate, while the projective direction represents the *shape* of the future continuation profile across multiple predicates.

This gives an operational meaning to the point/radius split that is stronger than generic neural embedding language.

## 9. Relation to the original PAL research question

The original practical question was whether a learned geometric representation can accelerate exact NP-hard search without entering the correctness path.

The refined question is:

\[
\boxed{
\text{Can a low-dimensional projective condensation preserve enough of the}
\atop
\text{future contextual residual to concentrate continuation mass?}
}
\]

Search acceleration then has a precise mechanism:

1. exact history space contains many distinctions;
2. only some distinctions affect the selected future observations;
3. PAL learns a quotient/condensation that suppresses irrelevant distinctions;
4. the learned continuation law concentrates beam mass on high-`H` children;
5. the symbolic verifier retains correctness.

This is not a worst-case complexity theorem.  It is a representation-dependent statement about effective branching and future-mass concentration.

In this formulation AEG, PCRG, and PAL occupy distinct but composable roles:

\[
\boxed{
\begin{array}{rcl}
\text{AEG/history} &:& \text{make process histories and their distinctions explicit},\\
\text{contextual residual} &:& \text{identify the exact future-relevant quotient},\\
\text{PCRG} &:& \text{provide projective condensation / point--dual geometry},\\
\text{PAL} &:& \text{learn an approximate future-relevant condensation and policy},\\
\text{verifier} &:& \text{retain exact correctness and supply certificates}.
\end{array}
}
\]

---

## 10. Falsifiable next experiments

The present result is promising but not sufficient to claim that projective geometry is uniquely responsible for the search gain.  The following tests should decide the issue.

### A. Fresh epsilon-minus sparse-survivor trace

Once the canonical `epsilon=-1` D audit is stable, export for every chirality branch:

- raw history/chirality state;
- structural D-failure flag;
- phase-conflict count;
- exact D survivor status;
- E/F survival depth;
- final certificate type where available.

Use a graded utility rather than final binary success.

### B. Projective versus real representation under transfer

Compare, at matched or controlled capacity:

- Complex-Hermitian PAL;
- real MLP;
- linear scorer;
- nearest-neighbor memory baseline.

The primary metric should be top-of-beam continuation-mass enrichment, not global MSE.

### C. Residual-consistency test

Cluster states by learned projective direction.  For states close in latent projective distance, measure whether their empirical distributions over future certificate/survival outcomes are also close.

This directly tests the claim that the latent geometry approximates a contextual residual quotient.

### D. Radius/mass test

Test whether `rho` is monotone with a continuation mass such as

\[
\log H_\beta(s).
\]

If projective direction predicts *type* while radius predicts *mass*, the PAL/PCRG decomposition gains a concrete search-theoretic interpretation.

### E. Frozen beam test

Only after the representation tests pass should PAL be inserted as a soft scorer into the actual categorification branch queue.  Hard pruning must remain exact.  Compare:

- exact branches evaluated before reaching deepest survivors;
- cumulative symbolic/CAS cost;
- top-k survival enrichment;
- wall-clock cost including scorer overhead.

---

## 11. Current verdict

**COMPUTATIONAL-CLAIM.** Graded viability supervision is useful on an exact all-negative categorification branch family where binary supervision is mathematically degenerate.

**COMPUTATIONAL-CLAIM.** In the first cross-component transfer probe, Complex-Hermitian PAL shows stronger extreme top-k rank-9 concentration than a same-hidden-width real MLP, although the MLP has slightly stronger global rank correlation.  This is a search-relevant signal, not yet proof of a unique projective advantage.

**REFORMULATION.** The most coherent theoretical reading is no longer "PAL learns a positive/negative classifier."  It is:

\[
\boxed{
\text{PAL learns a projective approximation to future continuation residuals,}
\atop
\text{with continuation mass providing the search potential.}
}
\]

The decisive next test is the fresh `epsilon=-1` trace, where the true survivor set is sparse and exact branch depth varies substantially.
