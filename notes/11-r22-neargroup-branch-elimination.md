# R(2,2): Conditional Near-Group Branch Elimination

## Status

`CONDITIONAL NO-LIFT THEOREM — all four order-eight extension types eliminated`

This note sharpens the `R(2,2)` open-problem attack from `notes/10-r22-open-categorification-attack.md`.

The standing conditional hypothesis is:

> A fusion category `A` categorifies `R(2,2)`, and the based-ring involution
> `alpha: X <-> Y` lifts to a monoidal `C2`-action fixing the four invertible
> isomorphism classes.

Under that hypothesis, the previous note proves at Grothendieck-ring level that

\[
\mathcal E:=\mathcal A^{C_2}
\]

is a near-group category of type

\[
\boxed{\widehat G+8}
\]

for an order-eight central extension

\[
1\to C_2\to\widehat G\to V_4\to1,
\]

hence

\[
\widehat G\in\{C_2^3,\ C_4\times C_2,\ D_8,\ Q_8\}.
\]

All four possibilities can now be eliminated without a unitarity assumption.

---

## 1. The `C2^3` branch is impossible

**CLASSICAL.** Andrew Schopieray, *Categorification of integral group rings extended by one dimension*, arXiv:2208.07319, Theorem 1.1, classifies categorifiable near-group rings `R(G,l)` when `G` is an elementary abelian 2-group.

For

\[
G=C_2^3,
\qquad l=8,
\]

the ring is not on the allowed list. Therefore

\[
\boxed{R(C_2^3,8)\text{ is not categorifiable}.}
\]

This exclusion is unconditional and does **not** use unitarity.

---

## 2. The `C4 x C2` branch is impossible for this equivariantization

**CLASSICAL.** Near-group categories of type

\[
C_2\times C_4+8
\]

do exist. Meng--Yu use such a category to construct the ring `R'(2)` by de-equivariantization. Therefore existence of the near-group category cannot itself exclude this branch.

The required question is whether a `C2 x C4 + 8` near-group category could possess a *different* Tannakian `Rep(C2)` whose de-equivariantization has ring `R(2,2)`.

### Unique boson

**CLASSICAL.** Rowell--Solomon--Zhang, *On near-group centers and super-modular categories*, arXiv:2305.09108, describe the Drinfeld centers of the four inequivalent `C2 x C4 + 8` near-group categories.

For every one of their four cases, the center invertibles are indexed by

\[
g\in C_2\times C_4
\]

and satisfy

\[
\theta_{a_g}=\langle g,g\rangle.
\]

Their bicharacter has the form

\[
\langle(x_1,y_1),(x_2,y_2)\rangle
=
\exp\!\left(2\pi i\frac{x_1x_2}{2}\right)
\exp\!\left(2\pi i m\frac{y_1y_2}{4}\right),
\qquad m=\pm1.
\]

For the three nontrivial order-two elements,

\[
\begin{aligned}
\theta_{a_{(1,0)}}&=-1,\\
\theta_{a_{(0,2)}}&=+1,\\
\theta_{a_{(1,2)}}&=-1.
\end{aligned}
\]

Thus

\[
\boxed{a_{(0,2)}\text{ is the unique nontrivial invertible boson in }Z(\mathcal E).}
\]

Hence the center has a unique Tannakian subcategory equivalent to `Rep(C2)`.

`experiments/r22_neargroup_branch_elimination.py` checks the finite bicharacter arithmetic.

### Unique de-equivariantization

**CLASSICAL.** Meng--Yu, arXiv:2608.06064, Corollary 5.8, prove that if `E` is a near-group category of type `C2 x C4 + 8`, then the rank-six category obtained by `C2` de-equivariantization has Grothendieck ring

\[
R'(2).
\]

Because the relevant `Rep(C2)` is unique, there is no second order-two Tannakian condensation capable of producing `R(2,2)`.

Therefore

\[
\boxed{C_4\times C_2\text{ cannot be }G(\mathcal A^{C_2})\text{ for an }R(2,2)\text{ swap lift}.}
\]

---

## 3. The nonabelian `D8` and `Q8` branches are also impossible

This step does **not** require the unitary classification of nonabelian near-group categories.

**CLASSICAL.** Victor Ostrik, with Appendix A jointly written with Dmitri Nikshych, *Pivotal fusion categories of rank 3*, arXiv:1309.4822, Theorem A.6, proves:

> If the near-group ring `K(G,n)` is categorifiable and the positive Frobenius--Perron dimension `d_+` of the unique noninvertible object is irrational, then `n` is divisible by `|G|` and `G` is abelian.

For every order-eight, level-eight near-group ring,

\[
d_+^2=8+8d_+,
\]

so

\[
\boxed{d_+=4+2\sqrt6,}
\]

which is irrational.

Consequently a categorifiable `G+8` near-group ring with `|G|=8` must have `G` abelian. Therefore

\[
\boxed{D_8+8\text{ and }Q_8+8\text{ are not categorifiable}.}
\]

This argument is unconditional; no `C*`, unitary, or unitarizability assumption is used.

For completeness, the same Appendix also proves that in the integral case one has `n<|G|` (Lemma A.9), explaining the general nonabelian level bound quoted by Schopieray.

---

## 4. Conditional No-Lift Theorem

### Theorem

**CANDIDATE-NEW / CONDITIONAL.** Let `A` be a fusion category categorifying `R(2,2)`. Then the based-ring involution

\[
\alpha(X)=Y,
\qquad
\alpha(Y)=X,
\qquad
\alpha|_{V_4}=\mathrm{id}
\]

cannot be realized by a monoidal `C2`-action on `A` fixing the four invertible isomorphism classes.

### Proof

Assume such an action exists. By the conditional near-group lift proposition of `notes/10-r22-open-categorification-attack.md`, the equivariantization

\[
\mathcal E=\mathcal A^{C_2}
\]

has near-group Grothendieck ring `R(Ghat,8)` where

\[
1\to C_2\to\widehat G\to V_4\to1.
\]

There are four isomorphism types for `Ghat`.

1. `C2^3` is impossible by Schopieray Theorem 1.1.
2. `C4 x C2` is impossible because its center has a unique `Rep(C2)`, whose de-equivariantization has ring `R'(2)` by Meng--Yu Corollary 5.8.
3. `D8` is impossible by Ostrik--Nikshych Theorem A.6 since `d_+=4+2sqrt(6)` is irrational but `D8` is nonabelian.
4. `Q8` is impossible for the same reason.

All possible extension groups are excluded, contradiction.

\[
\boxed{\text{Therefore no such monoidal swap action exists.}}\qquad\square
\]

---

## 5. Why this is strategically important

This is the first result in the repository whose target is not reconstruction of known category data or comparison of representations. It constrains a hypothetical categorification which the 2026 literature still leaves open.

The result does **not** yet decide whether `R(2,2)` is categorifiable. Instead it says something unexpectedly rigid:

\[
\boxed{
\text{if }R(2,2)\text{ is categorifiable, its categorification must break an exact symmetry of its fusion ring at the monoidal level.}
}
\]

Thus the original fusion grammar has an obvious `X<->Y` symmetry, but no associator class realizing `R(2,2)` may be fixed by that symmetry in the tensor-equivalence moduli problem.

This is precisely the kind of distinction an explicit operation-history treatment can expose:

\[
\text{grammar symmetry}\not\Rightarrow\text{coherent history symmetry}.
\]

The obstruction lives at the coherence layer.

---

## 6. Fixed-locus reduction for the next attack

`experiments/r22_swap_lift_skeleton.py` gives a favorable finite structure for studying this obstruction:

- `R(2,2)` has 48 nonzero fusion vertices, with multiplicity histogram `40 x 1` and `8 x 2`;
- after strict-unit normalization there are 37 fusion vertices;
- all eight multiplicity-two vertices lie in free `C2` orbits under `X<->Y`;
- every non-pointed fusion vertex lies in a free orbit;
- the only fixed strict-unit vertices are nine one-dimensional vertices entirely inside the pointed `V4` sector.

Therefore arbitrary tensorator matrices on high-multiplicity spaces are not the irreducible obstruction. Paired bases can normalize tensorators on free orbits; the surviving fixed-locus data are pointed one-dimensional cocycle variables coupled to global associator coherence.

This suggests the next mathematical target:

\[
\boxed{
\text{classify the obstruction to lifting }\alpha
\text{ from the pointed fixed locus through the mixed history cells}.}
\]

---

## 7. What would solve the open categorification problem

The conditional no-lift theorem converts the categorification question into a much sharper fork.

### Route A — prove the lift is forced

If one can prove from the `R(2,2)` fusion rules and fusion-category axioms that every categorification necessarily admits the swap tensor autoequivalence, then the theorem above yields an immediate contradiction:

\[
\boxed{R(2,2)\text{ is not categorifiable}.}
\]

### Route B — classify symmetry-breaking associators

If the lift need not exist automatically, then any categorification must lie in an `alpha`-nonfixed orbit of associator classes. One can therefore search only for symmetry-breaking solutions and try to derive an invariant/obstruction describing the failure of the swap to lift.

Either route is substantially narrower than solving all `84,096` raw scalar pentagon equalities.

---

## 8. Current branch table

| `G(A^{C2})` under a hypothetical swap lift | status |
|---|---|
| `C2^3` | **eliminated** — Schopieray Theorem 1.1 |
| `C4 x C2` | **eliminated** — unique Tannakian de-equivariantization is `R'(2)` |
| `D8` | **eliminated** — Ostrik--Nikshych Theorem A.6 |
| `Q8` | **eliminated** — Ostrik--Nikshych Theorem A.6 |

The near-group branch analysis is complete. The active problem is now the **monoidal symmetry-lift obstruction itself**.
