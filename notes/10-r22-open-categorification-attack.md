# R(2,2) Open Categorification Attack

## Status

`OPEN PROBLEM — structural reduction established; monoidal swap lift unresolved`

This note deliberately reopens exact-category work under a different success criterion from the earlier Fibonacci benchmarks.

The previous stop condition remains valid: increasing the size of a *known* exact categorical computation did not produce an AEG-specific invariant, compression, or execution advantage. The present target is different:

> **turn a categorification problem explicitly marked unknown in the 2026 literature into a theorem, either by construction or obstruction.**

The first target is the self-dual rank-6 fusion ring `R(2,2)` from Yue Meng and Zhiqiang Yu, *Classification of some Z/2Z x Z/2Z-quadratic fusion categories of rank 6*, arXiv:2608.06064 (2026).

Meng--Yu leave exactly three small cases unresolved:

\[
R(2,2),\qquad R(4,4),\qquad R'(4).
\]

They state that these rings pass the d-number test, cyclotomic-field test, and pseudo-unitary inequality, and explicitly say that they do not know whether the rings are categorifiable. They also suspect a relation to near-group categories if categorifications exist.

---

## 1. Why start with R(2,2)

**CLASSICAL.** The self-dual family has simple objects

\[
\{1,g,h,k=gh,X,Y\},
\]

with invertible group `V4`, stabilizer `<h>` of each noninvertible, and

\[
X^2=Y^2=1+h+mX+nY,
\]

\[
XY=g+k+nX+mY.
\]

For `R(2,2)`,

\[
X^2=Y^2=1+h+2X+2Y,
\qquad
XY=g+k+2X+2Y.
\]

**COMPUTATIONAL-CLAIM.** `experiments/r22_open_attack.py` verifies the based-ring associativity and gives the following raw associator difficulty profile.

| unresolved ring | nonzero F-blocks | raw F entries | largest F block | strict-unit-reduced fusion-space gauge dimension | naive pentagon scalar equalities | largest pentagon block |
|---|---:|---:|---:|---:|---:|---:|
| `R(2,2)` | 400 | 2,080 | 10 | 61 | 84,096 | 40 |
| `R(4,4)` | 400 | 19,744 | 34 | 157 | 2,738,304 | 272 |
| `R'(4)` | 400 | 19,744 | 34 | 157 | 2,738,304 | 272 |

This is not a proof that `R(2,2)` is easy. It is a tactical reason to attack it first: it is already outside the multiplicity-free regime but is much smaller than the other two unresolved cases.

The F-block histogram for `R(2,2)` is

\[
256\times 1,
\quad128\times 2,
\quad8\times 8,
\quad8\times 10,
\]

and the pentagon-block histogram is

\[
1536\times1,
\quad1280\times2,
\quad160\times8,
\quad160\times10,
\quad32\times40.
\]

The open-problem program should therefore avoid a naive scalar pentagon solve unless all structural reductions fail.

---

## 2. FP dimensions and the near-group numerical match

**CLASSICAL.** If `d=FPdim(X)=FPdim(Y)`, then

\[
d^2=2+4d,
\]

so

\[
\boxed{d=2+\sqrt6.}
\]

Hence

\[
\boxed{\operatorname{FPdim}(R(2,2))=4+2d^2=24+8\sqrt6.}
\]

A `C2` equivariantization would double the global dimension to

\[
48+16\sqrt6.
\]

A near-group ring of order eight and level eight has a unique noninvertible object `rho` satisfying

\[
\rho^2=\sum_{u\in\widehat G}u+8\rho,
\]

and therefore

\[
\operatorname{FPdim}(\rho)^2=8+8\operatorname{FPdim}(\rho),
\]

so

\[
\operatorname{FPdim}(\rho)=4+2\sqrt6=2d.
\]

The dimension match is exact, but dimension matching alone is not the main result below.

---

## 3. The swap symmetry and an exact orbit-square identity

Define the based-ring automorphism

\[
\alpha(X)=Y,
\qquad
\alpha(Y)=X,
\qquad
\alpha(1)=1,
\quad\alpha(g)=g,
\quad\alpha(h)=h,
\quad\alpha(k)=k.
\]

**COMPUTATIONAL-CLAIM.** The experiment verifies that this is a fusion-ring automorphism of `R(2,2)`.

Now form the formal orbit object

\[
\rho_0:=X+Y.
\]

A direct calculation gives

\[
\begin{aligned}
\rho_0^2
&=X^2+XY+YX+Y^2\\
&=2(1+g+h+k)+8(X+Y).
\end{aligned}
\]

Thus

\[
\boxed{
(X+Y)^2=2\sum_{v\in V_4}v+8(X+Y).
}
\tag{3.1}
\]

This is the central ring-level bridge to the near-group problem.

---

## 4. Conditional Near-Group Lift Proposition

### Statement

**CANDIDATE-NEW / CONDITIONAL.** Let `A` be a fusion category categorifying `R(2,2)`. Suppose the ring automorphism `alpha` above lifts to a monoidal action of `C2` on `A` which fixes the four invertible isomorphism classes and exchanges `X,Y`.

Then the equivariantization

\[
\mathcal E:=\mathcal A^{C_2}
\]

has near-group Grothendieck ring

\[
\boxed{R(\widehat G,8)}
\]

where `Ghat` is an order-eight central extension

\[
1\longrightarrow C_2
\longrightarrow\widehat G
\longrightarrow V_4
\longrightarrow1.
\]

Consequently

\[
\widehat G\in\{C_2^3,\ C_4\times C_2,\ D_8,\ Q_8\}.
\]

### Ring-level derivation

1. Each of the four invertible simple objects is fixed by the action. For a `C2` stabilizer over characteristic zero, it has two equivariant lifts. Hence `E` has eight invertible simples.
2. The orbit `{X,Y}` has trivial stabilizer and gives one simple object `rho` whose forgetful object is `X+Y`.
3. Every invertible `u` fixes `rho` under tensor product. Since `rho` is self-dual, cyclic symmetry/Frobenius reciprocity gives

   \[
   N_{\rho,\rho}^{u}=N_{u,\rho}^{\rho}=1.
   \]

   Thus all eight invertibles occur once in `rho^2`.
4. Forgetting equivariance sends the sum of the eight invertibles to

   \[
   2(1+g+h+k),
   \]

   and sends `rho` to `X+Y`. Comparing with (3.1) forces the remaining coefficient to be `8`.

Therefore

\[
\boxed{
\rho^2=\sum_{u\in\widehat G}u+8\rho.
}
\]

The proposition is elementary once the monoidal action exists. The existence of that action is precisely the unresolved gate.

---

## 5. Central-extension search space

**COMPUTATIONAL-CLAIM.** The experiment enumerates all normalized `C2`-valued 2-cocycles on `V4` before quotienting by coboundaries and classifies the corresponding order-eight central extensions. The 16 cocycle representatives distribute as

| extension group | normalized cocycle representatives |
|---|---:|
| `C2^3` | 2 |
| `C4 x C2` | 6 |
| `D8` | 6 |
| `Q8` | 2 |

These are representatives rather than cohomology-class counts; the point is only that the monoidal lift has a finite four-type extension target.

**CLASSICAL.** Schopieray, arXiv:2208.07319, proves that for elementary abelian 2-groups the near-group ring `R(G,l)` is categorifiable only in the listed low-level cases; in particular

\[
\boxed{R(C_2^3,8)\text{ is not categorifiable}.}
\]

**CLASSICAL.** On the positive side, the `C4 x C2 + 8` near-group category exists and is exactly the category used by Meng--Yu to construct the previously unresolved `R'(2)` through de-equivariantization. Their Lemma 5.3 identifies the near-group category as a `C2` equivariantization of a rank-six `V4`-quadratic category, which they then show has fusion ring `R'(2)`.

Thus the group-extension type is mathematically decisive, not bookkeeping:

\[
\begin{array}{c|c}
\widehat G & \text{known status at level 8}\\
\hline
C_2^3 & \text{categorification impossible}\\
C_4\times C_2 & \text{categorification exists}\\
D_8,Q_8 & \text{not treated as settled here}
\end{array}
\]

We deliberately do not import unitary-only nonabelian near-group classifications as obstructions to the pseudo-unitary problem without a separate unitarizability argument.

---

## 6. What AEG should do here

The important object is no longer an arbitrary path history inside an already-known category. It is the **coherence of a history symmetry**.

At the fusion-ring level, `alpha` is exact. At the category level, a monoidal lift requires coherent tensorators

\[
J_{a,b}:\alpha(a)\otimes\alpha(b)
\longrightarrow
\alpha(a\otimes b)
\]

on every fusion space, compatible with the associator.

Equivalently, if `F` denotes unknown associator data, the permuted data `alpha(F)` must lie in the appropriate restricted gauge orbit of `F`.

This suggests replacing

\[
\text{solve all pentagon entries for }F
\]

by the coupled problem

\[
\boxed{
\text{find a coherent fixed point of }\alpha
\text{ in the associator/history moduli problem}.
}
\]

The AEG interpretation is that the ring symmetry identifies large families of operation histories before the associator is solved. The next experiment should construct the quotient history complex and its vector-valued multiplicity fibers, retaining only transport variables inequivalent under the `V4` action, the swap `alpha`, strict-unit normalization, and vertex gauge.

This is a genuine test of the new success criterion: if this reduction determines an extension class, produces a monoidal action, or yields an obstruction without first solving all F-symbols, it has solved information that the traditional current classification leaves unknown.

---

## 7. Immediate attack graph

```text
A0  R(2,2) fusion ring and multiplicity fibers                 DONE
 |
 v
A1  ring swap alpha: X <-> Y                                  DONE
 |
 v
A2  conditional equivariantization => R(Ghat,8)               DONE at ring level
 |
 +--> A2a classify central extension type Ghat                finite: 4 types
 |
 v
A3  build alpha-equivariant history/fusion-space quotient     NEXT
 |
 v
A4  derive monoidal-functor coherence equations for J
 |
 +--> obstruction => no swap lift
 |
 +--> solution => identify Ghat
                 |
                 +--> C2^3 => contradiction by Schopieray
                 |
                 +--> C4xC2 => compare/construct from known +8 category
                 |
                 +--> D8/Q8 => separate near-group analysis
 |
 v
A5  if swap route is inconclusive, use the quotient machinery
    as a structured front-end to the residual pentagon solve
```

---

## 8. Red-team caveats

1. **A fusion-ring automorphism need not lift to a tensor autoequivalence.** This is the central gap, not a technicality.
2. The conditional near-group proposition does not prove categorifiability or non-categorifiability of `R(2,2)` by itself.
3. The order-eight extension group is not determined by the fusion ring alone; it depends on monoidal coherence data of the action.
4. `C4 x C2 + 8` existence does not imply that its de-equivariantization can realize `R(2,2)`. Meng--Yu's analyzed de-equivariantization realizes `R'(2)`.
5. Any use of Frobenius--Schur indicators to determine the extension class must be derived explicitly; no such identification is assumed in this note.
6. The project should prefer an obstruction or construction that can be stated independently of AEG terminology. AEG earns credit only if its representation is what makes that theorem discoverable/tractable.

---

## 9. Current verdict

The first open-problem attack has found a nontrivial reduction:

\[
\boxed{
R(2,2)\text{ categorification}
\quad\xrightarrow{\text{seek coherent swap lift}}\quad
R(\widehat G,8)\text{ near-group problem}.
}
\]

This is not yet a solution, but it replaces an unstructured large associator system by a sharply testable symmetry-lifting problem with a finite extension-class output.

The next milestone is not “more pentagon equations.” It is a machine-checkable construction of the `alpha`-equivariant history quotient and the monoidal tensorator coherence system.
