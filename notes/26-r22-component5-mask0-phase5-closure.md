# R(2,2) Phase 5 closure — component 5 / chirality mask 0

**Status:** `CLOSED / EXACT / component 5, chirality mask 0`

This note records the first complete closure of a fresh Phase-1 survivor through the final nonlinear pentagons.  It starts only from the canonical Phase-1--4 quotient frozen on `main`; all Phase-5 statements below were independently reconstructed after the earlier superseded epsilon-minus closure note.

No Gröbner basis, global nonlinear solver, floating-point search, or generic numerical root finder is used.  The proof is an exact sequence of localizations, finite algebraic stratifications, affine eliminations, and short final-pentagon certificates.

## 1. Fresh final kernel

For scalar component `5`, chirality mask `0`, the Phase-4 quotient has

- the genuine two-parameter E torus `p*q != 0`;
- 21 active F-linear components `z0,...,z20`;
- no forced-zero F component at the generic Phase-4 stratum.

The sparse final-pentagon compiler contracts only pentagons with four noninvertible external inputs directly in

\[
\mathbf Q(i)[p^{\pm1},q^{\pm1},z_0,\ldots,z_{20}].
\]

It finds

\[
\boxed{96}
\]

final pentagon blocks, with dimension profile

\[
32\times 8,\qquad 32\times 10,\qquad 32\times 40,
\]

hence `56,448` scalar positions.  Of these, `50,880` are nonzero before canonical deduplication, and they collapse exactly to

\[
\boxed{219}
\]

unique cubic Laurent-polynomial equations in 23 variables.

The term profile begins with four binomials and two trinomials; these short equations drive the entire closure.

## 2. First local certificate: `z0 != 0`

The four shortest final-pentagon equations are

\[
\begin{aligned}
P_1&:\quad p^2z_0+i z_2z_3=0,\\
P_2&:\quad p z_2z_3-\frac{1+i}{4}z_0=0,\\
P_3&:\quad q z_1z_8+\frac{1-i}{4}z_0=0,\\
P_4&:\quad q^2z_0-i z_1z_8=0.
\end{aligned}
\]

Their provenance is

- `(X,X,X,X;X)_(0,0)`;
- `(X,X,X,X;X)_(0,2)`;
- `(X,X,X,X;Y)_(0,18)`;
- `(X,X,X,X;Y)_(18,18)`.

Assuming `z0=0`, E invertibility gives

\[
z_2z_3=0,\qquad z_1z_8=0.
\]

The resulting four zero-pattern branches are all excluded:

1. `z0=z2=z1=0`: required 10x10 F blocks become singular;
2. `z0=z3=z8=0`: likewise excluded by F invertibility;
3. `z0=z2=z8=0`: `(X,X,X,X;1)_(0,0)` specializes to a nonzero constant, normalized as `1=0`;
4. `z0=z3=z1=0`: `(X,X,X,X;Y)_(3,27)` first forces `z4=0`, after which `(X,X,X,X;g)_(0,2)` specializes to `1=0`.

Therefore

\[
\boxed{z_0\ne0}.
\]

This part is recorded in detail in `notes/25-r22-phase5-z0-certificate.md`.

## 3. Continuous parameters collapse to finite algebraic choices

Since `z0 != 0`, the four equations above may now be divided legitimately.  They give

\[
\boxed{p^3=\frac{1-i}{4}},
\qquad
\boxed{q^3=-\frac{1+i}{4}},
\qquad
\boxed{\left(\frac pq\right)^3=i},
\]

and

\[
z_2z_3=i p^2z_0,
\qquad
z_1z_8=-i q^2z_0.
\]

Hence

\[
\boxed{z_1z_2z_3z_8\ne0}.
\]

A fifth short final-pentagon entry,

\[
(X,X,X,X;1)_{(0,0)},
\]

gives after substitution

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

Thus the formerly continuous `(p,q,z0)` sector is finite.

Choose

\[
P_0=-\frac{1+i}{2},
\qquad
Q_0=\frac{1-i}{2},
\qquad
\omega=\frac{-1+i\sqrt3}{2}.
\]

Every remaining E choice is

\[
p=P_0\omega^a,
\qquad
q=Q_0\omega^b,
\qquad a,b\in\{0,1,2\},
\]

while

\[
z_0=-1\pm\frac{\sqrt6}{2}.
\]

There are therefore exactly

\[
\boxed{3\times3\times2=18}
\]

finite `(p,q,z0)` branches.

A separate mod-3 grading audit checked whether simultaneous multiplication `(p,q) -> (omega p, omega q)` could quotient these choices.  Requiring preservation of both all 219 final equations and all required F-determinant polynomials gives an inconsistent full-rank system over `F_3`.  Therefore no such symmetry was assumed; the finite branches were audited explicitly.

## 4. First ten finite branches

The base pair `(a,b)=(0,0)` was reduced by an exact affine closure.  For either root of the z0 quadratic, 18 safely localized affine equations have rank 11.  They imply

\[
\begin{aligned}
z_6=z_7=z_9=z_{10}&=0,\\
z_{13}&=iz_0-z_{20},\\
z_{14}&=-z_{20},\\
z_{15}=z_{17}&=-qz_0,\\
z_{16}=z_{18}&=(-1+i)z_{20}+iqz_0,\\
z_{19}&=z_{20}-iz_0.
\end{aligned}
\]

Together with the two nonzero product identities, the kernel projects to seven Laurent variables.  On both z0 roots the entry

\[
( X,X,X,X,X;X )_{(5,2)}
\]

specializes to a nonzero constant equation.  Thus `(0,0)` is closed for both roots.

The same diagnostic strategy closes the other four branches with `b=0`, and also the four branches with `a=0`, `b=1,2`.  In the nontrivial ratio classes the same target has exact remainder proportional to

\[
\frac{-5+2\sqrt6}{4z_1}
\quad\text{or}\quad
-\frac{5+2\sqrt6}{4z_1},
\]

which is nonzero because `z1 != 0` and `5\pm2\sqrt6 != 0`.

Hence

\[
\boxed{10/18}
\]

finite `(p,q,z0)` branches are excluded before the rank-drop analysis.

## 5. The eight rank-drop branches

The eight remaining choices are

\[
(a,b)\in\{(1,1),(2,1),(1,2),(2,2)\},
\]

with either z0 root.

Here the safely localized affine system drops from rank 11 to rank 10.  Its free variables are initially

\[
z_1,z_2,z_3,z_4,z_5,z_8,z_{11},z_{12},z_{19},z_{20}.
\]

Using the already-proved nonzero product identities to eliminate `z3,z8`, the exact residual kernel has only

\[
\boxed{z_1,z_2,z_4,z_5,z_{11},z_{12},z_{19},z_{20}},
\qquad z_1z_2\ne0.
\]

Because generic SymPy algebraic-number expansion became the computational bottleneck at this point, the residual compiler was rewritten over the exact coefficient field

\[
K=\mathbf Q(i,\sqrt2,\sqrt3)
\]

using an eight-dimensional rational basis and sparse Laurent arithmetic.  The field implementation was independently checked on all eight branches against

\[
p^3=\frac{1-i}{4},
\qquad
q^3=-\frac{1+i}{4},
\qquad
2z_0^2+4z_0-1=0,
\]

before use in the certificate search.

### 5.1 Four branches closed by three local entries

Consider the three entries

\[
(XXXX;g)_{(0,0)},\qquad
(XXXX;g)_{(0,2)},\qquad
(XXXX;g)_{(0,3)}.
\]

After the affine closure they involve only

\[
x=z_{19},\qquad y=z_{20}.
\]

Writing their exact forms as

\[
\begin{aligned}
F_0&=g x^2+hxy+ky^2,\\
F_2&=a xy+b y^2+c,\\
F_3&=d x^2+e xy+f,
\end{aligned}
\]

set `Y=y^2`.  The last two equations give

\[
xy=UY+V,
\qquad
x^2=PY+Q.
\]

The first gives one affine equation `AY+B=0`.  Substituting its solution into the algebraic identity

\[
(xy)^2=x^2y^2
\]

yields a nonzero exact remainder for `(a,b)=(1,1)` and `(2,2)`, for both z0 roots.  These four branches are therefore excluded.

Thus

\[
\boxed{14/18}
\]

finite branches are closed.

### 5.2 The last four cube/root branches become two-sign branches

For `(a,b)=(2,1)` and `(1,2)`, for either z0 root, the same three-entry system is consistent but determines

\[
\boxed{z_{19}=-z_{20}},
\qquad
\boxed{z_{20}^2=-\frac18}.
\]

Hence

\[
z_{20}=\pm\frac{i\sqrt2}{4},
\qquad
z_{19}=\mp\frac{i\sqrt2}{4}.
\]

The four remaining cube/root branches therefore split into eight exact sign subbranches, with no continuous freedom in `z19,z20`.

### 5.3 Fourth entry closes all eight sign subbranches

Now evaluate the adjacent local entry

\[
\boxed{(XXXX;g)_{(0,1)}}.
\]

For each of

\[
(a,b)=(2,1),(1,2),
\]

for each root

\[
z_0=-1\pm\frac{\sqrt6}{2},
\]

and for each sign

\[
z_{20}=\pm\frac{i\sqrt2}{4},
\]

the exact projected entry is the same nonzero constant equation, normalized as

\[
\boxed{1=0}.
\]

All eight final sign subbranches are therefore excluded.

## 6. Closure statement

All 18 finite `(p,q,z0)` branches have now been excluded exactly.  Therefore the canonical Phase-4 branch

\[
\boxed{\text{scalar component }5\;/\;\text{chirality mask }0}
\]

has **no invertible associator extension satisfying the final four-noninvertible pentagons**.

Equivalently,

\[
\boxed{\text{component 5 / mask 0 is obstructed at Phase 5}.}
\]

This is the first complete fresh Phase-5 closure among the four Phase-1 survivor scalar components.

## 7. What the proof actually used

The closure did not require solving the 219 cubic equations globally.  Its effective structure is

\[
\begin{array}{c}
23\text{-parameter Laurent kernel}\\
\Downarrow\\
z_0\ne0\\
\Downarrow\\
p^3,\ q^3,\ 2z_0^2+4z_0-1\\
\Downarrow\\
18\text{ finite }(p,q,z_0)\text{ branches}\\
\Downarrow\\
10\text{ branches killed by short diagnostic cells}\\
\Downarrow\\
8\text{ rank-drop branches}\\
\Downarrow\\
4\text{ killed by three }(XXXX;g)\text{ entries}\\
\Downarrow\\
z_{19}=-z_{20},\quad z_{20}^2=-1/8\\
\Downarrow\\
(XXXX;g)_{(0,1)}\Rightarrow1=0.
\end{array}
\]

The main mathematical lesson is that the apparent high-dimensional nonlinear coherence problem has a sharply stratified exact search geometry.  The useful operation was not a global Gröbner solve but repeated passage to the correct local relation space, followed by exact finite branching.

## 8. Next frontier

Do not infer the same certificate for another chirality branch without replay.  The next gate is

\[
\boxed{\text{component 5 / chirality mask }105}.
\]

The first question is whether its 219-polynomial final kernel is related to mask 0 by an exact relabeling/conjugation, or whether it produces a genuinely different Phase-5 obstruction type.  Establish that before attempting to propagate the closure to masks `150,255` or to components `7,13,15`.
