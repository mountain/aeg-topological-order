# R(2,2) theorem audit — second D-amplitude sheet through Phase 4

**Status:** `EXACT / ALL 16 SECOND-SHEET BRANCHES F_PASS`

This note freezes the second physical D-amplitude sheet through the complete
parametric F-linear gate.  Together with the first D sheet, all 32 gauge-
inequivalent deep D classes now pass Phases 1--4.

The second sheet is generated uniformly by the non-gauge Smith-torsion sign
twist of the common 168-by-48 cross-D amplitude lattice.  It flips exactly eight
cross-D amplitudes on every scalar/chirality branch.  Phase 3 showed that all 16
second-sheet branches retain the same two-dimensional invertible E torus.  The
present audit asks whether the complete 1312-entry F-linear coherence quotient
changes on that sheet.

## 1. Exact Phase-4 method

For each second-sheet branch the replay rebuilds, from scratch:

1. the exact class-1 D data and all 1728 D-layer entries;
2. the complete E system with 1536 support-two equations and its two free roots;
3. all 32 required E determinant monomials;
4. the complete F-linear system on 1312 entries;
5. every weighted-component cycle condition over the E torus;
6. all sixteen required 8x8/10x10 F determinant polynomials;
7. the generic E-ratio stratum and every finite root-of-unity ratio stratum.

No floating-point solve, Gröbner basis, or selected E point is used in the
Phase-4 invertibility statement.

The four deep scalar components were replayed in separate CI jobs to preserve
the ten-minute per-job guardrail.

## 2. Components 5 and 13: 21-component type

For every chirality mask

```text
0, 105, 150, 255
```

on components `5` and `13`, the second D sheet gives exactly

```text
F equations                    = 15744
F support                      = {2: 15744}
F component condition profile = {'free': 21}
E-ratio modulus                = 4
generic active F components    = 21
generic bad required blocks    = []
finite strata                  = 4 x (21 active, 0 bad)
```

The required determinant term-count multiset is

\[
8\times123 + 8\times1339.
\]

The generic stratum and all four fourth-root ratio strata are simultaneously
invertible:

```text
generic, zeta_4^0, zeta_4^1, zeta_4^2, zeta_4^3
```

Within each scalar component all four chirality masks have one and only one
Phase-4 fingerprint variant.

Actions runs:

- component 5: `32282061975`;
- component 13: `32282933145`.

## 3. Components 7 and 15: 17+4 type

For every chirality mask on components `7` and `15`, the second D sheet gives

```text
F equations                    = 15744
F support                      = {2: 15744}
F component condition profile = {'free': 17, 'forced': 4}
E-ratio modulus                = 4
generic active F components    = 17
generic bad required blocks    = []
finite strata                  = 4 x (17 active, 0 bad)
```

Every one of the sixteen required F determinant polynomials has exactly 123
terms on the generic stratum.  Again, the generic stratum and all four fourth-
root ratio strata are simultaneously invertible.

Within each scalar component all four chirality masks have one and only one
Phase-4 fingerprint variant.

Actions runs:

- component 7: `32282669278`;
- component 15: `32283488267`.

## 4. Structural conclusion

The genuine D-amplitude `Z2` changes exact lower-layer phases but, through
Phase 4, does **not** change the combinatorial coherence skeleton.

Across both physical D sheets the deep frontier is organized into the same two
Phase-4 types:

\[
\boxed{5,13:\ 21\text{ active F components}}
\]

and

\[
\boxed{7,15:\ 17\text{ active}+4\text{ forced-zero F components}.}
\]

Therefore all

\[
4\text{ scalar components}\times4\text{ chirality masks}\times2\text{ D classes}
=\boxed{32}
\]

deep branches retain invertible loci through the complete F-linear gate.

This result does **not** imply that the Phase-5 nonlinear kernels on the two D
sheets are identical.  Exact phases can change the final cubic relations even
when the weighted F graph and determinant supports agree.

## 5. Next gate

The highest-information Phase-5 probe is

\[
\boxed{\text{component 7 / mask 0 / D-amplitude class 1}.}
\]

Component 7 belongs to the `17+4` type.  On D class 0 all four chirality masks
were killed by a fixed pair of final-pentagon provenances, giving a coordinate-
free contradiction of the form

\[
z=0,\qquad z^2-\frac12=0.
\]

The next gate must fresh-compile the class-1 nonlinear kernel and ask whether
those same provenances still yield that obstruction.  No class-0 coordinate
name or polynomial identity may be imported by assumption.
