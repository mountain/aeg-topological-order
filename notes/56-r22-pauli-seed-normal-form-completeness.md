# R(2,2) theorem audit — Pauli seed normal-form completeness

## Status

**CLOSED / EXACT.**

The epsilon-minus D-layer chirality census is now proved projectively exhaustive.  The historical use of Pauli/Clifford seed matrices is not an ansatz.

## 1. The gap being audited

For every two-dimensional multiplicity space `V_{MN}^P`, the downstream D-layer engine used the three stabilizer seed matrices

\[
L=X,\qquad M=Z,\qquad R=\chi Y,\qquad \chi\in\{\pm1\}.
\]

Before this audit, the original pentagon engine had verified these matrices as exact witnesses, but it had not established that every invertible seed solution was gauge-equivalent to this form.

The theorem-level question was therefore:

> Does every invertible solution of the original seed-only D pentagons, over each canonical deep epsilon-minus scalar component, become `(X,Z,+Y)` or `(X,Z,-Y)` after an allowed independent `GL_2(C)` basis change on the corresponding multiplicity-two fusion space?

## 2. Exhaustion of the seed-only D equations

`experiments/r22_epsminus_seed_pauli_normal_form_audit.py` reconstructs the D-layer equations directly from the multiplicity-aware pentagon engine.

It finds exactly

\[
\boxed{48\text{ seed-only D pentagons}}
\]

and proves that they are exhausted by

\[
\boxed{24\text{ singleton equations}+24\text{ pair equations}.}
\]

There are no additional seed-only D pentagons outside this list.

The 24 seed D blocks are organized as three roles

\[
L,M,R
\]

on each of the eight multiplicity-two fusion spaces.  Using the original source/target fusion paths, the verifier confirms for every seed block that the unique multiplicity-two vertex on the source side and the unique multiplicity-two vertex on the target side are the same underlying fusion space.  Therefore the allowed independent `GL_2(C)` gauge acts by ordinary conjugation on the seed triple.

## 3. Singleton pentagons force genuine involutions

For each deep scalar component

\[
\boxed{5,7,13,15}
\]

and each of the 24 singleton seed equations, the verifier substitutes a fully generic matrix

\[
U=\begin{pmatrix}u_{00}&u_{01}\\u_{10}&u_{11}\end{pmatrix}
\]

into the original pentagon and compares the resulting polynomial matrix with `U^2-I` and `U^2+I`.

All

\[
4\times24=96
\]

cases give a nonzero scalar multiple of

\[
\boxed{U^2-I=0}.
\]

The exact Actions profile is

```text
singleton_square_profile = {1: 96}
```

so no hidden `U^2=-I` branch remains.

Hence on every multiplicity-two space,

\[
\boxed{L^2=M^2=R^2=I}.
\]

## 4. Pair pentagons force the Clifford relations

For every deep scalar component, every one of the eight multiplicity-two spaces, and every pair among `(L,M,R)`, the verifier substitutes three independent generic `2x2` matrices into the original pair pentagons.

There are

\[
4\times8\times3=96
\]

such equations.  Each one is tested exactly against both a commutator and an anticommutator model.

The result is

```text
pair_relation_profile = {'anticommute': 96}
```

with every pair equation a nonzero scalar multiple of its anticommutator.  Therefore

\[
\boxed{LM+ML=0},
\qquad
\boxed{LR+RL=0},
\qquad
\boxed{MR+RM=0}.
\]

Together with the singleton result, every invertible seed triple satisfies the exact rank-two complex Clifford relations

\[
L^2=M^2=R^2=I,
\qquad
\{L,M\}=\{L,R\}=\{M,R\}=0.
\]

## 5. Elementary `GL_2(C)` normal-form lemma

The remaining classification is elementary and is also checked symbolically in the verifier.

Because `M^2=I` and `M` anticommutes with an invertible `L`, `M` cannot be scalar.  Hence it is diagonalizable with eigenvalues `+1,-1`, so after conjugation

\[
M=Z.
\]

Anticommutation with `Z` forces

\[
L=\begin{pmatrix}0&a\\b&0\end{pmatrix}.
\]

The equation `L^2=I` gives `ab=1`.  The residual diagonal conjugation

\[
G=\operatorname{diag}(a,1)
\]

preserves `Z` and sends `L` to

\[
X.
\]

A matrix anticommuting with both `Z` and `X` has the form

\[
R=\begin{pmatrix}0&u\\-u&0\end{pmatrix}.
\]

Then `R^2=I` gives

\[
u^2=-1,
\]

so over `\mathbf C`

\[
u=\pm i
\]

and therefore

\[
\boxed{R=\pm Y}.
\]

Thus every invertible seed solution is independently `GL_2(C)`-conjugate to

\[
\boxed{(L,M,R)=(X,Z,+Y)\text{ or }(X,Z,-Y)}.
\]

## 6. Consequence for the chirality census

There are eight multiplicity-two fusion spaces.  Each contributes only the discrete sign

\[
\chi\in\{\pm1\}
\]

after projective gauge normalization.  Therefore the full seed mod-gauge frontier is contained in

\[
\boxed{2^8=256}
\]

chirality assignments.

The existing fresh D trace already enumerates all 256 assignments and reduces them exactly to the four masks

\[
\boxed{0,105,150,255}.
\]

Hence that Phase-1 chirality census is now theorem-level exhaustive rather than a Pauli ansatz restricted search.

## 7. Executable replay

Verifier:

```text
experiments/r22_epsminus_seed_pauli_normal_form_audit.py
```

GitHub Actions:

```text
run 32394416585
job 96507814387
conclusion SUCCESS
```

The decisive output is

```text
seed_only_D_pentagons = 48
seed_blocks_verified_as_GL2_conjugation_endomorphisms = 24
singleton_square_profile = {1: 96}
pair_relation_profile = {'anticommute': 96}
```

followed by

```text
RESULT: every invertible epsilon-minus seed solution is independently GL2(C)-conjugate on each 2D multiplicity space to (X,Z,+/-Y); the 2^8 Pauli chirality census is projectively exhaustive
```

## 8. Theorem boundary after this gate

The local/projective completeness gap before the chirality census is now closed.  Together with the full complex scalar inventory, the exact chirality trace, the two physical D-amplitude sheets, and the Phase-5 terminal obstructions, every currently identified local branch of the coherence problem is represented in the proof ledger.

The next theorem node is no longer a new local algebra search.  It is **global proof bookkeeping and replay**:

1. freeze an executable exhaustive case ledger from the 16 scalar components through terminal contradiction;
2. run the canonical theorem replay from fresh state in serial theorem gates;
3. synthesize the theorem statement only after the ledger and replay agree.

No global non-categorifiability theorem is promoted by this note alone.
