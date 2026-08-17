# R(2,2): Conditional Near-Group Branch Elimination

## Status

`CONDITIONAL REDUCTION — two of four order-eight extension types eliminated`

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

The purpose here is to eliminate the two abelian possibilities rigorously.

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

Consequently the conditional equivariantization of an `R(2,2)` category cannot have invertible group `C2^3`.

---

## 2. Why `C4 x C2` needs a stronger argument

**CLASSICAL.** Near-group categories of type

\[
C_2\times C_4+8
\]

do exist. In fact Meng--Yu use precisely such a category to construct the previously unresolved ring `R'(2)` by de-equivariantization.

So existence of the near-group category cannot itself exclude this branch.

The required question is instead:

> Can a `C2 x C4 + 8` near-group category possess a *different* Tannakian `Rep(C2)` whose de-equivariantization has ring `R(2,2)` rather than `R'(2)`?

The answer is no, because the relevant `Rep(C2)` is unique.

---

## 3. Unique boson in the center of every `C2 x C4 + 8` category

**CLASSICAL.** Rowell--Solomon--Zhang, *On near-group centers and super-modular categories*, arXiv:2305.09108, describe the Drinfeld centers of the four inequivalent `C2 x C4 + 8` near-group categories.

For every category in their Table 3, the center contains exactly one invertible simple object `a_g` for every

\[
g\in C_2\times C_4,
\]

and its twist is

\[
\theta_{a_g}=\langle g,g\rangle.
\]

The bicharacter in all four cases has the form

\[
\langle(x_1,y_1),(x_2,y_2)\rangle
=
\exp\!\left(2\pi i\frac{x_1x_2}{2}\right)
\exp\!\left(2\pi i m\frac{y_1y_2}{4}\right),
\qquad m=\pm1.
\]

The three nontrivial order-two elements are

\[
(1,0),\qquad(0,2),\qquad(1,2).
\]

For either `m=+1` or `m=-1`,

\[
\begin{aligned}
\theta_{a_{(1,0)}}&=-1,\\
\theta_{a_{(0,2)}}&=+1,\\
\theta_{a_{(1,2)}}&=-1.
\end{aligned}
\]

`experiments/r22_neargroup_branch_elimination.py` checks this finite arithmetic.

Thus

\[
\boxed{a_{(0,2)}\text{ is the unique nontrivial invertible boson in }Z(\mathcal E).}
\]

A Tannakian subcategory equivalent to `Rep(C2)` has one nontrivial simple object, necessarily an invertible boson of order two. Since Rowell--Solomon--Zhang list all center invertibles, this gives

\[
\boxed{
Z(\mathcal E)\text{ contains a unique Tannakian }\operatorname{Rep}(C_2).
}
\]

---

## 4. Meng--Yu identify that unique de-equivariantization

**CLASSICAL.** Meng--Yu, arXiv:2608.06064, Corollary 5.8, prove:

> If `E` is a near-group fusion category of type `C2 x C4 + 8`, then `E` is a `C2`-equivariantization of a rank-six category `A`, and the Grothendieck ring of `A` is `R'(2)`.

Their preceding Lemma 5.3 constructs the required Tannakian `Rep(C2)` in the center.

Because Section 3 above shows that the center has only one nontrivial `Rep(C2)`, there is no second Tannakian order-two condensation which could yield another rank-six fusion ring.

Therefore every `C2` de-equivariantization relevant to an equivariantization presentation of `E` has

\[
\boxed{K_0(\mathcal A)=R'(2).}
\]

---

## 5. Conditional exclusion theorem

### Proposition

**CANDIDATE-NEW / CONDITIONAL.** Assume a categorification `A` of `R(2,2)` admits the monoidal swap action from `notes/10-r22-open-categorification-attack.md`. Then its equivariantization

\[
\mathcal E=\mathcal A^{C_2}
\]

cannot have invertible group

\[
C_2^3
\quad\text{or}\quad
C_4\times C_2.
\]

Hence necessarily

\[
\boxed{
G(\mathcal E)\in\{D_8,Q_8\}.
}
\]

### Proof

- `C2^3`: impossible because `R(C2^3,8)` is not categorifiable by Schopieray Theorem 1.1.
- `C4 x C2`: suppose it occurs. Then `E` is one of the four `C2 x C4 + 8` near-group categories. The center has a unique nontrivial Tannakian `Rep(C2)` by the Rowell--Solomon--Zhang center formula above. The original action presentation `E=A^{C2}` must correspond to this unique Tannakian subcategory. But Meng--Yu Corollary 5.8 says its de-equivariantization has ring `R'(2)`, contradicting `K0(A)=R(2,2)`.

\[
\square
\]

---

## 6. A small group-theoretic reinforcement

**COMPUTATIONAL-CLAIM.** In `C4 x C2`, there are three subgroups of order two, generated by

\[
(0,1),\quad(2,0),\quad(2,1).
\]

Only

\[
\langle(2,0)\rangle
\]

has quotient `V4`; the other two quotients are cyclic `C4`. This is checked in `experiments/r22_swap_lift_skeleton.py`.

This is not needed once center uniqueness is established, but it confirms that even at the group-extension level there is a distinguished kernel compatible with the rank-six `V4` quotient.

---

## 7. What remains, and what cannot yet be claimed

The conditional branch table is now

| `G(E)` | status under the monoidal-swap hypothesis |
|---|---|
| `C2^3` | **eliminated** — near-group ring not categorifiable |
| `C4 x C2` | **eliminated** — unique `Rep(C2)` de-equivariantizes to `R'(2)` |
| `D8` | open in the pseudo-unitary setting |
| `Q8` | open in the pseudo-unitary setting |

There are two important red-team restrictions.

1. **Do not use the known nonabelian *unitary* near-group classification to eliminate `D8,Q8`.** Meng--Yu only reduce an arbitrary categorification to a pseudo-unitary Galois conjugate; unitarity is an additional hypothesis.
2. **This does not yet prove that `R(2,2)` is non-categorifiable.** A categorification might exist with no tensor autoequivalence lifting `X<->Y`.

Thus the next attack has two possible ways to convert this conditional result into an unconditional theorem:

\[
\boxed{
\begin{array}{ll}
\textbf{Route A:}&\text{prove that every categorification of }R(2,2)\text{ must admit the swap lift};\\[2pt]
\textbf{Route B:}&\text{show that }D_8+8\text{ and }Q_8+8\text{ cannot occur in the}\
&\text{pseudo-unitary equivariantization forced by such a lift.}
\end{array}}
}
\]

Route A is more directly aligned with the AEG/history program: it asks whether the exact symmetry of the fusion-history grammar can be coherently extended across all associator cells.

---

## 8. Next concrete computation

The fixed-locus analysis in `experiments/r22_swap_lift_skeleton.py` has already shown something favorable:

- every non-pointed fusion vertex is in a free `C2` orbit under `X<->Y`;
- all eight multiplicity-two fusion vertices are free;
- after strict-unit normalization, the only fixed fusion vertices are nine one-dimensional vertices entirely inside the pointed `V4` sector.

Therefore the next solver should not introduce arbitrary tensorator matrices on every multiplicity space. It should:

1. normalize tensorators on free non-pointed vertex orbits by paired bases;
2. parameterize only the pointed fixed-locus cocycle data;
3. propagate those parameters through mixed associator cells;
4. detect whether global coherence forces one of the four central-extension classes, or gives an obstruction.

That is now the narrowest identified route from explicit operation histories to a genuinely unresolved categorification theorem.
