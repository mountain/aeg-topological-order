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

## Active ledger — Fibonacci F stage and braided follow-up

### Aboumrad 2022 — multiplicity-free F/R framework and solver baseline

- **Source:** Willie Aboumrad, *Quantum computing with anyons: an F-matrix and braid calculator*, arXiv:2212.00831.
- **CLASSICAL — F-stage data used:** multiplicity-free fusion-tree basis conventions; F-moves as changes of fusion basis; pentagon coherence as polynomial constraints; direct symbolic/Groebner solving as a computational baseline.
- **CLASSICAL — braided-stage data used:** the generic multiplicity-free hexagon equation, Eq. (2.3), and the standard fact that F/R data compile braid-group representations.
- **Normalization used here:** triangle/strict-unit F normalization and vacuum R normalization; the project keeps its own explicit basis ordering.
- **Allowed input:** generic categorical definitions and generic pentagon/hexagon formulas.
- **Not used as input:** any pre-tabulated numerical Fibonacci F/R values or preferred Fibonacci braid matrices.
- **COMPUTATIONAL-CLAIM — benchmark relevance:** the paper emphasizes that hexagon equations are more localized than pentagons; this supports testing sparse/local equation organization but does not establish an AEG advantage.

### Levin–Wen 2004 — string-net program

- **Source:** Michael A. Levin and Xiao-Gang Wen, *String-net condensation: A physical mechanism for topological phases*, arXiv:cond-mat/0404617.
- **CLASSICAL — data used now:** none in the F/R reconstruction calculations.
- **Comparison/later use:** target reference for the M6/T6 string-net compilation stage and for keeping the physical topological-order objective distinct from the associator/braiding benchmarks.
- **No model-specific recoupling values** have been used to seed the F or R symbolic solves.

### Trebst--Troyer--Wang--Ludwig 2009 — post-freeze Fibonacci F comparison

- **Source:** Simon Trebst, Matthias Troyer, Zhenghan Wang, Andreas W. W. Ludwig, *A short introduction to Fibonacci anyon models*, arXiv:0902.3275, Secs. 2.3--2.4.
- **CLASSICAL — comparison data:** fusion-tree basis, F-moves, pentagon consistency, basis order `\{1,\tau\}`, standard trivial-F normalization, and the standard nontrivial unitary Fibonacci F block.
- **Comparison status:** **comparison-only for explicit Fibonacci constants**; opened only after `notes/01-blind-fibonacci-pentagon.md` and the blind engine had been frozen in Git history.
- **COMPUTATIONAL-CLAIM — F comparison result:** our real symmetric unitary gauge agrees entry-for-entry after identifying `a=(sqrt(5)-1)/2=phi^{-1}` and `sqrt(a)=phi^{-1/2}`.
- **R-isolation warning:** the same source continues to explicit R/hexagon material. Therefore the current lineage is not eligible to claim a blind R reconstruction. Explicit standard R-values remain intentionally absent from the repository.

### Moriwaki 2022 — parenthesized braid operad originality audit

- **Source:** Yuto Moriwaki, *Vertex operator algebra and parenthesized braid operad*, arXiv:2209.10443.
- **CLASSICAL — result relevant here:** the parenthesized braid operad is described via fundamental groupoids of configuration spaces and acts by monodromy in the conformal-block setting.
- **Research consequence:** the bare combinatorics “parenthesization + braid/exchange morphisms + monodromy/coherence” is classical and must not be advertised as an AEG novelty.
- **AEG-specific question left open:** whether attaching explicit operation histories, sparse transport certificates, compiler IR, or representation-complexity semantics gives practical or structural value beyond the classical parenthesized-braid framework.
- **No model-specific Fibonacci constants** are imported from this source.

### AEG upstream — explicit path / holonomy calibration

- **Source:** `mountain/aeg-paper/notes/foundations-and-geometry/04-affine-torus-holonomy.tex`.
- **Blob revision used:** `de501e888110f887815328ae4524c602698e6a38`.
- **AEG-UPSTREAM — idea used:** retain operation histories explicitly, attach local group-valued transports, and distinguish local face relations from global path holonomy.
- **Not imported:** the affine group, its commutator/torsion values, or any claim that fusion pentagons/hexagons possess the same curvature interpretation.

### Three-body methodological calibration — rank must emerge

- **Source:** `mountain/three-body/docs/note_04.md`, blob `6d7c5198df5fdb782a03dd7b342a4aa057bc039c`.
- **Source:** `mountain/three-body/docs/note_05.md`, blob `023dab383fec9375dd02fc2b7f1823144c685f41`.
- **AEG-UPSTREAM — idea used:** diagnose the representation/ruler structure selected by the problem rather than postulating a Hyperoperation rank in advance.
- **Not imported:** three-body-specific `SL(2,R)/SO(2)`, Busemann, contact, or Casimir geometry.

---

## Reconstruction and comparison gate policy

- **CLASSICAL.** The F derivation in `notes/01-blind-fibonacci-pentagon.md` was frozen before opening sources that provide explicit standard Fibonacci F values.
- **CLASSICAL.** The F comparison records basis order, vertex gauge, and unitary/normalization conventions in `notes/03-f-comparison-gate-and-r-isolation.md`.
- **PROTOCOL.** The symbolic R/hexagon derivation in `notes/04-symbolic-braiding-history-quotient.md` contains no explicit standard R constants but is **not blind**, because its workstream descends from the source-exposed F-comparison session.
- **PROTOCOL.** Any future claim of blind Fibonacci R reconstruction requires a genuinely independent workstream that receives only the fusion grammar and frozen F-data and does not open explicit Fibonacci R-symbols, braid matrices, modular data, or topological-spin data before its solve is frozen.
