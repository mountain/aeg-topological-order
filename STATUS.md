# Status

## Current stage

`T9 R(2,2) THEOREM-CLOSURE AUDIT — LOCAL/GAUGE BRANCH COMPLETENESS CLOSED / GLOBAL CASE LEDGER NEXT`

The theorem-completeness work remains on draft PR `#12`, branch `agent/r22-theorem-closure`. No theorem promotion or merge is authorized yet.

## Closed theorem gates

1. **Scalar A/B/C quotient.** Exactly 16 components modulo the full complex gauge torus:
   \[
   \epsilon_+: 0,1,2,3,8,9,10,11,
   \qquad
   \epsilon_-: 4,5,6,7,12,13,14,15.
   \]
   Archive: `notes/44-r22-scalar-component-inventory-audit.md`.

2. **Immediate local obstructions.** All eight epsilon-plus components and the four shallow epsilon-minus components `4,6,12,14` are excluded by independent executable local-F obstructions. Archive: `notes/43-r22-shallow-epsminus-local-f-closure.md` plus the epsilon-plus verifier.

3. **Pauli seed normal-form completeness.** For every deep scalar component `5,7,13,15`, the original seed-only D pentagons are exactly `24 singleton + 24 pair`. Across all four deep scalar components:
   \[
   96/96:\ U^2=I,
   \qquad
   96/96:\ \text{pairwise anticommutation}.
   \]
   Every invertible seed triple on each two-dimensional multiplicity space is therefore independently `GL_2(C)`-conjugate to
   \[
   \boxed{(X,Z,+Y)\text{ or }(X,Z,-Y)}.
   \]
   Hence the `2^8=256` chirality census is projectively exhaustive, not a restricted Pauli ansatz. Verifier: `experiments/r22_epsminus_seed_pauli_normal_form_audit.py`; Actions run `32394416585`; archive: `notes/56-r22-pauli-seed-normal-form-completeness.md`.

4. **Deep chirality census.** For each of `5,7,13,15`, all 256 chirality assignments are replayed exactly and reduce to the four masks
   \[
   \boxed{0,105,150,255},
   \]
   with profile `192 structural + 60 phase + 4 survivors`.

5. **D-amplitude quotient.** Every deep chirality survivor has exactly two gauge-inequivalent physical D-amplitude classes. The homogeneous cross-D group is
   \[
   H_D\cong(\mathbf C^*)^6\times\mu_2\times\mu_2,
   \]
   the connected six-dimensional part is endpoint gauge, disconnected scalar gauge removes one `Z2`, and the allowed Pauli projective normalizer does not remove the final one. Thus the exact deep physical frontier has
   \[
   4\times4\times2=32
   \]
   branches.

6. **Phases 1–4.** Both D-amplitude classes have exact D witnesses and all 32 physical deep branches pass Phases 1–4.

7. **Phase 5, class 0.** The accepted canonical chain closes all 16 class-0 deep branches.

8. **Phase 5, class 1.** The theorem audit closes all 16 newly exposed second-sheet branches:
   \[
   \boxed{5:4/4,\quad7:4/4,\quad13:4/4,\quad15:4/4}.
   \]
   Complete archive: `notes/55-r22-second-d-sheet-phase5-closure.md`.

The final previously open branch `component 13 / mask 255 / class 1` is `CLOSED / EXACT` by Actions run `32393826437`, with exact finite ledger
\[
18=2_{\rm affine}+4_{\rm p-rank11}+4_{\rm q-rank11}+8_{\rm rank10}=18_{\rm closed}.
\]
Archive: `notes/54-r22-second-d-sheet-component13-mask255-phase5-closure.md`.

## Current theorem boundary

All presently identified **local algebra, projective-normal-form, gauge-component, chirality, D-amplitude, and terminal Phase-5 branches are closed**. In particular, the previous two theorem-completeness gaps — the second physical D sheet and the Pauli seed ansatz — have both been removed by fresh exact replay.

This still does not by itself promote the global theorem. The remaining work is now proof assembly rather than a new local search.

## Open frontier — executable global case ledger

The next gate is to freeze one machine-checkable finite case tree:

\[
16\text{ scalar components}
\to
\begin{cases}
8\ \epsilon_+\text{ local-F leaves},\\
4\ \epsilon_-\text{ shallow local-F leaves},\\
4\ \epsilon_-\text{ deep components}.
\end{cases}
\]

For each deep component the ledger must record the exhaustive route

\[
256\text{ seed chirality assignments}
\to4\text{ masks}
\to2\text{ physical D classes}
\to8\text{ terminal leaves per scalar component},
\]

so that the deep part contains exactly

\[
4\times4\times2=32
\]

unique terminal leaves, with no omissions or duplicate quotient classes.

The ledger gate must also attach every leaf to an archived/executable terminal certificate. Only after this finite tree is frozen should the repository run the final canonical serial replay from a fresh state.

## Remaining sequence

1. close and archive the executable global case ledger;
2. run the final canonical theorem replay as serial sub-gates under the 10-minute/job guardrail;
3. write the theorem-level synthesis;
4. only then decide whether to promote
   \[
   \boxed{R(2,2)\text{ is non-categorifiable}.}
   \]

## Verification discipline

- full-complex gauge, not sign-only gauge;
- exact Smith/lattice calculations for monomial components;
- source-provenance terminal certificates;
- localization only after nonzeroness is proved;
- no global Gröbner solve;
- no floating-point nonlinear solve or continuation;
- 10-minute maximum per Actions research job;
- named `z_j` coordinates are implementation charts, not invariant theorem evidence.
