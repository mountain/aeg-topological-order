# R(2,2) Phase 5 — local certificate forcing `z0 != 0`

**Status:** `CANDIDATE-NEW / EXACT LOCAL CERTIFICATE / component 5, chirality 0`

This note records the first strict local reduction inside the final nonlinear pentagons for the fresh branch `component 5 / chirality 0`.  It uses only exact Phase-4 quotient data, a handful of final pentagon entries, the already-proved E torus `p*q != 0`, and required F-block invertibility.  No Groebner basis or global nonlinear solve is used.

## Four shortest final-pentagon equations

The sparse Phase-5 kernel contains the following exact equations:

\[
\begin{aligned}
P_1&:\quad p^2z_0+i z_2z_3=0,\\
P_2&:\quad p z_2z_3-\frac{1+i}{4}z_0=0,\\
P_3&:\quad q z_1z_8+\frac{1-i}{4}z_0=0,\\
P_4&:\quad q^2z_0-i z_1z_8=0.
\end{aligned}
\]

Their provenance is respectively

- `(X,X,X,X;X)_(0,0)`;
- `(X,X,X,X;X)_(0,2)`;
- `(X,X,X,X;Y)_(0,18)`;
- `(X,X,X,X;Y)_(18,18)`.

## Excluding `z0 = 0`

Assume `z0=0`. Since `p,q` are nonzero on the E-invertible torus, the four equations imply

\[
z_2z_3=0,\qquad z_1z_8=0.
\]

Hence four zero-pattern branches remain.

### Branch A: `z0=z2=z1=0`

Exact restriction of the required F determinants makes all eight 10x10 blocks singular, including `F^{XXX}_X`.  This branch is excluded by F invertibility.

### Branch D: `z0=z3=z8=0`

Likewise all eight required 10x10 blocks become singular.  This branch is excluded by F invertibility.

### Branch ZB: `z0=z2=z8=0`

The final pentagon entry

\[
(X,X,X,X;1)_{(0,0)}
\]

specializes exactly to a nonzero constant equation, normalized as

\[
1=0.
\]

Hence ZB is impossible.

### Branch ZC: `z0=z3=z1=0`

The final pentagon entry

\[
(X,X,X,X;Y)_{(3,27)}
\]

specializes to the singleton equation

\[
z_4=0.
\]

So ZC reduces to

\[
ZC4:\quad z_0=z_1=z_3=z_4=0.
\]

On ZC4 the final pentagon entry

\[
(X,X,X,X;g)_{(0,2)}
\]

again specializes to a nonzero constant equation, normalized as

\[
1=0.
\]

Thus ZC4, and hence ZC, is impossible.

All four branches under `z0=0` are excluded. Therefore

\[
\boxed{z_0\ne0.}
\]

## Immediate algebraic consequences

Because `z0 != 0`, the four shortest equations may now be divided legitimately.  They give

\[
\boxed{p^3=\frac{1-i}{4}},
\qquad
\boxed{q^3=-\frac{1+i}{4}},
\qquad
\boxed{\left(\frac pq\right)^3=i}.
\]

They also imply

\[
z_2z_3=i p^2z_0,\qquad z_1z_8=-i q^2z_0,
\]

so

\[
\boxed{z_1z_2z_3z_8\ne0}.
\]

A fifth short entry,

\[
(X,X,X,X;1)_{(0,0)},
\]

is

\[
pz_2z_3-iqz_1z_8+\frac{1+i}{4}z_0^2-\frac{1+i}{8}=0.
\]

Substituting the two product relations yields

\[
\boxed{2z_0^2+4z_0-1=0}.
\]

Thus the formerly continuous `p,q,z0` part of the 23-parameter kernel has already collapsed to finite algebraic choices before any general nonlinear solver is invoked.

## Next frontier

The preferred next step is a relation-space lift of the 219 exact cubic kernel equations: treat each occurring monomial as a temporary linear coordinate, localize only by the now-proved nonzero variables

\[
p,q,z_0,z_1,z_2,z_3,z_8,
\]

and search for low-support rank contradictions among 2–4 pentagon entries.  This is a linear necessary-condition test in monomial space, not a Groebner computation.
