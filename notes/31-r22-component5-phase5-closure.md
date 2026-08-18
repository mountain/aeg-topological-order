# R(2,2) Phase 5 — complete closure of scalar component 5

**Status:** `CLOSED / EXACT / ALL FOUR CHIRALITY SURVIVORS`

This note freezes the current theorem boundary for scalar component `5` in the epsilon-minus `R(2,2)` categorification attack.

The four Phase-1 chirality survivors are

\[
\boxed{0,105,150,255}.
\]

All four have now been replayed through the complete Phase-5 quotient and excluded exactly.  Therefore

\[
\boxed{\text{scalar component 5 has no invertible associator extension}.}
\]

Equivalently,

\[
\boxed{\text{scalar component 5 is completely obstructed at Phase 5}.}
\]

This statement does **not** yet imply global non-categorifiability of `R(2,2)`: scalar components `7`, `13`, and `15` remain open at Phase 5.

Detailed branch notes are:

- `notes/26-r22-component5-mask0-phase5-closure.md`;
- `notes/27-r22-component5-mask105-phase5-closure.md`;
- `notes/29-r22-component5-mask150-phase5-closure.md`;
- `notes/30-r22-component5-mask255-phase5-closure.md`.

---

## 1. Common Phase-5 kernel geometry

For every component-5 chirality survivor the Phase-4 quotient contains

\[
p,q,z_0,\ldots,z_{20},
\]

so there are 23 effective nonlinear parameters.

Fresh sparse exact compilation gives, for each mask,

- 96 final pentagon blocks with four noninvertible external inputs;
- 56,448 scalar positions;
- 50,880 nonzero scalar entries;
- 219 unique exact cubic Laurent-polynomial equations.

Thus all four chiralities share the reduction

\[
50,880\text{ raw nonzero entries}
\longrightarrow
219\text{ exact cubic relations}.
\]

No closure requires a global Gröbner basis or numerical nonlinear solve.

---

## 2. The four local phase patterns

After `z0 != 0` is proved on each branch, the four shortest local equations give the following exact relations.

| mask | \(p^3\) | \(q^3\) | \(z_2z_3/(p^2z_0)\) | \(z_1z_8/(q^2z_0)\) |
|---:|---|---|---:|---:|
| 0 | \((1-i)/4\) | \(-(1+i)/4\) | \(+i\) | \(-i\) |
| 105 | \((1+i)/4\) | \(-(1+i)/4\) | \(-i\) | \(-i\) |
| 150 | \((1-i)/4\) | \((-1+i)/4\) | \(+i\) | \(+i\) |
| 255 | \((1+i)/4\) | \((-1+i)/4\) | \(-i\) | \(+i\) |

In every mask the fifth local entry gives

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

For masks `150` and `255`, this fifth relation was independently re-derived from the original pentagon provenance using only the preceding product/cube relations and **without assuming the z0 quadratic**.  Their final serial verification also audited F-coordinate stability across independent Python hash seeds.

The phase table reveals a clean two-bit pattern: the first chirality bit flips the `p`-side phase, while the second flips the `q`-side phase.  This pattern is structurally suggestive, but the proof does not use a global chirality symmetry: the naive identity-coordinate complex-conjugation map was audited and fails at the full Phase-5 quotient.

---

## 3. `z0=0` is impossible for every survivor

Each mask has a fresh exact localization proof that

\[
\boxed{z_0\ne0}.
\]

For the later serial replays of masks `150` and `255`, the zero-branch audit was strengthened: all 50,880 raw nonzero final-pentagon entries were specialized **before canonicalization and deduplication**.  The four product-zero patterns

```text
A, ZB, ZC, D
```

all close directly by a nonzero torus-only constant equation.  This raw-before-canonical discipline avoids deriving accidental constraints from a polynomial that was normalized by a factor that becomes zero after specialization.

---

## 4. Universal finite-stratum split

For every component-5 chirality survivor, the scale sector collapses to

\[
3\times3\times2=18
\]

finite algebraic choices of `(p,q,z0)`.

All four masks then exhibit the same exact affine-rank stratification:

\[
\boxed{18=10+8}.
\]

### Generic finite stratum

Ten branches have

\[
\operatorname{rank}=11,
\qquad
\dim_{\rm free}=9,
\]

and force

\[
\boxed{z_6=z_7=z_9=z_{10}=0}.
\]

They are excluded by short diagnostic final-pentagon cells whose remainders are nonzero Laurent monomials in already-proved nonzero scale variables.

### Rank-drop stratum

Exactly eight branches remain:

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\}
\]

for both roots of the `z0` quadratic.

They have

\[
\operatorname{rank}=10,
\qquad
\dim_{\rm free}=10,
\]

with no affine forced zero.  After safe product elimination, the decisive nonlinear relations collapse to a local two-variable core

\[
x=z_{19},\qquad y=z_{20}.
\]

This repeated `10+8` rank geometry is one of the main structural findings of the component-5 computation.

---

## 5. Local closure certificates

The rank-drop strata are closed by only a few neighboring entries of the `(XXXX;g)` final pentagon blocks.

### Mask 0

The eight difficult finite branches reduce to a small two-variable exact system.  Four branches are excluded by three local entries; the remaining four satisfy

\[
z_{19}=-z_{20},
\qquad
z_{20}^2=-\frac18,
\]

and a fourth adjacent entry gives a nonzero constant equation.  See note 26.

### Mask 105

Four off-diagonal/root branches use two-cell certificates:

\[
(x-y)^2=0,
\qquad
4xy-4y^2-1=0
\]

imply `-1=0`.

The four diagonal/root branches use three cells: `G2+G3` forces `x=\pm y`; the same-sign branch is impossible, and the opposite-sign branch gives `y^2=-1/8`, after which `G0` is nonzero.  See note 27.

### Mask 150

A strict serial replay independently reproduces the same certificate geometry as mask 105:

- four branches close by two cells;
- four branches close by three cells.

The final nonzero constants on the diagonal pairs are

\[
-\frac{\sqrt3}{4}+\frac{i}{4}
\quad\text{and}\quad
-\frac{\sqrt3}{4}-\frac{i}{4}.
\]

GitHub Actions run `32173886648` (run 99) verifies the entire chain serially.  See note 29.

### Mask 255

All eight rank-drop branches close by three-cell certificates, but the geometry differs from mask 150.

For the off-diagonal pairs,

\[
\operatorname{Res}_x(G_0,G_1)=48y^4,
\]

so a common zero forces `y=0`, then `x=0`, while `G2(0,0)=i` is nonzero.

For the diagonal pairs,

\[
iG_3-G_2=4(1+i)(x-y)(x+y),
\]

and `G0` is nonzero on both sign branches.  Again `x=y=0` contradicts `G2`.

GitHub Actions run `32175782953` (run 100) verifies all eight branches serially.  See note 30.

---

## 6. Component-5 theorem boundary

Combining the four independent branch closures gives

\[
\boxed{
\forall m\in\{0,105,150,255\},
\quad
\mathcal C_{5,m}^{\mathrm{Phase5}}=\varnothing.
}
\]

Hence there is no epsilon-minus categorification branch lying over scalar component 5.

The global `R(2,2)` problem remains open because Phase 5 has not yet been closed for scalar components

\[
\boxed{7,13,15}.
\]

---

## 7. Methodological consequence

The component-5 calculation repeatedly exhibits the same compression pattern:

\[
\begin{array}{c}
50,880\text{ raw final entries}\\
\Downarrow\\
219\text{ cubic relation types}\\
\Downarrow\\
z_0\ne0\text{ and five local scale relations}\\
\Downarrow\\
18\text{ finite strata}\\
\Downarrow\\
10+8\text{ affine-rank stratification}\\
\Downarrow\\
(z_{19},z_{20})\text{ local relation core}\\
\Downarrow\\
2\text{--}4\text{ local pentagon entries}\\
\Downarrow\\
\text{exact contradiction}.
\end{array}
\]

The practical lesson is not merely that the original system can be computed.  The effective obstruction lives in a much smaller **relation space** after the correct quotient and stratification.  This is now reproduced across all four component-5 chiralities, rather than being an accident of a single branch.

---

## 8. Next frontier

The next priority is

\[
\boxed{\text{scalar component 13 / chirality mask 0}.}
\]

Component 13 shares the Phase-4 count of 21 free weighted F components with component 5, making it the cleanest test of whether the `219 -> finite strata -> low-dimensional local certificate` mechanism persists across scalar components.

No component-5 local relation, coordinate identification, or certificate should be imported into component 13 without a fresh exact replay.
