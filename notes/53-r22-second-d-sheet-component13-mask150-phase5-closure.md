# R(2,2) second D sheet: component 13 / mask 150 Phase-5 closure

## Status

**CLOSED / EXACT.**

This note records the theorem-audit replay of scalar component `13`, chirality mask `150`, on the second physical D-amplitude class.  The branch was rebuilt from fresh Phase-5 coherence data.  No historical D-sheet coordinate identification or terminal certificate was assumed, and no global Gröbner basis, floating-point root search, numerical continuation, or global nonlinear solve was used.

## 1. Fresh kernel

The second-sheet sparse compiler gives:

- 21 active F components;
- 23 nonlinear variables `p,q,z0,...,z20`;
- 15,744 support-two F-linear equations before the final kernel;
- 50,880 raw nonzero final entries;
- 219 unique cubic kernel relations;
- no generic constant contradiction.

## 2. Source-validated local scale relations

The five fixed provenances

```text
(XXXXX)_(0,0)
(XXXXX)_(0,2)
(XXXXY)_(0,18)
(XXXXY)_(18,18)
(XXXX;1)_(0,0)
```

are source-validated on D-amplitude class `1`.  A first attempted transcription was rejected by the executable source gate because the first product coefficient had been misread from the canonicalized fingerprint.  Returning to the raw source polynomial corrected the relation before any finite-stratum work proceeded.

The exact class-1 relations are

\[
z_6^2=\frac12,
\qquad
p^3=\frac{1-i}{4},
\qquad
q^3=\frac{-1+i}{4},
\]

\[
z_0z_9=-p^2z_6,
\qquad
z_1z_7=q^2z_6.
\]

The scale relation is obtained before localization from

\[
P_5-P_2+P_3=\frac{1-i}{8}(1-2z_6^2).
\]

Hence

\[
p,q,z_0,z_1,z_6,z_7,z_9\ne0.
\]

The successful source replay is GitHub Actions run `32369165871`.

## 3. Exact finite census

Enumerating the three cube roots of `p`, three cube roots of `q`, and two square roots of `z6` gives 18 exact branches.  Only `z9,z7` are eliminated through the proved product identities, and Laurent factors are stripped only in the proved-nonzero coordinates `z0,z1`.

The fresh class-1 census gives

\[
\boxed{18=2_{\rm affine}+4_{\rm p-rank11}+4_{\rm q-rank11}+8_{\rm rank10}}.
\]

More precisely:

- `(a,b)=(0,0)`, both signs: affine inconsistent;
- p-side `(1,0),(2,0)`, both signs: rank 11, forced `z2=z8=0`;
- q-side `(0,1),(0,2)`, both signs: rank 11, forced `z12=z13=0`;
- `(1,1),(2,1),(1,2),(2,2)`, both signs: rank 10, no forced-zero coordinate.

The rank-10 free coordinates are

```text
z0,z1,z10,z11,z15,z16,z18,z20.
```

GitHub Actions run `32380553875` completes the 18-stratum census.

## 4. Terminal source geometry

A representative residual-source probe finds:

- p-side fixed provenance `(XXXX;Y)_(1,0)` becomes a nonzero exact constant;
- q-side fixed provenance `(XXXXX)_(2,5)` becomes a nonzero exact constant;
- the rank-10 core lies in
  \[
  (r,s)=(z_{18},z_{20}).
  \]

The fixed g-cells

```text
G2 = (XXXX;g)_(0,2)
G3 = (XXXX;g)_(0,3)
G0 = (XXXX;g)_(0,0)
```

have normalized anchor forms on every rank-10 branch

\[
G_2\sim1+4rs-4s^2,
\qquad
G_3\sim1+4rs-4r^2.
\]

Subtracting them gives `r^2=s^2`.  On `r=s`, `G2` becomes `1=0`.  On `r=-s`, `G2` gives

\[
s^2=\frac18,
\]

and the fixed third cell `G0` evaluates to a nonzero exact algebraic number on every branch.

Representative probe: GitHub Actions run `32380965082`.

## 5. Complete terminal replay

`experiments/r22_phase5_component13_torsion_mask150_terminal_certificate.py` recompiles the class-1 kernel once and source-validates the complete finite ledger:

\[
2_{\rm affine}+4_{\rm p}+4_{\rm q}+8_{\rm rank10}=18/18.
\]

All four p-side branches are closed by the same fixed nonzero-constant cell, all four q-side branches by the same fixed nonzero-constant cell, and all eight rank-10 branches by the same `G2,G3,G0` source family.

GitHub Actions run `32381418977` reports:

```text
affine_inconsistent = 2
p_rank11_closed      = 4
q_rank11_closed      = 4
rank10_closed        = 8
finite_total         = 18
RESULT: component 13 mask 150 class-1 Phase-5 branch is CLOSED / EXACT
```

Therefore

\[
\boxed{\text{component 13 / mask 150 / D-amplitude class 1 is CLOSED / EXACT}.}
\]

At this checkpoint the second-sheet Phase-5 ledger is `15/16`; only component `13` / mask `255` remains unresolved.
