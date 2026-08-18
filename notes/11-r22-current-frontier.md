# R(2,2) Current Frontier

**Date:** 2026-08-17

The localization audit is now frozen.  The next unresolved step is no longer the raw pentagon system.

## Exact reductions already obtained

- scalar A/B/C layer: 153 variables, rank-129 monomial system, effective gauge rank 24, hence no continuous moduli;
- scalar component group at this layer: `(Z/2)^4`;
- stabilizer signs collapse to one `epsilon = +/-1`;
- D stabilizer blocks reduce to commuting involutions (`epsilon=+1`) or Pauli/Clifford triples (`epsilon=-1`);
- trivial lower branch is excluded because F-layer coherence makes all eight 10x10 associator blocks singular;
- a concrete `epsilon=-1` scalar representative extends through the 24 Pauli D seeds;
- the other 48 D blocks each have a one-dimensional local intertwiner space with an invertible representative.

## Immediate unresolved kernel

The next exact task is to restore scalar amplitudes on those 48 projective D intertwiners and solve their residual multiplicative consistency.  Only after that should E and F be compiled for the `epsilon=-1` branch.

A numerical phase solve has been used only as reconnaissance and indicates that the residual D amplitude system is likely consistent; it is **not** yet accepted as proof.  The repository must next produce an exact lattice/congruence certificate or an exact obstruction.

## Compute rule

Do not increase symbolic timeouts.  The failed 120-second generic SymPy construction has already shown that expression-level representation is the wrong layer for large linear subsystems.  Continue with integer lattices, sparse linear IR, and exact low-dimensional matrix algebra.
