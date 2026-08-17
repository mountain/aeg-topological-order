# R(2,2): Pointed-Module Swap and the Mixed-Coherence Obstruction

## Status

`STRUCTURAL LOCALIZATION — ring and pointed-module symmetry survive; tensor symmetry is obstructed`

This note combines three facts established in the current open-problem attack:

1. the fusion ring `R(2,2)` has an involution `alpha` fixing `V4` and swapping `X,Y`;
2. the induced two-point module category over the pointed subcategory has a swap module autoequivalence;
3. `notes/11-r22-neargroup-branch-elimination.md` proves conditionally that no categorification of `R(2,2)` can realize this swap as a monoidal `C2` action on the full fusion category.

The consequence is a precise localization of the obstruction:

\[
\boxed{
\text{ring symmetry}
\longrightarrow
\text{pointed-module symmetry}
\not\longrightarrow
\text{full tensor symmetry}.
}
\]

The missing datum lives in the coherence of the noninvertible multiplication, not in the permutation of objects or the pointed action alone.

---

## 1. Pointed subcategory and two-point module

Let `A` be a hypothetical categorification of `R(2,2)`. Its pointed subcategory has simple objects

\[
G=\{1,g,h,k=gh\}\cong V_4,
\]

so

\[
\mathcal P:=\mathcal A_{pt}\simeq\operatorname{Vec}_{V_4}^{\omega}
\]

for some class `omega in H^3(V4,C^x)`.

The noninvertible simples form one transitive `V4` orbit

\[
\mathcal M=\langle X,Y\rangle,
\]

with stabilizer

\[
H=G[X]=G[Y]=\langle h\rangle\cong C_2.
\]

Thus, as a `P`-module category, `M` is the standard transitive module associated to the coset set

\[
V_4/H=\{H,gH\}.
\]

**CLASSICAL.** Indecomposable module categories over `Vec_G^omega` are described by subgroup/cochain data `(H,psi)` with `d psi=omega|_H`; equivalently they are induced projective 2-representations. This is the pointed-module classification used by Ostrik and reformulated explicitly by Ganter--Usher.

---

## 2. Why a module swap exists

There are two complementary descriptions.

### 2.1 Dual group-theoretical category

The module endofunctor category

\[
\operatorname{Fun}_{\mathcal P}(\mathcal M,\mathcal M)
\]

is the group-theoretical fusion category

\[
\mathcal C(V_4,\omega,H,\psi).
\]

**CLASSICAL.** Gelaki--Naidu describe its simples by pairs consisting of an `H`-double coset `HaH` and an irreducible projective representation of

\[
H^a=H\cap aHa^{-1}.
\]

Here `V4` is abelian, so `H` is normal, every double coset is an ordinary coset, and

\[
H^a=H\cong C_2
\]

for both cosets. The relevant projective cocycle on `C2` is cohomologically trivial because

\[
H^2(C_2,\mathbb C^\times)=0.
\]

Therefore the nontrivial coset `gH` contributes invertible module endofunctors. Their action on the two simple module objects interchanges the two cosets and hence swaps

\[
X\leftrightarrow Y.
\]

So the swap is not merely an object-level permutation: it is a genuine `P`-module autoequivalence.

### 2.2 Finite cochain audit

`experiments/r22_pointed_module_swap.py` independently checks the same phenomenon in a finite cochain model.

It enumerates normalized sign-valued `V4` 3-cocycles, all sign-valued two-point module associators compatible with them, and solves the module-functor coherence equations for the coset swap.

A useful warning appears:

- if the swap tensorator is artificially restricted to `+/-1`, false obstructions occur;
- allowing fourth roots of unity removes them.

Across all admissible sign-cochain representatives and all `256` sign-valued module-associator representatives tested, a swap module functor exists. Some representatives require tensorator phases `+/- i`.

**COMPUTATIONAL-CLAIM.** This finite audit is a gauge sanity check, not the proof of the general statement; the group-theoretical dual argument above is the conceptual proof.

---

## 3. The full category has trivial universal grading

The fusion rules themselves imply

\[
\mathcal A_{ad}=\mathcal A.
\]

Indeed,

\[
X\otimes X^*=1+h+2X+2Y
\]

already puts `h,X,Y` in the adjoint subcategory, while

\[
X\otimes Y=g+k+2X+2Y
\]

then puts `g,k` there as well.

Hence

\[
\boxed{U(\mathcal A)=1.}
\]

**CLASSICAL.** The group of tensor natural automorphisms of the identity functor is canonically

\[
\operatorname{Aut}_{\otimes}(\operatorname{Id}_{\mathcal A})
\cong
\operatorname{Hom}(U(\mathcal A),\mathbb C^\times),
\]

so in this case

\[
\boxed{\operatorname{Aut}_{\otimes}(\operatorname{Id}_{\mathcal A})=1.}
\]

This removes one possible source of higher scalar ambiguity. It does **not** imply that every object-fixing gauge autoequivalence of `A` is trivial; those are distinct notions and must not be conflated.

---

## 4. Where the obstruction must live

The pointed action and its module symmetry are therefore not the issue.

Let

\[
S:\mathcal M\to\mathcal M
\]

be a `P`-module autoequivalence with

\[
S(X)=Y,\qquad S(Y)=X.
\]

To extend `S` to a tensor autoequivalence of `A` which is the identity on `P`, one needs compatibility not only with

\[
\mathcal P\otimes\mathcal M\to\mathcal M,
\]

but also with the multiplication bifunctor

\[
\boxed{
\mathcal M\otimes\mathcal M
\longrightarrow
\mathcal P\oplus\mathcal M.
}
\]

At the Grothendieck-ring level this multiplication is perfectly symmetric because `m=n=2`:

\[
X^2=Y^2=1+h+2X+2Y,
\]

\[
XY=g+k+2X+2Y.
\]

But `notes/11-r22-neargroup-branch-elimination.md` proves that no full monoidal `C2` action realizing the swap can exist.

Therefore the obstruction is necessarily an **associator-level failure of the symmetric multiplication data to extend the pointed-module swap**.

This is much narrower than the raw categorification problem:

\[
\boxed{
\text{84,096 scalar pentagon entries}
\quad\rightsquigarrow\quad
\text{extension of one module symmetry across }M\otimes M.
}
\]

The number `84,096` is a raw matrix-entry proxy, not the dimension of a minimal polynomial system; the arrow denotes a change of problem representation, not a proven asymptotic reduction.

---

## 5. Fixed-locus structure makes the obstruction unusually local

`experiments/r22_swap_lift_skeleton.py` shows:

- 48 nonzero fusion vertices in total, with multiplicities `40 x 1` and `8 x 2`;
- 37 after strict-unit normalization;
- all eight multiplicity-two fusion vertices lie in free swap orbits;
- all non-pointed fusion vertices lie in free swap orbits;
- the only fixed strict-unit fusion vertices are nine one-dimensional vertices inside the pointed `V4` sector.

Thus the difficult high-multiplicity spaces are not fixed points of the involution. Paired basis choices can compare them orbitwise.

The obstruction should therefore be sought in **closed mixed associator histories** which start with the module swap, pass through `M x M` fusion, and return to the same pointed/module frame.

This is the current AEG target: not a new categorical invariant, but a small explicit history cycle whose failure to close detects the impossibility of extending a module symmetry to a tensor symmetry.

---

## 6. Relation to generalized near-group structure theory

**CLASSICAL.** Dong--Sun show that a generalized near-group category with nonzero noninvertible multiplicities has strong adjoint/universal-grading structure; in particular its adjoint subcategory remains non-pointed and one reduces classification to generalized near-group categories with trivial universal grading.

For `R(2,2)` the fusion rules already force the whole category to have trivial universal grading, so it is precisely in this hard core.

Their general structure results do **not** assert that a nontrivial stabilizer automatically arises from an equivariantization, nor that the ring swap must lift to a tensor autoequivalence. Therefore the no-lift phenomenon found here is not removed by an existing generalized-near-group theorem.

---

## 7. Triangular Prism Equations: useful baseline, not yet a direct solver

**CLASSICAL.** Liu--Palcoux--Ren--Vercleyen prove that in the spherical case the Triangular Prism Equations (TPE) are equivalent to pentagon equations after a change of basis, and demonstrate that localization can solve categorification problems inaccessible to a naive global pentagon treatment.

This is strategically important: an equivalent representation can solve previously unsolved categorification problems.

However, the particularly cheap localization criterion used in their Section 6.2 assumes fusion multiplicities at most one. `R(2,2)` has multiplicity two, so that criterion cannot simply be transplanted.

The project has already tested the general zero-spectrum and one-spectrum obstructions without finding a witness for `R(2,2)`, `R(4,4)`, or `R'(4)`.

A full multiplicity-aware TPE implementation remains a legitimate independent attack, but it is no longer the only structured route: the module-swap obstruction gives a much smaller problem-specific target.

---

## 8. Next exact target: the mixed swap-defect cell

The next computation should construct the smallest closed history diagram measuring the compatibility of

\[
S(X)=Y
\]

with the multiplication channels in

\[
X\otimes X,
\quad X\otimes Y,
\quad Y\otimes X,
\quad Y\otimes Y.
\]

A successful formulation should satisfy four requirements:

1. **Gauge aware:** invariant under paired basis changes on free swap orbits.
2. **Local:** involve only the mixed `P/M` associator blocks necessary to close the history cycle.
3. **Complete for extension:** vanishing should be equivalent, or provably necessary, for extending the pointed-module swap to a tensor autoequivalence.
4. **Computable before full categorification:** the defect should be constrained by pentagon/TPE identities enough to derive a contradiction or a small residual algebraic system.

If such a defect is forced nonzero for every possible associator, that supplies a conceptual explanation of the conditional no-lift theorem. If, conversely, fusion-category axioms force the defect to vanish, then the swap would lift and `R(2,2)` would be non-categorifiable immediately.

That is now the central open attack.
