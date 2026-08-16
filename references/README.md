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

## Active ledger — Fibonacci F stage, braiding, and string-net compilation

### Aboumrad 2022 — multiplicity-free F/R framework and solver baseline

- **Source:** Willie Aboumrad, *Quantum computing with anyons: an F-matrix and braid calculator*, arXiv:2212.00831.
- **CLASSICAL — F-stage data used:** multiplicity-free fusion-tree basis conventions; F-moves as changes of fusion basis; pentagon coherence as polynomial constraints; direct symbolic/Groebner solving as a computational baseline.
- **CLASSICAL — braided-stage data used:** the generic multiplicity-free hexagon equation, Eq. (2.3), and the standard fact that F/R data compile braid-group representations.
- **Normalization used here:** triangle/strict-unit F normalization and vacuum R normalization; the project keeps its own explicit basis ordering.
- **Allowed input:** generic categorical definitions and generic pentagon/hexagon formulas.
- **Not used as input:** any pre-tabulated numerical Fibonacci F/R values or preferred Fibonacci braid matrices.
- **COMPUTATIONAL-CLAIM — benchmark relevance:** the paper emphasizes that hexagon equations are more localized than pentagons; this supports testing sparse/local equation organization but does not establish an AEG advantage.

### Levin–Wen 2004 — string-net Hamiltonian and plaquette baseline

- **Source:** Michael A. Levin and Xiao-Gang Wen, *String-net condensation: A physical mechanism for topological phases*, arXiv:cond-mat/0404617; Phys. Rev. B 71, 045110 (2005).
- **CLASSICAL — data now used directly:** the honeycomb/trivalent string-net Hamiltonian; vertex branching constraints; the plaquette decomposition `B_p = sum_s a_s B_p^s`; and the matrix-element formula expressing `B_p^s` as a cyclic product of local F-symbols around the plaquette.
- **CLASSICAL — normalization used:** for the smooth topological phase, the coefficient of loop type `s` is proportional to its quantum dimension, `a_s = d_s / sum_i d_i^2`.
- **CLASSICAL — algebra used as validation target:** loop-insertion operators compose according to the fusion rules, and the quantum-dimension weighted `B_p` is a projector.
- **COMPUTATIONAL-CLAIM — project use:** `experiments/levin_wen_plaquette.py` specializes the formula to the frozen Fibonacci F-gauge and verifies the fusion algebra/projector identities exactly in all 64 hexagonal external-label sectors.
- **Research consequence:** the physical string-net model remains entirely classical input; AEG is tested only as an alternative representation/certificate layer.

### Bonesteel–DiVincenzo 2012 — local F-move circuit baseline

- **Source:** N. E. Bonesteel and D. P. DiVincenzo, *Quantum Circuits for Measuring Levin-Wen Operators*, arXiv:1206.6048; Phys. Rev. B 86, 165113 (2012).
- **CLASSICAL — result relevant here:** the Fibonacci Levin–Wen vertex and plaquette operators can be measured/compiled using local categorical transformations, including explicit F-move circuits.
- **CLASSICAL — complexity relevance:** the paper explicitly studies circuit/gate complexity rather than treating the plaquette as a naive dense matrix.
- **Benchmark consequence:** an AEG history compiler must be compared with optimized local F-move/circuit formulations, not only with full matrix materialization.
- **No new Fibonacci constants** are imported from this source for the plaquette experiment; the project uses its already-frozen F-stage gauge.

### Gu–Levin–Swingle–Wen 2008 — tensor-product string-net representation

- **Source:** Zheng-Cheng Gu, Michael Levin, Brian Swingle, Xiao-Gang Wen, *Tensor-product representations for string-net condensed states*, arXiv:0809.2821.
- **CLASSICAL — result relevant here:** general string-net condensed states admit natural tensor-product-state representations built from local tensors.
- **Originality consequence:** locality and compact tensor-network representation of string-net data are established prior art; an O(n) local factor representation of an n-gon plaquette is not by itself an AEG novelty.

### Buerschaper–Aguado–Vidal 2008 — explicit string-net tensor network

- **Source:** O. Buerschaper, M. Aguado, G. Vidal, *Explicit tensor network representation for the ground states of string-net models*, arXiv:0809.2393.
- **CLASSICAL — result relevant here:** string-net ground states have explicit tensor-network representations constructed from the underlying tensor-category data.
- **Originality consequence:** a history DAG that canonicalizes to the same local tensor network must be treated as a reformulation unless it supplies additional proof/provenance functionality with measurable value.

### Trebst--Troyer--Wang--Ludwig 2009 — post-freeze Fibonacci F comparison

- **Source:** Simon Trebst, Matthias Troyer, Zhenghan Wang, Andreas W. W. Ludwig, *A short introduction to Fibonacci anyon models*, arXiv:0902.3275, Secs. 2.3--2.4.
- **CLASSICAL — comparison data:** fusion-tree basis, F-moves, pentagon consistency, basis order `\{1,\tau\}`, standard trivial-F normalization, and the standard nontrivial unitary Fibonacci F block.
- **Comparison status:** **comparison-only for explicit Fibonacci constants**; opened only after `notes/01-blind-fibonacci-pentagon.md` and the blind engine had been frozen in Git history.
- **COMPUTATIONAL-CLAIM — F comparison result:** our real symmetric unitary gauge agrees entry-for-entry after identifying `a=(sqrt(5)-1)/2=phi^{-1}` and `sqrt(a)=phi^{-1/2}`.
- **R-isolation warning:** the same source continues to explicit R/hexagon material. Therefore the braided lineage is not eligible to claim a blind R reconstruction. Explicit standard R-values remain intentionally absent from the repository.

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
- **CLASSICAL.** The Levin–Wen/string-net stage is not a reconstruction gate: the plaquette formula is intentionally used as the physical/categorical baseline. Any AEG claim must be a representation, compilation, or certificate claim measured against that baseline.
