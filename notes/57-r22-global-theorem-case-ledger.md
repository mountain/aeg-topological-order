# R(2,2) theorem audit — executable global case ledger

## Status

**CLOSED / EXACT AS A FINITE COVERAGE LEDGER.**

This note freezes the finite quotient tree that connects the independently audited local/gauge gates to terminal obstructions.  It is a bookkeeping theorem gate: it does not replace the mathematical certificate attached to any leaf.

## 1. Scalar partition

The full-complex-gauge scalar quotient has exactly 16 components, partitioned without overlap as

\[
\epsilon_+:\quad 0,1,2,3,8,9,10,11,
\]

\[
\epsilon_-\text{ shallow}:\quad 4,6,12,14,
\]

\[
\epsilon_-\text{ deep}:\quad 5,7,13,15.
\]

Thus the scalar level is exhausted by

\[
\boxed{8+4+4=16}.
\]

The first eight terminate at the complete epsilon-plus local-F obstruction.  The four shallow epsilon-minus components terminate at the independent shallow local-F obstruction.

## 2. Deep projective frontier

The Pauli seed normal-form audit proves that the original seed-only D pentagons reduce every invertible seed triple, modulo independent `GL_2(C)` conjugation on each multiplicity-two space, to

\[
(X,Z,\pm Y).
\]

There are eight such spaces, hence the exhaustive projective seed frontier has

\[
2^8=256
\]

chirality assignments per deep scalar component.

Fresh D-layer replay reduces all 256 assignments to exactly the four masks

\[
\boxed{0,105,150,255}.
\]

## 3. Physical D-amplitude quotient

For every deep scalar/mask survivor, the full D-amplitude gauge audit gives exactly two gauge-inequivalent physical amplitude classes,

\[
\boxed{D\text{ class }0,\quad D\text{ class }1}.
\]

Therefore the physical deep frontier is exactly

\[
\boxed{
4\text{ deep scalars}
\times4\text{ chirality masks}
\times2\text{ D classes}
=32\text{ leaves}.
}
\]

The executable ledger verifies these 32 triples are unique and exhaustive.

## 4. Terminal certificates

Every class-0 deep leaf is attached to its accepted component-level Phase-5 synthesis:

- component 5: `notes/31-r22-component5-phase5-closure.md`;
- component 7: `notes/41-r22-component7-phase5-closure.md`;
- component 13: `notes/36-r22-component13-phase5-closure.md`;
- component 15: `notes/42-r22-component15-phase5-closure.md`.

Every class-1 deep leaf is attached to the theorem-audit second-sheet archives:

- component 5, all four masks: `notes/50-r22-second-d-sheet-component5-phase5-closure.md`;
- components 7 and 15, all four masks: `notes/48-r22-second-d-sheet-17plus4-phase5-closure.md`;
- component 13 masks 0/105/150/255: `notes/51`, `notes/52`, `notes/53`, `notes/54` respectively.

The ledger checks that every referenced archive/interface exists in the checked-out theorem branch and that every physical deep leaf receives exactly one certificate reference.

## 5. Global terminal count

The top-level theorem leaves are therefore

\[
8\ \epsilon_+\text{ local-F leaves}
+
4\ \epsilon_-\text{ shallow local-F leaves}
+
32\ \epsilon_-\text{ deep Phase-5 leaves}.
\]

Hence

\[
\boxed{44\text{ top-level terminal leaves}.}
\]

The executable gate rejects any overlap, missing scalar component, missing deep mask, missing D class, duplicate physical branch, or missing certificate artifact.

## 6. Executable replay

Verifier:

```text
experiments/r22_theorem_case_ledger.py
```

GitHub Actions:

```text
run 32394807045
job 96509129534
conclusion SUCCESS
```

Decisive output:

```text
scalar_components = 16
pauli_seed_chirality_assignments_per_deep_scalar = 256
deep_survivor_masks = [0,105,150,255]
physical_D_classes_per_survivor = [0,1]
physical_deep_terminal_leaves = 32
global_terminal_leaves = 44
```

followed by

```text
RESULT: the finite theorem case tree is exhaustive and non-overlapping: 8 epsilon-plus local-F leaves + 4 shallow epsilon-minus local-F leaves + 32 deep physical Phase-5 leaves = 44 terminal leaves, each attached to a frozen certificate
```

## 7. Theorem boundary after this node

No known quotient or branch-completeness gap remains in the finite case tree.  This is materially stronger than the historical state: the theorem audit has explicitly closed both the missing second D-amplitude sheet and the previously unproved Pauli seed normal form.

The remaining gate is now **canonical proof replay**, not discovery of another branch:

1. replay the scalar quotient and local obstruction gates from fresh state;
2. replay the seed normal form, chirality localization, and full D-amplitude quotient;
3. replay both D sheets through Phases 2–5 in serial theorem jobs;
4. require the replayed case counts to agree with this 44-leaf ledger;
5. only then synthesize and consider promotion of the global non-categorifiability theorem.

The 10-minute per-job guardrail remains mandatory; the final replay must be split rather than lengthened if any stage approaches the limit.
