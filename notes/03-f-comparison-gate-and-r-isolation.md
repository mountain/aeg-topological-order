# F comparison gate and R-isolation boundary

**Date:** 2026-08-17  
**Status:** post-freeze comparison; blind F derivation preserved  
**Prerequisites frozen before comparison:** `notes/01-blind-fibonacci-pentagon.md`, `experiments/fibonacci_pentagon.py`

## 0. Executive result

**COMPUTATIONAL-CLAIM.** The blind reconstruction produced, before any standard Fibonacci F table was consulted,

\[
a=\frac{\sqrt5-1}{2},\qquad
F^{\tau\tau\tau}_{\tau}
\sim
\begin{pmatrix}
a&\sqrt a\\
\sqrt a&-a
\end{pmatrix},
\qquad
F^{\tau\tau\tau}_{1}=1.
\]

**CLASSICAL.** Trebst--Troyer--Wang--Ludwig, arXiv:0902.3275, Sec. 2.4, use the basis order \(\{1,\tau\}\), normalize the trivial F-data to one, and give the nontrivial Fibonacci block as

\[
\begin{pmatrix}
\varphi^{-1}&\varphi^{-1/2}\\
\varphi^{-1/2}&-\varphi^{-1}
\end{pmatrix},
\qquad
\varphi=\frac{1+\sqrt5}{2}.
\]

**COMPUTATIONAL-CLAIM.** Since

\[
\frac{\sqrt5-1}{2}=\varphi^{-1},
\]

our real symmetric unitary gauge agrees entry-for-entry with this standard convention. No additional basis permutation or nontrivial gauge transformation is required after choosing \(b=c=\sqrt a\).

**CLASSICAL.** This is a successful reconstruction of known Fibonacci associator data, not a new topological invariant.

---

## 1. Audit order

**COMPUTATIONAL-CLAIM.** The blind derivation was committed before this comparison gate was opened:

- `experiments/fibonacci_pentagon.py` — initial blind engine commit `8003a82994ce49fab99b2fe7825a1ba55d417187`;
- `notes/01-blind-fibonacci-pentagon.md` — frozen derivation commit `12e8c10ca3a3f8efe24452834b461e015ea12e41`;
- `experiments/direct_pentagon_baseline.py` — independent direct-equation baseline commit `a5023056546da6ef394a6ab27b9ccfdfce9ef414`;
- `experiments/associahedron_k5.py` — five-input flatness verifier commit `3942e574c0d77927714eec6ed202d12a4aa8b0bc`.

**CLASSICAL.** The comparison source was therefore not an input to the polynomial derivation or unitary branch selection.

---

## 2. Exact convention match

**CLASSICAL.** The comparison reference treats fusion-tree labelings as orthonormal bases and F-moves as unitary changes of basis.

**CLASSICAL.** It uses the central-channel basis order \(\{1,\tau\}\).

**CLASSICAL.** Its unit/trivial F-symbol normalization agrees with the strict-unit convention used by this project at the comparison point.

**COMPUTATIONAL-CLAIM.** Our symbolic matrix was stored with old intermediate channel as the first index and new intermediate channel as the second index. In the chosen symmetric gauge transposition conventions become immaterial for this particular block, because the recovered matrix is real symmetric.

**COMPUTATIONAL-CLAIM.** The equality

\[
a=\varphi^{-1},\qquad \sqrt a=\varphi^{-1/2}
\]

establishes exact entrywise agreement with the standard block.

---

## 3. What the comparison does and does not establish

**CLASSICAL.** It establishes that the blind pentagon reconstruction has landed on the standard unitary Fibonacci associator in the stated convention.

**COMPUTATIONAL-CLAIM.** Together with the independent direct-pentagon baseline, this strongly checks that the history-engine indexing and path-composition conventions are correct at the F level.

**CLASSICAL.** It does not establish any computational advantage for AEG; `notes/02-direct-baseline-k5-and-holonomy-boundary.md` records that the optimized direct categorical baseline yields the same five symbolic variables and the same pentagon polynomial system.

**CLASSICAL.** It does not establish nontrivial topological holonomy for F-moves. Pure reassociation remains coherent/flat.

---

## 4. R-isolation boundary

**CLASSICAL.** The same standard Fibonacci reference proceeds immediately from its F-matrix discussion to R-matrices and hexagon/braiding data.

**COMPUTATIONAL-CLAIM.** During the F-comparison lookup, the current research session was exposed to a source that contains explicit standard Fibonacci R-data. Those values are intentionally **not copied into this repository**.

**CLASSICAL.** Under `AGENTS.md` rule 3, this workstream must therefore not claim a subsequent R reconstruction to be blind.

**REFORMULATION.** The correct research-process analogue of a clean-room experiment is now:

1. freeze the allowed braided input grammar before a new workstream starts;
2. permit that workstream to use the already reconstructed F-data;
3. prohibit access to comparison sources containing explicit Fibonacci R-values until its symbolic hexagon solve is frozen;
4. only then open the R-comparison gate.

**COMPUTATIONAL-CLAIM.** This branch stops before symbolic R/hexagon reconstruction for that reason. The stop is methodological, not mathematical.

---

## 5. Frozen inputs proposed for a fresh blind R workstream

**CLASSICAL.** Allowed:

- simple labels \(\{1,\tau\}\) and Fibonacci fusion grammar;
- the now independently reconstructed and comparison-verified F-data;
- strict-unit normalization;
- braiding as an unknown natural isomorphism represented by channelwise symbolic R-data;
- hexagon coherence;
- unitarity, with its exact point of use declared.

**CLASSICAL.** Forbidden until the next comparison gate:

- numerical/closed-form standard Fibonacci R-symbols;
- known braid-generator matrices containing those phases;
- modular S/T data or topological spins that algebraically reveal the same phases;
- any reference section that tabulates the forbidden values.

**REFORMULATION.** The target object for the next stage should be the enlarged fusion--braid history groupoid: F-edges remain flat chart changes, R-edges supply exchange primitives, and hexagon cells impose compatibility. Gauge-invariant braid holonomy is the first place where a genuinely nontrivial global history transport is expected.

---

## 6. Reference

**CLASSICAL.** Simon Trebst, Matthias Troyer, Zhenghan Wang, Andreas W. W. Ludwig, *A short introduction to Fibonacci anyon models*, arXiv:0902.3275, especially Secs. 2.3--2.4 for fusion-tree bases, pentagon coherence, normalization, and the standard F-matrix. This source is **comparison-only** for explicit Fibonacci constants.
