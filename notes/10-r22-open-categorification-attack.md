# Note 10 — Open-problem attack on `R(2,2)`

**Status:** research note / candidate obstruction / literature quantifier audit pending  
**Date:** 2026-08-17

---

## 0. Why this line reopens the exact-category program

The preceding Fibonacci/string-net program closed the question

> does an un-enriched explicit history representation give a new invariant or
> an intrinsic complexity advantage over optimized categorical methods?

with a negative answer at the tested scales.

The present line asks a different question:

> can an operation-history/symmetry reduction solve a categorification problem
> whose answer is currently unknown?

Meng--Yu (arXiv:2608.06064, 2026) leave three rank-six
`V4 = C2 x C2`-quadratic fusion rings whose categorifiability is not resolved in
that work.  We attack the smallest self-dual case `R(2,2)`.

Success is no longer measured by variable count.  A genuine success is either

- a construction of a fusion category with Grothendieck ring `R(2,2)`, or
- a rigorous obstruction proving that `R(2,2)` is not categorifiable.

---

## 1. Exact fusion ring

Write

\[
V_4=\{1,g,h,k=gh\},
\]

and let the noninvertible simples be `X,Y`.  For `R(2,2)`:

\[
gX=Y,\qquad hX=X,\qquad kX=Y,
\]

with the same action on `Y`, and

\[
X^2=Y^2=1+h+2X+2Y,
\]

\[
XY=YX=g+k+2X+2Y.
\]

`experiments/r22/fusion_ring.py` verifies associativity directly from the
integer fusion tensor.

The noninvertible Frobenius--Perron dimension is

\[
\boxed{d=2+\sqrt6},
\qquad d^2=4d+2,
\]

and

\[
\boxed{\operatorname{FPdim}(R(2,2))=24+8\sqrt6}.
\]

The exact characteristic polynomial of multiplication by `X` is

\[
\lambda^2(\lambda^2-2)(\lambda^2-4\lambda-2).
\]

NumPy is used only as a floating-point spectral reconnaissance check; SymPy is
the exact source of truth for these identities.

---

## 2. The distinguished based-ring involution

The based ring has a nontrivial involution

\[
\boxed{\tau(X)=Y,\quad \tau(Y)=X,\quad
\tau|_{V_4}=\mathrm{id}.}
\]

The exact automorphism enumeration in `fusion_ring.py` confirms it as a
based-ring automorphism.

The original categorification problem may therefore be attacked through the
more rigid question:

> If a categorification `C` of `R(2,2)` exists, is the involution `tau`
> forced to lift to an order-two tensor autoequivalence?

This is deliberately stronger than ring symmetry.  A based-ring automorphism
need not lift to a tensor autoequivalence.

---

## 3. Pointed associator is reduced to one bit

For any hypothetical categorification, the pointed subcategory is

\[
\mathcal P\simeq \mathrm{Vec}_{V_4}^{\omega}.
\]

Meng--Yu's Frobenius--Schur indicator analysis in the self-dual case gives

\[
\nu_2(h)=+1,
\qquad
\nu_2(g)=\nu_2(k)=\pm1.
\]

The finite cohomology calculation in
`experiments/r22/module_symmetry.py` independently verifies

\[
H^3(V_4,\mathbb C^\times)\cong(C_2)^3,
\]

and that restriction to the three order-two subgroups gives a bijection

\[
[\omega]\longmapsto
(\omega(g,g,g),\omega(h,h,h),\omega(k,k,k))
\in\{\pm1\}^3.
\]

Thus Meng--Yu's indicator constraints leave only

\[
\boxed{(+,+,+)\quad\text{or}\quad(-,+,-).}
\]

The second class is the pullback of the nontrivial class of

\[
V_4/\langle h\rangle\cong C_2.
\]

So the pointed associator uncertainty is only a single binary choice.

---

## 4. The noninvertible sector is a transitive pointed module

Let

\[
\mathcal M=\langle X,Y\rangle.
\]

As a left `P`-module category it is the transitive `V4`-set

\[
V_4/\langle h\rangle,
\]

with stabilizer

\[
H=\langle h\rangle.
\]

The nontrivial automorphism of this two-point `V4`-set is precisely

\[
X\leftrightarrow Y.
\]

Using the explicit twisted-module pentagon and the standard module-functor
1-cell equation, `experiments/r22/module_symmetry.py` enumerates all module
autoequivalences for both allowed pointed 3-cocycle classes.

The result is

\[
\boxed{\operatorname{Aut}_{\mathcal P}(\mathcal M)\cong C_2\times C_2}
\]

in both cases, and both autoequivalence classes whose underlying permutation
swaps `X,Y` have order two.

### Consequence

There is **no obstruction at the pointed-module level** to lifting the ring
involution `tau`.

Any remaining obstruction must occur when this module symmetry is required to
respect the multiplication

\[
\mathcal M\otimes\mathcal M
\longrightarrow
\mathcal P\oplus\mathcal M
\]

and the full associator.

This is the first decisive localization of the open problem.

---

## 5. Raw size versus the residual tensor-symmetry kernel

The strict-unit `R(2,2)` associator contains hundreds of nonzero matrix blocks
and roughly two thousand raw matrix entries before gauge reduction.  We do not
attempt a global polynomial solve at this stage.

If the pointed/module symmetry has already been fixed, the additional
tensorator data that can obstruct a tensor lift is concentrated on

\[
X\otimes X,
\quad X\otimes Y,
\quad Y\otimes X,
\quad Y\otimes Y.
\]

`experiments/r22/symmetry_lift_profile.py` finds:

\[
\boxed{16\text{ nonzero }M\otimes M\text{ multiplicity blocks}}
\]

with

\[
\boxed{40\text{ raw }GL\text{-matrix parameters}.}
\]

The involution `tau` pairs them into

\[
\boxed{8\text{ block orbits / }20\text{ representative raw parameters}.}
\]

This is the natural next local equation system if the center/condensation
argument below does not already obstruct the lift.

---

## 6. Conditional equivariantization theorem

We now isolate a stronger notion.

### Definition — strict-pointed lift

A **strict-pointed lift** of `tau` is an order-two tensor action

\[
C_2\curvearrowright\mathcal C
\]

whose generator sends `X<->Y` and whose restriction to the pointed subcategory
`P` is monoidally isomorphic to the identity tensor functor.

Assume such a lift exists.

Let

\[
\mathcal D=\mathcal C^{C_2}
\]

be the equivariantization.

The four fixed invertible objects each split into two equivariant simples, so
`D` has eight invertibles.  The free orbit `{X,Y}` gives one noninvertible
simple `rho`, with

\[
\operatorname{FPdim}(\rho)=2d=4+2\sqrt6.
\]

Since

\[
\operatorname{FPdim}(\mathcal D)
=2\operatorname{FPdim}(\mathcal C)
=48+16\sqrt6,
\]

one obtains

\[
\rho^2=\sum_{u\in\widetilde G}u+8\rho.
\]

Hence

\[
\boxed{K_0(\mathcal D)=R(\widetilde G,8),\qquad|\widetilde G|=8.}
\]

Because the action is monoidally trivial on the pointed subcategory,
`\widetilde G` is abelian.  The finite equivariant-structure calculation in
`symmetry_lift_profile.py` gives only

\[
\boxed{\widetilde G\cong C_2^3\quad\text{or}\quad C_4\times C_2.}
\]

Schopieray's Theorem 1.1 in *Categorification of integral group rings extended
by one dimension* implies

\[
R(C_2^3,8)
\]

is not categorifiable.  Therefore:

### Conditional theorem A

If a categorification of `R(2,2)` admits a strict-pointed lift of `tau`, then

\[
\boxed{\mathcal C^{C_2}\text{ is a near-group category of type }
(C_4\times C_2)+8.}
\]

This part of the reduction is considered established modulo routine checking
of the standard equivariantization conventions.

---

## 7. Unique-boson calculation for the target near-group categories

Rowell--Solomon--Zhang describe the Drinfeld centers of the near-group
categories of type

\[
(C_2\times C_4)+8.
\]

For the invertible central objects `a_g`, the boson condition is governed by
the order-two elements and the defining nondegenerate symmetric bicharacter.
For `G=C2 x C4`, the relevant bicharacters have parameter `m=+/-1`.

`experiments/r22/near_group_bosons.py` evaluates the self-pairing exactly.
For the three nontrivial order-two elements

\[
(1,0),\quad(0,2),\quad(1,2),
\]

the self-pairings are, for either sign of `m`,

\[
\boxed{-1,\quad+1,\quad-1.}
\]

Thus each of the four near-group monoidal classes considered in the
near-group-center literature has exactly one nontrivial invertible boson:

\[
\boxed{a_{(0,2)}.}
\]

Consequently there is only one Tannakian subcategory

\[
\operatorname{Rep}(C_2)\subset Z(\mathcal D)
\]

generated by an invertible simple object.

---

## 8. Candidate obstruction via uniqueness of de-equivariantization

Equivariantization/de-equivariantization are inverse constructions when the
canonical Tannakian `Rep(G)` in the center is retained as part of the data.
Thus a `C2` action on `C` producing `D=C^{C2}` determines a canonical

\[
\operatorname{Rep}(C_2)\subset Z(\mathcal D),
\]

and de-equivariantizing `D` by that Tannakian subcategory recovers `C` up to
tensor equivalence.

But for the candidate target `D` above, the preceding calculation says the
nontrivial boson, and hence the possible invertible Tannakian `Rep(C2)`, is
unique.

Meng--Yu construct a de-equivariantization of a near-group category of type

\[
(C_2\times C_4)+8
\]

whose Grothendieck ring is `R'(2)`.

This suggests the following obstruction.

### Candidate-new theorem B

> No categorification of `R(2,2)` admits a strict-pointed tensor lift of the
> involution `X<->Y`.

### Proposed proof skeleton

1. Assume such a lift exists.
2. By Conditional theorem A,
   \[
   D=C^{C_2}
   \]
   is of near-group type `(C4 x C2)+8`.
3. The canonical `Rep(C2) subset Z(D)` is generated by a nontrivial invertible
   boson.
4. The center of every relevant `(C4 x C2)+8` near-group monoidal class has
   exactly one such boson.
5. Therefore the de-equivariantization that inverts the assumed action is the
   unique bosonic `C2` de-equivariantization.
6. Meng--Yu's construction identifies that de-equivariantization with fusion
   ring `R'(2)`.
7. But the assumed inverse de-equivariantization must have fusion ring
   `R(2,2)`, a contradiction.

### Critical audit point

Step 6 requires an exact quantifier check of Meng--Yu Corollary 5.8:

- if Corollary 5.8 asserts the `R'(2)` de-equivariantization for **every**
  monoidal class of `(C2 x C4)+8` near-group categories, Candidate theorem B
  closes;
- if it asserts only existence for a selected near-group monoidal class, the
  four classes must be checked individually before the contradiction is
  valid.

Until that quantifier is checked from the primary text, Theorem B remains
`CANDIDATE-NEW`, not a theorem of the repository.

---

## 9. Why this is an AEG-relevant attack even if the obstruction is classical

None of the ingredients above should be advertised as a new categorical
formalism:

- group cohomology,
- module categories,
- equivariantization,
- near-group categories,
- Drinfeld-center bosons

are classical.

The AEG contribution under test is methodological:

\[
\boxed{
\text{large global coherence problem}
\to
\text{explicit history/symmetry stabilizer}
\to
\text{module orbit}
\to
\text{small tensor-lift kernel}
\to
\text{center obstruction}.
}
\]

The original pentagon existence problem is not solved by brute-force algebra;
it is converted into a chain of increasingly rigid local/history questions.
If Candidate theorem B closes and subsequently the remaining non-strict lift
branches can also be excluded, this strategy will have produced a genuinely
new answer to an open categorification problem.

---

## 10. Immediate next tasks

### G1 — close the Corollary 5.8 quantifier

Read Meng--Yu's primary source at the statement/proof of Corollary 5.8 and
record exactly whether the de-equivariantization result is universal across all
`(C2 x C4)+8` near-group monoidal classes.

### G2 — audit the unique-boson theorem against the primary center formulas

Record the exact Rowell--Solomon--Zhang proposition giving the twist/boson
criterion for the invertibles `a_g`, and confirm that all four monoidal classes
use only the two bicharacter signs already enumerated.

### G3 — if Candidate theorem B closes, remove the strict-pointed branch

Then any possible categorification of `R(2,2)` must have either

- no tensor lift of `tau`, or
- a lift whose restriction to the pointed category is a genuinely nontrivial
  monoidal autoequivalence.

This is a major structural restriction.

### G4 — attack the remaining 20-parameter `M x M` lift kernel

If the center argument does not close, generate the tensor-functor coherence
system only on the eight `tau`-orbits of `M x M` multiplicity blocks.  Use:

1. SymPy exact symbolic equations;
2. NumPy/SciPy Jacobian/rank reconnaissance only after gauge fixing;
3. exact algebraic recognition and substitution for any numerical candidate.

Do not return to a global raw pentagon solve unless this localized kernel
provably fails to decide the lift.
