# R(2,2) theorem audit — second D-amplitude sheet through Phase 3

**Status:** `EXACT / 16-of-16 SECOND-SHEET BRANCHES E_PASS`

This note records the Phase-3 consequence of the D-amplitude completeness audit.
The earlier Phase-1 chirality frontier contains 16 deep scalar/chirality branches,
but the complete cross-D amplitude lattice has one additional gauge-inequivalent
`Z2` class on each branch.  Thus the theorem-level deep D frontier has 32 classes.

The second class is not discovered independently branch by branch.  A single
Smith-torsion generator of the common 168-by-48 D-amplitude exponent matrix
flips exactly eight cross-D amplitudes.  The resulting class was replayed in all
16 scalar/chirality branches against all 1728 original D-layer matrix entries.

This note asks the next question only: does that second D sheet survive the
complete E layer?

## 1. Representative comparison

The first fresh comparison used scalar component `5`, chirality mask `0`.
Both D-amplitude classes give exactly

- 1536 nonzero E equations;
- support profile `1536 x support-2`;
- exact E rank 126;
- E nullity 2;
- no identically zero required E determinant;
- determinant monomial profile

\[
16\times p^2,\qquad16\times q^2.
\]

For both classes an explicit exact point `p=q=1` makes all 32 required E blocks
invertible and replays all 1536 original E-layer matrix entries exactly.

Thus the second D class does not produce an E-layer obstruction on the first
representative branch.

GitHub Actions run: `32281036322`.

## 2. Complete second-sheet E census

The same exact gate was then replayed on all

\[
4\text{ deep scalar components}\times4\text{ chirality masks}=16
\]

second-sheet branches:

```text
components = 5,7,13,15
masks      = 0,105,150,255
D class    = 1
```

Every branch reports

```text
E_PASS
E equations = 1536
support     = {2: 1536}
rank        = 126
nullity     = 2
zero required determinant blocks = []
determinant term counts = {1: 32}
```

and every determinant profile is exactly

\[
\boxed{16\times(2,0)+16\times(0,2)}.
\]

All branches also admit the explicit exact point with both free E roots set to
1, and all 1536 original E pentagon entries replay to zero exactly.

The census has one and only one structural fingerprint variant:

```text
branches              = 16
statuses              = {'E_PASS': 16}
fingerprint_variants  = 1
variant_branch_counts = [16]
```

GitHub Actions run: `32281267232`.

## 3. Updated deep-frontier statement

The old theorem ledger treated the 16 scalar/chirality survivors as the complete
deep frontier.  The D-amplitude audit corrected this to 32 gauge-inequivalent D
classes.  Phase 3 now proves that **all 32** retain invertible E loci.

Equivalently, for every deep scalar component, every Phase-1 chirality survivor,
and both physical D-amplitude classes, the complete E layer has a genuine
2-dimensional invertible solution torus.

Therefore the newly discovered D torsion sheet is not removed at Phase 3.

## 4. Next gate

Do not assume that the second sheet inherits the historical Phase-4 F quotient.
The next serial gate is

\[
\boxed{\text{component 5 / mask 0 / D-amplitude class 1 at parametric Phase 4}.}
\]

It must rebuild the full 1312-entry F-linear coherence system over the fresh
second-sheet E torus and recompute every required 8x8/10x10 determinant
polynomial.  Only after that representative fingerprint is known should the
other 15 second-sheet branches be replayed.
