# R(2,2) Open Categorification Attack — Scale and Localization Audit

**Status:** active open-problem attack / exact-combinatorial audit  
**Date:** 2026-08-17

## 0. Research criterion

The earlier Fibonacci/string-net benchmark closed the question whether an *un-enriched explicit history representation* by itself gives a new exact invariant or a complexity advantage over optimized categorical/graphical formulations. This note reopens exact fusion-category work under a different success criterion:

> use operation-history organization as a **solver coordinate system** for a fusion ring whose categorifiability is currently unresolved.

The target is the self-dual rank-six ring `R(2,2)` from Meng--Yu (2026). The success condition is not a speedup. It is either:

1. construct invertible associator data satisfying every pentagon, hence a categorification; or
2. derive a rigorous obstruction excluding categorification.

Everything below is therefore a *localization/attackability audit*, not a claim that the history complex is a new categorical invariant.

---

## 1. Frozen fusion ring

Use simples

\[
\{1,g,h,k,X,Y\},\qquad k=gh,
\]

with invertibles forming \(V_4\), `h` stabilizing `X,Y`, while `g,k` exchange them, and

\[
X^2=Y^2=1+h+2X+2Y,
\]

\[
XY=YX=g+k+2X+2Y.
\]

The implementation in `experiments/r22_scale_audit.py` checks associativity of the based ring before constructing any coherence equations.

**COMPUTATIONAL-CLAIM.** The fusion matrix of \(X\) has characteristic polynomial

\[
\lambda^2(\lambda^2-2)(\lambda^2-4\lambda-2),
\]

so

\[
\operatorname{FPdim}(X)=2+\sqrt6,
\qquad
\operatorname{FPdim}(R(2,2))=24+8\sqrt6.
\]

The exact SymPy result is cross-checked numerically with NumPy.

---

## 2. Raw associator scale

There are 48 nonzero trivalent fusion spaces:

- 40 of multiplicity one;
- 8 of multiplicity two.

Before strict-unit normalization the local associator inventory is

\[
256\times1,\quad128\times2,\quad8\times8,\quad8\times10,
\]

for 400 nonzero F-blocks and 2080 scalar matrix entries.

After removing associators with a unit among the three inputs:

\[
\boxed{273\text{ F-blocks},\qquad1881\text{ scalar entries}.}
\]

A direct four-input enumeration gives 3168 nonzero pentagon blocks and 84096 scalar matrix equations. Restricting to four non-unit external inputs leaves

\[
\boxed{1833\text{ pentagon blocks},\qquad76185\text{ scalar equations}.}
\]

**RESEARCH DECISION.** A global symbolic solve at this representation level is rejected. The issue is algebraic elimination, not evaluation cost.

---

## 3. History-layer decomposition

Classify a non-unit F-block \(F^{abc}_d\) by the number of noninvertible inputs among \(a,b,c\) and whether \(d\) is invertible:

| layer | type | blocks | scalar entries |
|---|---|---:|---:|
| A | pointed | 27 | 27 |
| B | one noninvertible, noninvertible output | 54 | 54 |
| C | two noninvertibles, invertible output | 72 | 72 |
| D | two noninvertibles, noninvertible output | 72 | 288 |
| E | three noninvertibles, invertible output | 32 | 128 |
| F | three noninvertibles, noninvertible output | 16 | 1312 |

The pentagon incidence relation is triangular enough to permit staged propagation.

**COMPUTATIONAL-CLAIM.** At block level:

- B closes after one scalar seed;
- C closes after one scalar seed;
- both seeds are movable by residual trivalent gauge from the preceding layer;
- D is completely exposed after 24 local \(2\times2\) seed blocks;
- every E block has a local linear singleton exposure;
- every F block has a local linear singleton exposure.

Thus the largest associators are **not** independent 64- or 100-variable nonlinear subproblems once lower history layers are fixed.

---

## 4. Scalar A/B/C layers: no continuous moduli

For the 153 scalar A/B/C associators, one-dimensional pentagons are multiplicative equations. Write their exponent matrix as

\[
A_{\rm sc}\in M_{729\times153}(\mathbb Z).
\]

`experiments/r22_scalar_audit.py` computes exactly

\[
\operatorname{rank}_{\mathbb Q}A_{\rm sc}=129.
\]

The strict-unit scalar trivalent gauge action has effective rank 24 and lies in the kernel of the pentagon exponent map. Therefore

\[
\boxed{153-129-24=0.}
\]

**COMPUTATIONAL-CLAIM.** There are no continuous scalar A/B/C moduli after gauge.

The Smith normal form has nontrivial invariant factors

\[
\boxed{2,2,2,2},
\]

so the multiplicative solution group modulo its connected gauge orbit has 16 discrete components at this stage.

This should be read as a finite branch inventory for the solver, not as a classification of full categorifications: D/E/F extension can eliminate some or all branches.

### 4.1 Stabilizer sign collapse

Define the gauge-invariant middle-stabilizer scalars

\[
\epsilon_X=F^{hXh}_{X},\qquad
\epsilon_Y=F^{hYh}_{Y}.
\]

Local pentagons give

\[
\epsilon_X^2=\epsilon_Y^2=1.
\]

More strongly, the exponent audit produces an integral two-pentagon witness:

- `(g,h,X,h) -> Y`;
- `(h,g,X,h) -> Y`.

Their quotient cancels the common scalar history and gives

\[
\boxed{\epsilon_X=\epsilon_Y=: \epsilon\in\{+1,-1\}.}
\]

This removes the apparently mixed `(+,-)` and `(-,+)` stabilizer regimes from the D-layer analysis.

---

## 5. D layer: projective involution problem, not 288 free entries

The 24 first-exposed D blocks correspond to the three possible positions of the stabilizer `h` on each of the eight multiplicity-two spaces

\[
V_{MN}^{P},\qquad M,N,P\in\{X,Y\}.
\]

Let the three matrices on one such two-dimensional space be \(L,M,R\).

`experiments/r22_d_layer_probe.py` verifies that the 24 singleton pentagons give projective involution equations. After scalar normalization,

\[
L^2=M^2=R^2=I.
\]

Pair pentagons give

\[
LM=\epsilon ML,\qquad
LR=\epsilon RL,\qquad
MR=\epsilon RM.
\]

Consequently:

- if \(\epsilon=+1\), the three involutions commute and are simultaneously diagonalizable over characteristic zero;
- if \(\epsilon=-1\), they form a two-dimensional Clifford/Pauli triple, with the remaining local distinction a discrete chirality.

**COMPUTATIONAL-CLAIM.** No continuous four-entry freedom survives in an isolated stabilizer seed block after these relations; the D-layer problem becomes a finite projective-representation branch problem plus transport between the eight multiplicity spaces.

The eight spaces split under the elementary pair-flip transports into two size-four orbits, distinguished by parity of the number of `Y` labels.

---

## 6. F layer: a cheap sparse linear problem after lower data are fixed

A first reconnaissance branch sets the scalar A/B/C representative to the trivial one and chooses identity representatives for the compatible D/E lower transports. This is **one branch only**, not a general assumption.

On that branch, every D pentagon and every E pentagon passes exactly. The first failure occurs in the F layer.

A direct SymPy construction of the complete F linear system was deliberately stopped after 120 seconds: it was spending time building expression trees despite the known linearity. `experiments/r22_f_sparse_linear.py` replaces it with a dedicated linear IR (`0 / constant / variable-id`).

The complete F-layer system then has

\[
\boxed{1312\text{ variables},\quad11136\text{ nonzero linear equations}.}
\]

It is generated in under a second on the development machine. Rank calculations modulo two independent large primes agree:

\[
\boxed{\operatorname{rank}=1167,\qquad\operatorname{nullity}=145.}
\]

Every nonzero equation has support two and is simply an equality of two F entries. Contracting these equalities gives

\[
\boxed{145\text{ entry-equivalence components}}
\]

with component-size distribution

\[
128\times8,\qquad16\times16,\qquad1\times32.
\]

### 6.1 Exact obstruction to the trivial lower branch

For each of the eight \(10\times10\) F-blocks, the linear coherence equations identify rows 0 and 1 and also columns 0 and 1. In the canonical fusion-path ordering these are the paths through the two invertible intermediate channels `1` and `h`.

Therefore every such block satisfies

\[
\boxed{\det F^{abc}_{d}=0}
\]

identically on this branch.

**COMPUTATIONAL-CLAIM.** The trivial scalar / identity D-E branch cannot extend to a fusion category because the associator would be noninvertible. This is an exact branch obstruction obtained *before* the final four-noninvertible pentagons.

This is the first useful branch-killing result of the open-problem attack.

---

## 7. What has and has not been achieved

### Established computationally

1. The raw `1881 / 76185` problem has a strong staged dependency structure.
2. Scalar A/B/C data have zero continuous moduli modulo gauge and only finitely many discrete components.
3. The two stabilizer signs are forced equal.
4. D seeds reduce to finite commuting or Clifford-type involution data.
5. The large F layer is linear after lower data are fixed.
6. One natural discrete branch is rigorously excluded by an exact rank defect in every 10-dimensional associator block.

### Not established

1. No categorification or noncategorifiability theorem for `R(2,2)` has yet been proved.
2. The 16 scalar components have not all been extended through D/E/F.
3. The \(\epsilon=-1\) Clifford regime is the next main branch, but a complete exact extension/obstruction has not yet been frozen.
4. The final four-noninvertible pentagons have not yet been reduced to their minimal kernel for every surviving branch.

---

## 8. Next attack

The next computation should **not** rebuild the global pentagon system. It should branch on the finite scalar components and proceed locally:

1. choose a representative scalar A/B/C component;
2. classify/gauge-fix its D stabilizer triples;
3. propagate the remaining D blocks by local intertwiner equations;
4. solve E blocks linearly;
5. generate the F-layer sparse linear system and reject any branch whose required F blocks are singular;
6. only for surviving branches, compile the four-noninvertible pentagons into a reduced exact polynomial kernel.

A branch is worth passing to numerical reconnaissance only after these exact local filters.

The research question has therefore changed from

\[
\text{“can we solve 1881 unknowns?”}
\]

to

\[
\boxed{\text{“which finite coherence branch, if any, survives exact local extension?”}}
\]

That is the current open-problem attack surface.
