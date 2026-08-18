# R(2,2) Phase 5 — final nonlinear kernel protocol

**Status:** `OPEN / DEVELOPMENT GATE`

Phase 1–4 are frozen on `main`.  Phase 5 studies only pentagons with four noninvertible external inputs after substituting the exact D witnesses, the full two-parameter E torus, and the complete F-linear weighted quotient.

The first gate is component 5 / chirality mask 0.  No nonlinear solving is allowed at this gate.  The compiler must report only:

- number of kernel variables;
- number of final pentagon blocks and scalar positions;
- number of raw nonzero equations;
- number of unique normalized Laurent polynomials;
- term-count and degree profiles;
- exact pentagon-entry provenance for every unique polynomial.

The compiler uses a sparse exact representation over

\[
\mathbf Q(i)[p^{\pm1},q^{\pm1},z_0,\ldots,z_{n-1}],
\]

rather than materializing generic SymPy F-symbol matrices.  The E-invertible locus has `p*q != 0`, so a common Laurent monomial in `p,q` may be removed when canonicalizing an equation.  No F-component variable may be divided out.

The preferred next step after a successful kernel compile is local-certificate search: prioritize subsets of 2–4 pentagon entries and seek an exact contradiction, localized only by already-proved invertibility conditions.  Gröbner-basis computation remains deferred until the small kernel and its local structure are audited.
