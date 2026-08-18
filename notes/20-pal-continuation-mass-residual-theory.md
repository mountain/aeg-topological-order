# PAL continuation mass, contextual residuals, and projective factorization

**Status:** `REFORMULATION / elementary exact propositions + research conjecture for learned geometry`

This note sharpens the connection among three existing strands:

1. PAL completion-mass / parent-local search training from `mountain/domino-tiling`;
2. PCRG / PAL-II projective point--predicate geometry from `mountain/pcrg-paper`;
3. contextual continuation residuals in AEG Paper IV.

The propositions below are elementary.  The research content is the proposed interpretation and the empirical programme: a successful PAL representation should approximate a future-continuation residual, with projective direction encoding normalized future type and a radial variable encoding total continuation mass.

---

## 1. Search as a continuation experiment

Let `S` be a finite rooted search tree (or a DAG after unfolding paths).  A state `s` records the current past.  Legal next actions generate children `c \in Child(s)`.  A terminal continuation from `s` is a continuation word `eta` ending in a leaf `ell=s\cdot eta`.

Let

\[
u(\ell)\ge0
\]

be a declared terminal utility.  The classical target-count case is

\[
u(\ell)=\mathbf 1[\ell\text{ is a target completion}].
\]

When exact positives are absent or too sparse, a graded utility may be used, for example

\[
\boxed{u_\beta(\ell)=e^{-\beta d(\ell)}}
\]

for a declared certified defect or failure distance `d`.

Define the continuation mass

\[
\boxed{
H(s)=\sum_{\ell\succeq s}u(\ell).
}
\]

The sum is over continuation paths/leaves, so the child decomposition is disjoint and

\[
\boxed{
H(s)=\sum_{c\in Child(s)}H(c).
}
\]

This is exactly the mathematical form already used by PAL completion-count teachers.

---

## 2. The induced parent-local law

Whenever `H(s)>0`, define

\[
\boxed{
P^*(c\mid s)=\frac{H(c)}{H(s)}.
}
\]

### Proposition 2.1 — path telescoping

For a complete path

\[
s_0\to s_1\to\cdots\to s_T=\ell,
\]

one has

\[
\prod_{t=0}^{T-1}P^*(s_{t+1}\mid s_t)
=
\frac{u(\ell)}{H(s_0)}.
\]

**Proof.**  The intermediate continuation masses cancel:

\[
\prod_t \frac{H(s_{t+1})}{H(s_t)}
=
\frac{H(\ell)}{H(s_0)}
=
\frac{u(\ell)}{H(s_0)}.
\]

Thus parent-local completion-mass training is not an arbitrary calibration device.  It is the conditional law of the globally utility-tilted path measure.

For binary target utility this is the uniform distribution over target completions when all target leaves have unit weight.  For `u_beta=e^{-beta d}`, it is a Gibbs-like distribution concentrating on low-defect continuations.

---

## 3. Why parent-local listwise loss matches long-horizon path loss

Let

\[
\mu(\ell)=u(\ell)/H(s_0)
\]

be the exact utility-tilted terminal distribution.  Let a learned policy `P_theta(c|s)` induce

\[
Q_\theta(\ell)=\prod_t P_\theta(s_{t+1}\mid s_t).
\]

### Proposition 3.1 — chain-rule decomposition

Assume `P_theta` gives positive mass wherever `mu` does.  Then

\[
\boxed{
D_{KL}(\mu\Vert Q_\theta)
=
\sum_s \Pr_\mu[s\text{ is visited}]\,
D_{KL}\!\left(P^*(\cdot\mid s)\Vert P_\theta(\cdot\mid s)\right).
}
\]

**Proof.**  Expand the log likelihood ratio along each path and exchange the sum over leaves with the sum over visited prefixes.  This is the ordinary chain rule for KL divergence on a tree.

This proposition explains a central empirical fact in the original PAL experiments: a sibling-listwise objective and parent-normalized path score are aligned with the long-horizon construction distribution, whereas raw scores compared across unrelated parents are not.

For beam search this identity is not itself a deterministic speedup theorem, but it identifies the correct distributional objective.  Top-of-beam enrichment is a natural operational diagnostic because it measures whether high continuation mass is concentrated into the retained frontier.

---

## 4. Continuation mass factors through contextual residuals

AEG Paper IV defines contextual continuation equivalence by

\[
p\equiv_Cp'
\iff
O_C(p\cdot\eta)=O_C(p'\cdot\eta)
\quad\forall\eta.
\]

Suppose terminal utility is a function of the declared future observation,

\[
u(\ell)=g(O_C(\ell)),
\]

and equivalent states use the same continuation-word measure/counting convention.

### Proposition 4.1 — residual sufficiency for continuation mass

If

\[
s\equiv_Cs',
\]

then

\[
\boxed{H(s)=H(s').}
\]

Consequently the continuation mass factors through the exact residual quotient

\[
\mathcal R_C=S/\!\equiv_C.
\]

When action labels descend to the quotient, the exact parent-local law also factors through it:

\[
\boxed{
P^*(c\mid s)=P^*([c]\mid[s]).
}
\]

**Interpretation.**  The ideal search policy does not require the literal history.  It requires only distinctions in the past that can alter the declared future continuation experiment.

This gives a precise version of the statement that search difficulty can depend strongly on representation: a representation that approaches the continuation residual can discard large amounts of history while preserving the information needed to order futures.

---

## 5. A multi-predicate continuation kernel

A single scalar mass does not characterize *how* a state can continue.  Let `pi` index future predicates or outcome/certificate types.  Define predicate-specific utility

\[
u_\pi(\ell)\ge0
\]

and mass

\[
H_\pi(s)=\sum_{\ell\succeq s}u_\pi(\ell).
\]

Let `H_0` be a positive reference mass and define the normalized continuation kernel

\[
\boxed{
K(s,\pi)=\frac{H_\pi(s)}{H_0(s)}.
}
\]

Examples in the current categorification search include future predicates such as

- survives D structural coherence;
- survives D amplitude closure;
- reaches E;
- reaches F-linear coherence;
- belongs to a particular exact certificate family;
- reaches a specified defect/rank stratum.

If the chosen predicate family separates the future behaviors relevant to the experiment, then the row

\[
K(s,\cdot)
\]

is a coordinate representation of the selected contextual residual.  Total mass `H_0(s)` and normalized profile `K(s,.)` separate two logically different quantities:

\[
\boxed{
\text{how much viable future remains}
\quad\text{vs.}\quad
\text{what kind of future remains}.
}
\]

---

## 6. PAL as a projective factorization of the continuation kernel

The original Complex-Hermitian PAL implementation encodes a state by

\[
z_s\in\mathbb C^d,
\qquad \rho_s>0,
\]

and a predicate by

\[
c_\pi\in\mathbb C^d.
\]

Its normalized relation is

\[
q_\pi(s)=
\frac{|c_\pi^\dagger z_s|^2}
{\|c_\pi\|^2\|z_s\|^2}.
\]

Define Hermitian rank-one projectors

\[
P_s=\frac{z_sz_s^\dagger}{\|z_s\|^2},
\qquad
E_\pi=\frac{c_\pi c_\pi^\dagger}{\|c_\pi\|^2}.
\]

Then

\[
\boxed{
q_\pi(s)=\operatorname{tr}(P_sE_\pi).
}
\]

Hence the PAL relation depends only on projective directions

\[
[z_s]\in\mathbb{CP}^{d-1},
\qquad[c_\pi]\in\mathbb{CP}^{d-1},
\]

not on their nonzero complex scales.

This gives a concrete interpretation of PAL as a constrained low-dimensional projective factorization of a future-predicate kernel.

### Relation to PCRG

PCRG uses the more general rank-one idempotent

\[
\Pi=\frac{v\otimes\phi}{\phi(v)}.
\]

The PAL Hermitian geometry should therefore be viewed as a positive/Hermitian specialization of the broader point--dual bivaluation geometry, not as the whole PCRG structure.  This distinction matters: future versions may need genuinely non-Hermitian point/covector pairs if the residual geometry cannot be represented faithfully by Hermitian incidence alone.

---

## 7. A falsifiable point/radius semantics

The preceding sections suggest the following empirical hypothesis, not a theorem about the current network:

\[
\boxed{
\rho_s\ \text{should encode total continuation mass,}
\qquad
[z_s]\ \text{should encode normalized future type.}
}
\]

A concrete calibration is

\[
\log\rho_s\approx a+b\log H_0(s),
\]

while projective distances should predict distances between normalized continuation profiles `K(s,.)`.

The current PAL scorer does **not** force this semantic separation: `rho` is learned only through the final score.  Therefore a stronger PAL residual model should add explicit auxiliary objectives, for example

\[
L_{\rm mass}=\big(\log\rho_s-\operatorname{stopgrad}(\log H_0(s))\big)^2
\]

and a multi-predicate projective loss fitting `K(s,pi)`.

This would turn the point/radius interpretation from post-hoc analogy into a directly testable representation claim.

---

## 8. Consequence for the original PAL question

The original practical question was:

> Can PAL accelerate hard / NP-hard search without entering the correctness path?

The refined theoretical question is:

> Does the search problem admit a substantially compressed future-continuation residual, and can a learned projective representation approximate that residual well enough to concentrate continuation mass into a narrow search frontier?

This suggests the mechanism

\[
\boxed{
\text{explicit history}
\to
\text{future residual}
\to
\text{projective condensation}
\to
\text{continuation-mass concentration}
\to
\text{search acceleration}.
}
\]

Worst-case complexity need not change.  The potential gain comes from reducing *effective search entropy* under the problem distribution.

A useful quantitative object is the entropy of the exact local continuation law

\[
\mathcal H(s)=-\sum_cP^*(c\mid s)\log P^*(c\mid s).
\]

A good learned policy should approach this law with small conditional KL while maintaining low inference overhead.  Beam survival then depends on whether high-mass paths have sufficiently low accumulated surprisal to remain inside the beam.

---

## 9. Immediate tests in R(2,2)

The auxiliary experiment should remain outside the theorem path.

1. Use the already-closed epsilon-plus family to test parent-local continuation-mass distillation with `experiments/r22_pal_continuation_mass_probe.py`.
2. Once the fresh epsilon-minus audit stabilizes, export exact failure depth/certificate traces and replace the local-rank proxy with a true graded continuation utility.
3. Compare PAL, real MLP, linear, nearest-neighbor, and cheap handcrafted exact features at matched capacity.
4. Measure top-k continuation-mass enrichment and exact-algebra work before reaching the deepest surviving branch.
5. Explicitly test the point/radius hypothesis:
   - `rho` versus `log H`;
   - projective distance versus continuation-profile distance;
   - transfer across held-out scalar components and certificate families.

Only if these transfer diagnostics hold should the phrase **learned projective contextual residual** be promoted from a research hypothesis to a substantive theory claim.
