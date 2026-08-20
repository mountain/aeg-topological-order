# R(2,2) second D sheet — component 13 / mask 105 Phase-5 closure

## Status

**CLOSED / EXACT.**

This note freezes the theorem-audit closure of scalar component `13`, chirality mask `105`, physical D-amplitude class `1`.  No class-0 coordinate identity or terminal certificate is assumed; every decisive relation below was recompiled on the second D sheet and checked by final-pentagon provenance.

## Fresh nonlinear kernel

The class-1 Phase-5 kernel has:

- 21 active F components;
- 23 variables;
- 50,880 raw nonzero final entries;
- 219 unique cubic kernel polynomials;
- F-degree profile `57 x degree-2 + 162 x degree-3`;
- no constant contradiction.

Fresh fingerprint: Actions run `32365679843`.

## Five-cell finite-scale model

The fixed source cells

```text
(XXXXX)_(0,0)
(XXXXX)_(0,2)
(XXXXY)_(0,18)
(XXXXY)_(18,18)
(XXXX1)_(0,0)
```

were source-validated on D class 1 and imply, before any unsafe localization,

\[
P_5-P_2-iP_3=\frac{1+i}{8}(2z_0^2-1).
\]

Hence

\[
\boxed{z_0^2=\frac12}.
\]

The remaining exact relations give

\[
\boxed{p^3=\frac{-1+i}{4}},\qquad
\boxed{q^3=\frac{1-i}{4}},
\]

and

\[
\boxed{z_3z_{10}=-ip^2z_0},\qquad
\boxed{z_6z_9=-q^2z_0}.
\]

Therefore `p,q,z0,z3,z6,z9,z10` are nonzero.  Source gate: Actions run `32367286396`.

## Exact 18-stratum census

After eliminating only `z10` and `z9` with the proved product identities and localizing only at proved-nonzero `z3,z6`, the exact census is

\[
\boxed{18=2+4+4+8}.
\]

More precisely:

- 2 branches `(a,b)=(0,0)` are affine-inconsistent;
- 4 p-side rank-11 branches `(a,b)=(1,0),(2,0)` force `z7=z8=0`;
- 4 q-side rank-11 branches `(a,b)=(0,1),(0,2)` force `z11=z18=0`;
- 8 branches `(a,b)=(1,1),(2,1),(1,2),(2,2)` have rank 10 and no forced zero.

Fresh census: Actions run `32367554907`.

## Terminal source certificates

A representative residual probe (run `32367832253`) identified the class-1 terminal geometry.

### p-side rank 11

The fixed provenance

\[
\boxed{(XXXX;Y)_{(1,0)}}
\]

reduces in all four branches to a nonzero exact scalar times `z3`.  Since `z3 != 0`, all four branches are excluded.

### q-side rank 11

The fixed provenance

\[
\boxed{(XXXXX)_{(5,2)}}
\]

reduces in all four branches to a nonzero exact scalar times `z6`.  Since `z6 != 0`, all four branches are excluded.

### rank 10

The affine quotient leaves

```text
z3,z4,z5,z6,z17,z18,z19,z20
```

free, with a two-variable terminal core

\[
r=z_{17},\qquad s=z_{18}.
\]

The same three source cells are used on all eight branches:

```text
G3 = (XXXX;g)_(0,3)
G2 = (XXXX;g)_(0,2)
G0 = (XXXX;g)_(0,0)
```

For each branch, `G3+G2` factors as

\[
s(a+bs),\qquad a,b\ne0.
\]

Thus there are exactly two exact `s` candidates.  `G3` is linear in `r` on each candidate and fixes `r`; the two anchors vanish at those reconstructed points, while the fixed third cell `G0` is nonzero at both.  Hence every rank-10 branch is excluded.

Full terminal replay: Actions run `32368154629`, summary

```text
affine_inconsistent = 2
p_rank11_closed     = 4
q_rank11_closed     = 4
rank10_closed       = 8
finite_total        = 18
```

Therefore

\[
\boxed{\text{component 13 / mask 105 / D class 1 is CLOSED / EXACT}.}
\]

## Frontier after this checkpoint

The second D-amplitude sheet is now closed on 14 of 16 deep Phase-5 branches.  The only remaining branches are

\[
\boxed{13/150,\qquad 13/255.}
\]

PR `#12` remains draft.  This checkpoint does not promote the global non-categorifiability theorem; seed-normal-form completeness and the final exhaustive theorem replay remain separate gates.
