# R(2,2) theorem audit — complete second D-amplitude sheet Phase-5 closure

## Status

**SECOND PHYSICAL D-AMPLITUDE SHEET: 16/16 CLOSED / EXACT.**

The theorem audit discovered that every deep epsilon-minus chirality survivor has two gauge-inequivalent physical cross-D amplitude classes.  The historical downstream calculation covered only class `0`.  This note freezes the complete downstream closure of the newly exposed class `1`.

## Ledger

For D-amplitude class `1`:

| scalar component | mask 0 | mask 105 | mask 150 | mask 255 |
|---|---:|---:|---:|---:|
| 5  | CLOSED | CLOSED | CLOSED | CLOSED |
| 7  | CLOSED | CLOSED | CLOSED | CLOSED |
| 13 | CLOSED | CLOSED | CLOSED | CLOSED |
| 15 | CLOSED | CLOSED | CLOSED | CLOSED |

Thus

\[
\boxed{16/16\text{ second-sheet Phase-5 branches are CLOSED / EXACT}.}
\]

The component-level archives are:

- components `7` and `15`: `notes/48-r22-second-d-sheet-17plus4-phase5-closure.md`;
- component `5`: `notes/50-r22-second-d-sheet-component5-phase5-closure.md`;
- component `13`, mask `0`: `notes/51-r22-second-d-sheet-component13-mask0-phase5-closure.md`;
- component `13`, mask `105`: `notes/52-r22-second-d-sheet-component13-mask105-phase5-closure.md`;
- component `13`, mask `150`: `notes/53-r22-second-d-sheet-component13-mask150-phase5-closure.md`;
- component `13`, mask `255`: `notes/54-r22-second-d-sheet-component13-mask255-phase5-closure.md`.

## What is now complete

The exact theorem audit has now established:

1. exactly 16 scalar A/B/C components modulo the full complex gauge torus;
2. complete epsilon-plus local-F obstruction;
3. complete shallow epsilon-minus local-F obstruction;
4. for each deep scalar component, exact Phase-1 chirality reduction
   \[
   256\to 4=\{0,105,150,255\};
   \]
5. two physical D-amplitude classes per deep chirality branch;
6. all 32 deep physical D branches pass Phases 1–4 exactly;
7. every class-0 Phase-5 branch has an exact terminal obstruction;
8. every class-1 Phase-5 branch now also has an exact terminal obstruction.

Hence the downstream branch ledger is no longer missing the second D-amplitude sheet.

## Remaining theorem boundary

A global theorem is still not promoted.  The next logical completeness question occurs **before** the chirality census: the historical D construction installs, on each two-dimensional multiplicity space, the exact seed triple

\[
X,\quad Z,\quad \chi Y,\qquad \chi\in\{\pm1\}.
\]

The remaining audit must prove that this is not merely a convenient ansatz: every invertible seed solution allowed by the original seed-only D pentagons must be obtainable from one of these Pauli/Clifford triples by an allowed `GL_2(C)` basis change, without leaving the already-audited canonical scalar A/B/C component.

Only after this Pauli seed normal-form gate is closed should the repository freeze the global case ledger and run the final canonical serial theorem replay.
