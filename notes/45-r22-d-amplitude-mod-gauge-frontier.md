# R(2,2) theorem audit — D-amplitude mod-gauge frontier

## Status

**CONNECTED PART CLOSED / DISCRETE PART UNDER AUDIT.**

The fresh theorem-closure audit found a previously unrecorded structural feature in the epsilon-minus D-amplitude layer.

For every deep scalar component

\[
\boxed{5,7,13,15}
\]

and every surviving chirality mask

\[
\boxed{0,105,150,255},
\]

the 48 nonzero cross-D amplitudes satisfy the same 168 binomial character equations.  Their homogeneous exponent matrix is literally identical across all sixteen branches.

## 1. Exact lattice profile

`experiments/r22_epsminus_d_amplitude_gauge_audit.py` computes, for the common

\[
A_D\in M_{168\times48}(\mathbb Z),
\]

\[
\operatorname{rank}_{\mathbb Q}A_D=42,
\qquad
\operatorname{rank}_{\mathbb F_2}A_D=40.
\]

Its nonzero Smith factors are

\[
\boxed{1^{40},2,2}.
\]

Therefore the homogeneous nonzero amplitude solution group is

\[
\boxed{H_D\cong(\mathbf C^*)^6\times\mu_2\times\mu_2}.
\]

This is not a numerical observation: it is the exact character-lattice decomposition of the complete 168-equation binomial system.

Fresh Actions run:

```text
32262002092
```

reconstructs all sixteen branches and confirms that there is exactly one exponent-matrix variant.

## 2. Connected residual gauge

Scalar basis changes on the eight multiplicity-two fusion spaces

\[
V_{MN}^P,\qquad M,N,P\in\{X,Y\},
\]

leave the normalized Pauli seed matrices unchanged by scalar conjugation.  On the 48 cross-D blocks they act by source/target endpoint ratios.

The endpoint graph is exactly two connected K4 components, so its incidence gauge map has rank

\[
8-2=6.
\]

The verifier reconstructs the source and target fusion spaces directly from fusion multiplicities and checks

\[
\boxed{A_D B=0}.
\]

Since the connected homogeneous amplitude solution also has dimension six,

\[
\boxed{H_D^\circ=\operatorname{im}(B)}.
\]

Thus **all continuous D-amplitude freedom is gauge**.  No additional continuous moduli were missed by the previous root-of-unity witness construction.

## 3. The new discrete question

The remaining component group is

\[
\boxed{\pi_0(H_D)\cong\mathbb Z_2\times\mathbb Z_2}.
\]

Therefore existence of one exact D-amplitude witness per chirality does not, by itself, prove theorem-level exhaustiveness.

There are two possibilities:

1. the two `Z2` directions are images of **disconnected residual trivalent gauge transformations** that preserve the canonical scalar representative and Pauli seed slice; then all four amplitude components are gauge-equivalent and the existing downstream E/F/Phase-5 analysis remains exhaustive;
2. some torsion direction survives the full gauge stabilizer; then each chirality survivor splits into additional genuine D-amplitude branches, and those branches must be propagated through E/F/Phase 5 before a global non-categorifiability theorem can be claimed.

## 4. Current gate

The next verifier is

```text
experiments/r22_epsminus_d_discrete_gauge_audit.py
```

It includes both:

- the 29 multiplicity-one scalar trivalent gauge parameters;
- the scalar centers of the eight multiplicity-two fusion-space basis gauges.

It reconstructs their exact monomial action on all 24 Pauli seed D blocks and all 48 cross-D blocks.  It then computes the disconnected component group of the gauge stabilizer of

1. the canonical A/B/C scalar representative, and
2. the exact Pauli seed normalization,

and maps those disconnected gauge components into `pi_0(H_D)`.

The decisive criterion is whether this image has rank two over `F2` modulo the connected six-dimensional endpoint gauge.

## 5. Theorem boundary

Until that gate is resolved, the theorem-level statement

\[
R(2,2)\text{ is non-categorifiable}
\]

must remain **OPEN** even though every previously selected Phase-5 branch is obstructed.

This is precisely the kind of gap the fresh theorem audit was intended to expose: the issue is no longer local pentagon solving, but completeness of the quotient by residual gauge.
