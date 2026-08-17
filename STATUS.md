# Status

## Stage

`T9 R(2,2) OPEN CATEGORIFICATION ATTACK — localization audit complete; finite-branch extension in progress`

## Why the exact line is reopened

**RESEARCH DECISION.** The earlier exact Fibonacci/string-net program remains closed under its original success criterion: explicit operation history did not produce a new invariant or a complexity advantage over optimized categorical/graphical baselines. That negative result is preserved in `notes/08-graphical-certificate-and-coherence-barrier.md` and `notes/09-stage-closure.md`.

**REFORMULATION.** The line is reopened under a different and stricter criterion: can an operation-history/localization representation solve a categorification problem whose answer is currently unknown? Mathematical equivalence to pentagon coherence is allowed; success now means a new construction or obstruction, not a speedup.

## Open target

**CLASSICAL.** The target is Meng--Yu's rank-six self-dual `R(2,2)` fusion ring in the `V_4`-quadratic family:

\[
\{1,g,h,gh,X,Y\},\qquad gX=Y,
\]

\[
X^2=Y^2=1+h+2X+2Y,
\qquad
XY=g+gh+2X+2Y.
\]

See `references/r22-open-problem.md`.

**SUCCESS CONDITION.** Either construct invertible F-data satisfying every pentagon, or derive a rigorous obstruction to categorification. Reproducing known criteria or merely reducing runtime is not sufficient.

## Exact scale audit

**COMPUTATIONAL-CLAIM.** `experiments/r22_scale_audit.py` verifies the based-ring associativity and obtains

\[
\operatorname{FPdim}(X)=2+\sqrt6,
\qquad
\operatorname{FPdim}(R(2,2))=24+8\sqrt6.
\]

The raw strict-unit associator problem has

\[
\boxed{273\text{ nontrivial F-blocks},\quad1881\text{ scalar entries}}
\]

and the non-unit four-input pentagons contain

\[
\boxed{1833\text{ blocks},\quad76185\text{ scalar matrix equations}.}
\]

**RESEARCH DECISION.** A global SymPy/Gröbner solve at this level is rejected.

## History-layer localization

Split non-unit F-blocks into six dependency layers:

| layer | blocks | scalar entries | role |
|---|---:|---:|---|
| A | 27 | 27 | pointed |
| B | 54 | 54 | one noninvertible |
| C | 72 | 72 | two noninvertibles, invertible output |
| D | 72 | 288 | two noninvertibles, noninvertible output |
| E | 32 | 128 | three noninvertibles, invertible output |
| F | 16 | 1312 | three noninvertibles, noninvertible output |

**COMPUTATIONAL-CLAIM.** Pentagon incidence is sufficiently triangular that B/C close after gauge-fixable scalar seeds; D begins with 24 local 2x2 stabilizer blocks; E/F have local linear singleton exposures once lower layers are fixed.

## Scalar A/B/C result

**COMPUTATIONAL-CLAIM.** `experiments/r22_scalar_audit.py` converts the 729 scalar pentagons to a monomial exponent matrix

\[
A_{sc}\in M_{729\times153}(\mathbb Z),
\qquad
\operatorname{rank}A_{sc}=129.
\]

The effective scalar trivalent-gauge rank is 24, so

\[
\boxed{153-129-24=0.}
\]

There are no continuous scalar A/B/C moduli after gauge.

**COMPUTATIONAL-CLAIM.** Smith normal form leaves

\[
\boxed{(\mathbb Z_2)^4}
\]

at the component level: 16 discrete scalar branches must be extended or excluded.

**COMPUTATIONAL-CLAIM.** The two gauge-invariant stabilizer signs are not independent. Two scalar pentagons give

\[
\boxed{\epsilon_X=\epsilon_Y=: \epsilon,\qquad\epsilon^2=1.}
\]

## D-layer result

**COMPUTATIONAL-CLAIM.** `experiments/r22_d_layer_probe.py` verifies that the 24 first D-layer seed blocks reduce, after scalar normalization, to three involutions on each multiplicity-two fusion space:

\[
L^2=M^2=R^2=I,
\]

\[
LM=\epsilon ML,\quad LR=\epsilon RL,\quad MR=\epsilon RM.
\]

Thus the D seed problem has finite projective-representation types rather than 288 unconstrained scalar entries:

- `epsilon=+1`: commuting involutions;
- `epsilon=-1`: 2D Clifford/Pauli triples with discrete chirality.

The eight multiplicity-two spaces split into two size-four transport orbits by `Y`-parity.

## F-layer sparse linear audit and first branch obstruction

**ENGINEERING NOTE.** A naive complete SymPy construction of the F-layer linear system hit the predeclared 120-second stop limit. It was not allowed to continue. The dedicated sparse linear IR in `experiments/r22_f_sparse_linear.py` constructs the same layer in well under a second on the development machine.

For the simplest reconnaissance branch (`A/B/C` trivial representative and compatible identity D/E transports), the F layer has

\[
1312\text{ entries},\qquad11136\text{ nonzero linear equations}.
\]

Two independent modular-rank checks give

\[
\boxed{\operatorname{rank}=1167,\qquad\operatorname{nullity}=145.}
\]

Every equation is an entry equality. Contracting them gives 145 equivalence components with sizes

\[
128\times8,\qquad16\times16,\qquad1\times32.
\]

**COMPUTATIONAL-CLAIM / BRANCH OBSTRUCTION.** In every one of the eight 10x10 F-blocks, coherence identifies rows 0 and 1 and columns 0 and 1. These correspond to the two invertible intermediate channels `1` and `h`. Hence every such associator is singular.

\[
\boxed{\text{The trivial scalar / identity D-E branch cannot categorify }R(2,2).}
\]

This is an exact branch-killing result, not a numerical-rank guess.

## Current attack surface

**COMPUTATIONAL-CLAIM.** The raw problem should no longer be viewed as an approximately 1900-dimensional nonlinear solve. The current structure is

\[
\boxed{
\text{16 scalar branches}
\to
\text{finite D projective branches}
\to
\text{linear E/F intertwiners}
\to
\text{four-noninvertible consistency kernel}.
}
\]

**ONGOING COMPUTATIONAL-CLAIM.** A concrete `epsilon=-1` scalar representative has been found and its 24 Pauli-type D seeds pass their local pentagons. The remaining 48 D blocks have one-dimensional local intertwiner spaces with invertible representatives. This result is still being promoted into the checked repository experiment and should not yet be treated as the final branch extension.

## Immediate next task

1. Freeze an exact `epsilon=-1` scalar representative from the 16-component scalar system.
2. Enumerate the finite D chiralities and propagate the remaining 48 D blocks exactly.
3. Solve their residual scalar-amplitude consistency as a multiplicative lattice problem.
4. Solve E linearly.
5. Build the F sparse-linear system for each surviving D/E branch and reject singular branches immediately.
6. Only then compile the four-noninvertible pentagons into the final reduced polynomial kernel.

## Compute guardrails

- Do not materialize the full 76185-equation SymPy system.
- Use Python for combinatorial/history incidence, SymPy for exact low-dimensional algebra/Smith forms, and NumPy/SciPy only for reconnaissance.
- A heavy symbolic operation gets an explicit time limit; timeout is evidence to change representation, not to increase the limit automatically.
- Numerical solutions are discovery evidence only. Any categorification or obstruction claim must be frozen by exact verification.

## Research labels / caveat

**CLASSICAL.** The fusion ring and the general categorification problem come from the existing fusion-category literature.

**REFORMULATION.** The A/B/C/D/E/F history layering is a solver organization of ordinary coherence data.

**CANDIDATE-NEW.** The specific localization chain and branch obstruction for `R(2,2)` may become new mathematical content if it survives independent verification and contributes to resolving the open categorifiability question. No originality claim is made yet.
