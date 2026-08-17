# Note 12 — Localized triangular-prism attack on `R(2,2)`

**Status:** active main workstream / exact local algebra complete / TPE compiler dictionary pending  
**Date:** 2026-08-17

---

## 0. Strategic role

The project success criterion has changed.  We are no longer asking whether AEG
is a more economical notation for known categorical coherence.  We are asking
whether a history/localization representation can turn a published
categorifiability `unknown` into a theorem.

The first target is Meng--Yu's unresolved self-dual ring `R(2,2)`.

Two independent attack lines are currently justified:

1. **symmetry obstruction:** the manifest based-ring involution `X<->Y` has
   been shown (candidate-new, pending external audit) not to admit any
   order-two tensor lift;
2. **localized coherence:** use the triangular-prism/string-Fourier
   coordinates of Liu--Palcoux--Ren--Vercleyen to attack a small, highly
   overdetermined subsystem without assuming that symmetry lifts.

This note records the second line.

---

## 1. Why TPE is the right baseline, not a competing strawman

Liu--Palcoux--Ren--Vercleyen prove that for spherical fusion categories the
triangular prism equations (TPE) are equivalent to the pentagon equations up
to a change of basis.  Their point is computational/structural localization:
small overdetermined TPE subsystems can be solved before the full coherence
system is expanded.

Meng--Yu work in the pseudo-unitary/spherical setting for the rank-six
`V4`-quadratic problem, so this spherical localization is applicable to the
hypothetical categories under attack.

The 2025 TPE paper explicitly proposes the following standard localization.
For a self-dual simple object `X`, let

\[
n=\dim\operatorname{End}(X\otimes X).
\]

The string Fourier transform (SFT) introduces `n^2` local matrix entries; the
standard triangular-prism family has `n^3` configurations and roughly
`n^3/3` equations after `C3` rotational symmetry.

The same paper says that a near-group polynomial system based on this viewpoint
is work in progress.  No public standard-prism generator was located; the
paper's public Sage appendix is for a different localization example.  Data are
stated to be available from the authors on reasonable request.

Therefore we implement the index dictionary ourselves, conservatively, from
the published TPE theorem rather than reverse-engineering an unpublished
near-group codebase.

---

## 2. The exact local algebra for `R(2,2)`

The noninvertible self-dual simple `X` satisfies

\[
\boxed{X^2=1+h+2X+2Y}.
\]

Hence

\[
\operatorname{End}(X^2)
\cong
\mathbb C\oplus\mathbb C\oplus M_2(\mathbb C)\oplus M_2(\mathbb C)
\]

as a semisimple algebra and

\[
\boxed{n=1^2+1^2+2^2+2^2=10.}
\]

Thus the first standard-TPE localization introduces only

\[
\boxed{n^2=100}
\]

SFT matrix entries, versus the much larger global associator system.

`experiments/r22/tpe_local_algebra.py` constructs this algebra exactly using
SymPy algebraic numbers.

---

## 3. Normalized I-shaped matrix units

For each simple summand `c` of `X^2`, and multiplicity indices `i,j`, use the
normalized matrix units

\[
\tau_{cij}.
\]

The resolution-of-identity normalization from the TPE paper is

\[
\boxed{
\tau_{cij}\tau_{c'k\ell}
=
\delta_{cc'}\delta_{jk}\,d_c^{-1}\tau_{ci\ell},
\qquad
\operatorname{tr}(\tau_{cij})=\delta_{ij}.
}
\]

There are exactly ten such basis elements:

- one from the `1` block;
- one from the `h` block;
- four from the `X` multiplicity-two block;
- four from the `Y` multiplicity-two block.

The identity is therefore

\[
\boxed{
\operatorname{id}_{X^2}
=
\sum_{c,i}d_c\tau_{cii}.
}
\]

With

\[
d_X=d_Y=2+\sqrt6,
\]

the categorical trace of the identity is `d_X^2`, as required.

---

## 4. Exact trilinear trace tensor

For three I-basis elements,

\[
T(a,b,c)=\operatorname{tr}(abc)
\]

is completely known from the matrix-unit algebra.

Out of

\[
10^3=1000
\]

ordered triples, exactly

\[
\boxed{18}
\]

have nonzero trace.

The values are:

- `1` for the two scalar blocks `1,h`;
- 
  \[
  d_X^{-2}=d_Y^{-2}=\frac52-\sqrt6
  \]

  for the sixteen nonzero `M_2` triples.

Modulo cyclic rotation of the three factors, the 1000 triples form exactly

\[
\boxed{340}
\]

orbits:

- 10 fixed triples;
- 330 length-three orbits.

Exactly 10 of these 340 orbits have nonzero trilinear trace; 330 have zero
trace in the I-shaped matrix-unit algebra.

### Audit boundary

This is **not yet stated as “330 zero TPE equations.”**

What is proved is the sparsity of the known I-basis multiplication/trace tensor.
The standard-prism TPE places this known algebraic side against contractions of
unknown SFT/tetrahedral entries, but the precise normalization and index
orientation must be compiled from Theorem 4.21 before the 340 orbit values are
called equations.

---

## 5. The local block is exactly a large associator block

For the four possible parenthesization channels of three copies of `X`, direct
fusion-ring enumeration gives

\[
\dim F^{XXX}_d=
\begin{cases}
2,&d=1,g,h,k,\\
10,&d=X,\\
8,&d=Y.
\end{cases}
\]

In particular,

\[
\boxed{F^{XXX}_X\text{ is a }10\times10\text{ block}.}
\]

So the 100 local SFT entries are not an arbitrary auxiliary space: they are a
change-of-basis presentation of the largest core associator block attached to
three copies of `X`.

This is the first strong indication that TPE localization is geometrically
aligned with the difficult part of the `R(2,2)` coherence problem.

---

## 6. Important red-team correction: do not impose naive cubic invariance

It is tempting to write the standard-prism system schematically as

\[
T=U^{\otimes3}T
\]

for the trilinear trace tensor `T` and SFT matrix `U`.

We explicitly reject this shortcut until the graphical normalization is
compiled.

The string Fourier transform is a 90-degree rotation which exchanges the two
pictorial products (ordinary multiplication and the Fourier/convolution
product).  In planar-algebra language it exchanges the identity-type element
with the Jones/unit-channel projection up to dimension normalization.  Thus it
is not an ordinary algebra automorphism preserving a single multiplication and
its cubic trace tensor.

A naive single-product cubic-invariance equation can therefore create false
solutions or false obstructions.

This red-team point is central: the TPE compiler must retain the process/history
information about *which product* is being evaluated.  This is also precisely
where an AEG-style explicit operation history may provide a useful software
representation even though the underlying categorical equation is classical.

---

## 7. Compiler target

The next implementation should compile Theorem 4.21 directly.

For every standard prism triple of I-basis elements:

1. decode it into the nine object labels `X1,...,X9` and six trivalent basis
   morphisms `alpha1,...,alpha6`;
2. evaluate the known side using the exact matrix-unit product;
3. enumerate the intermediate simple object and the three resolution bases on
   the other side;
4. map each tetrahedron to a canonical SFT/F-variable key, respecting
   orientation, dual basis, pivotal/FS signs, and tetrahedral symmetries;
5. emit an exact polynomial over
   \[
   \mathbb Q(\sqrt6)
   \]
   plus the still-undetermined pivotal/rotation roots of unity where required;
6. quotient equations only by symmetries that have been explicitly verified
   in the chosen conventions.

### Validation strategy

Before using the compiler on `R(2,2)`, reproduce one published TPE localization
example from the paper or a multiplicity-free category with known F-symbols.
Only after this test passes should a Gröbner inconsistency be interpreted as a
categorification obstruction.

---

## 8. Why this may solve something rather than merely run faster

The important comparison is not

\[
1881\text{ global variables}\quad\text{versus}\quad100\text{ local variables}.
\]

That would only be an efficiency claim.

The actual hypothesis is stronger:

> a local, overdetermined history coordinate system may reveal an algebraic
> obstruction before a global pentagon solution is accessible at all.

The TPE literature already demonstrates this phenomenon on other
categorification problems.  The `R(2,2)` question is whether the same mechanism,
combined with its unusually sparse

\[
\mathbb C\oplus\mathbb C\oplus M_2\oplus M_2
\]

local algebra, is strong enough to decide one of Meng--Yu's current unknown
rings.

If the 100-variable standard subsystem has no solution after correct
normalization, that is immediately a non-categorifiability proof.  If it has a
small finite solution set, the solutions become boundary data for the next
localized shell of TPE/pentagon equations.

Either outcome advances the open problem.
