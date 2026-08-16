# References Ledger

Prioritize primary papers and standard mathematical references.

Initial buckets:

1. Wen topological order / quantum order / long-range entanglement;
2. Levin–Wen string-net models;
3. Fibonacci anyons and modular/fusion category conventions;
4. F-symbol, pentagon, R-symbol, hexagon computation;
5. categorical / algebraic higher symmetry;
6. computational solvers for fusion categories and braid representations.

For each source record:

- exact data/axiom/result used;
- gauge and normalization conventions;
- whether the result is allowed as reconstruction input or comparison only;
- computational complexity information, if any.

---

## Active ledger — blind Fibonacci reconstruction

### Aboumrad 2022 — multiplicity-free F-matrix / pentagon solver

- **Source:** Willie Aboumrad, *Quantum computing with anyons: an F-matrix and braid calculator*, arXiv:2212.00831.
- **CLASSICAL — data used:** multiplicity-free fusion-tree basis conventions; F-moves as changes of fusion basis; pentagon coherence as polynomial constraints; direct symbolic/Groebner solving as a computational baseline.
- **CLASSICAL — normalization used here:** only the triangle/strict-unit statement is imported into the blind grammar; the project keeps its own explicit basis ordering.
- **Allowed during blind reconstruction:** yes, for general categorical definitions and the pentagon formalism.
- **Forbidden during blind reconstruction:** any pre-tabulated numerical Fibonacci F/R data or preferred Fibonacci gauge.
- **COMPUTATIONAL-CLAIM — benchmark relevance:** the paper notes that generic pentagon solving becomes difficult and motivates sparse equation engineering; this is relevant to T5 but does not establish an AEG advantage.

### Levin–Wen 2004 — string-net program

- **Source:** Michael A. Levin and Xiao-Gang Wen, *String-net condensation: A physical mechanism for topological phases*, arXiv:cond-mat/0404617.
- **CLASSICAL — data used now:** none in the blind F solve.
- **Comparison/later use:** target reference for the M6/T6 string-net compilation stage and for keeping the physical topological-order objective distinct from the current associator benchmark.
- **Allowed during blind reconstruction:** conceptual context only.
- **Forbidden during blind reconstruction:** no model-specific recoupling values may be used to seed the F solve.

### AEG upstream — explicit path / holonomy calibration

- **Source:** `mountain/aeg-paper/notes/foundations-and-geometry/04-affine-torus-holonomy.tex`.
- **Blob revision used:** `de501e888110f887815328ae4524c602698e6a38`.
- **AEG-UPSTREAM — idea used:** retain operation histories explicitly, attach local group-valued transports, and distinguish local face relations from global path holonomy.
- **Not imported:** the affine group, its commutator/torsion values, or any claim that fusion pentagons possess the same curvature interpretation.

### Three-body methodological calibration — rank must emerge

- **Source:** `mountain/three-body/docs/note_04.md`.
- **Blob revision used:** `6d7c5198df5fdb782a03dd7b342a4aa057bc039c`.
- **Source:** `mountain/three-body/docs/note_05.md`.
- **Blob revision used:** `023dab383fec9375dd02fc2b7f1823144c685f41`.
- **AEG-UPSTREAM — idea used:** diagnose the representation/ruler structure selected by the problem rather than postulating a Hyperoperation rank in advance.
- **Not imported:** three-body-specific `SL(2,R)/SO(2)`, Busemann, contact, or Casimir geometry.

---

## Comparison gate policy

- **CLASSICAL.** The derivation in `notes/01-blind-fibonacci-pentagon.md` must be frozen before opening sources that provide explicit standard Fibonacci F/R values for comparison.
- **CLASSICAL.** Once the gate is opened, comparison notes must record basis order, vertex gauge, pivotal/unitary normalization, and any convention changes before declaring equality of matrices.
