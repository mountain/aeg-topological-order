# R(2,2) theorem audit — shallow epsilon-minus local-F closure

## Status

**CLOSED / EXACT / FRESH RECONSTRUCTION.**

The canonical epsilon-minus scalar components

\[
\boxed{4,6,12,14}
\]

are independently obstructed before cross-D amplitudes, E data, or the final four-noninvertible pentagons are needed.

This note replaces the non-executable historical statement retained in the superseded epsilon-minus closure note with a fresh theorem-audit certificate on the current canonical code base.

## 1. Why a reconstruction was required

The historical `notes/15-r22-epsilon-minus-closure.md` was deliberately excluded from canonical `main` because its old D-amplitude family claim was false.  That note separately recorded a later fresh local-F obstruction for components `4,6,12,14`, but the corresponding standalone executable was not promoted into the Phase-1–4 closure.

Therefore a theorem-level proof could not cite the historical sentence alone.  The local obstruction has now been reconstructed independently as

```text
experiments/r22_epsminus_shallow_local_f_obstruction.py
```

from the current full-`C*` canonical scalar representatives and current pentagon engine.

## 2. Inputs of the certificate

The verifier uses only:

1. a canonical scalar A/B/C representative;
2. the epsilon-minus Pauli/Clifford stabilizer-seed normal form;
3. the four pentagons with exactly one external stabilizer `h` and three `X` labels;
4. the required target associator

\[
F^{XXX}_X\in M_{10}(\mathbf C).
\]

It does **not** use:

- cross-D amplitude closure;
- E-layer data;
- any Phase-5 final pentagon;
- floating-point rank tests;
- Gröbner bases or global nonlinear solving.

## 3. Complete local chirality inventory

The four source pentagons are

```text
(h,X,X,X) -> X
(X,h,X,X) -> X
(X,X,h,X) -> X
(X,X,X,h) -> X
```

The script discovers their actual D-seed dependencies from pentagon provenance rather than assuming a chirality subset.  Exactly four multiplicity spaces are read:

```text
(X,X,X)
(X,X,Y)
(X,Y,X)
(Y,X,X)
```

Hence the local target block depends on exactly

\[
2^4=16
\]

Clifford chirality patterns.

All sixteen are enumerated explicitly.  This is the complete local branch inventory relevant to the determinant of `F^{XXX}_X`.

## 4. Exact local-F system

For each canonical scalar component and each local chirality pattern, direct substitution into the four pentagons produces exactly

\[
\boxed{400}
\]

nonzero homogeneous linear relations on the 100 entries of `F^{XXX}_X`.

Every relation has support one or two.  They are therefore solved over characteristic zero by an exact weighted union-find relation graph.  The required determinant is then computed exactly by subset dynamic programming as a polynomial in the surviving weighted-component parameters.

The rejection criterion is not a sample rank defect: a branch is rejected only when the full determinant polynomial is the zero polynomial.

## 5. Shallow components

GitHub Actions run

```text
32258657976
```

reconstructs the local system for all

\[
4\text{ components}\times16\text{ local chiralities}=64
\]

cases and reports:

```text
component 4   nonzero determinant polynomials = []   closed=True
component 6   nonzero determinant polynomials = []   closed=True
component 12  nonzero determinant polynomials = []   closed=True
component 14  nonzero determinant polynomials = []   closed=True
```

Thus, in every case,

\[
\boxed{\det F^{XXX}_X\equiv0}.
\]

Since an associator in a fusion category must be invertible, every one of these 64 local Clifford branches is impossible.

Therefore

\[
\boxed{4,6,12,14\text{ are completely obstructed}.}
\]

## 6. Deep-component negative controls

The same verifier is applied, without changing the local equations or determinant algorithm, to the accepted Phase-1 survivors

\[
\{5,7,13,15\}\times\{0,105,150,255\}.
\]

All sixteen control branches retain a nonzero determinant polynomial.  Each reported determinant polynomial has

```text
1339 monomials
```

under this local quotient.

Therefore the verifier does not trivially declare every epsilon-minus branch singular.  It reproduces exactly the intended shallow/deep separation:

\[
\boxed{4,6,12,14\text{ locally singular};\qquad5,7,13,15\text{ locally pass}.}
\]

This negative control is stronger than merely reproducing the historical shallow verdict.

## 7. Theorem-level consequence

The epsilon-minus scalar inventory is

\[
\boxed{4,5,6,7,12,13,14,15}.
\]

The present certificate closes four components immediately:

\[
\boxed{4,6,12,14}.
\]

The remaining four

\[
\boxed{5,7,13,15}
\]

are precisely the deep frontier carried by the canonical Phase-1–4 replay and the later Phase-5 component closures.

Thus the theorem-closure audit no longer depends on the superseded epsilon-minus note for this partition.

## 8. Proof boundary

This note closes only the shallow epsilon-minus scalar components.  It does not by itself establish the global `R(2,2)` theorem.

The theorem audit must still fresh-replay:

1. the epsilon-plus eight-component obstruction;
2. the scalar quotient and epsilon partition;
3. the complete Phase-1–4 deep-branch reduction;
4. the component `5` and `13` Phase-5 certificates under robust fresh-process replay;
5. the already coordinate-free component `7` and `15` closures;
6. the final case-exhaustiveness ledger.
