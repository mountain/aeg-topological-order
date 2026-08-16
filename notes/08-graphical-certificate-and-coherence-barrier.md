# Round 3 — Graphical Certificate Extraction and the Coherence-Quotient Barrier

**Stage:** T8 closure / proof-certificate audit  
**Date:** 2026-08-17  
**Code:** `experiments/plaquette_commutation_certificate.py`

---

## 0. Executive conclusion

The adjacent-plaquette benchmark has now reached the stop condition that was built into the research protocol.

**CLASSICAL.** Levin and Wen already give a constant-size graphical proof that adjacent plaquette operators commute. In the fattened-lattice representation, \(B_p^s\) is simply insertion of an \(s\)-loop around plaquette \(p\). Applying two neighboring plaquette operators in either order produces the same two-loop intermediate diagram; coherent local-rule reduction then gives identical physical matrix elements.

**REFORMULATION.** `experiments/plaquette_commutation_certificate.py` encodes this proof as an explicit operation-history diamond / proof DAG.

**NEGATIVE BENCHMARK.** The extracted history certificate does not improve on the optimized categorical baseline. It is a machine-readable restatement of the classical Levin–Wen graphical proof.

This closes the strongest remaining claim from the preceding stages:

\[
\boxed{
\text{AEG history IR has not shown a fusion/string-net-specific}\
\text{compression or proof advantage beyond categorical graphical calculus.}
}
\]

The negative result is not that explicit history is useless. It is that **this exact use of explicit history is already native to the relevant categorical/string-net formalism.**

---

# 1. The direct baseline and the proof baseline are fundamentally different objects

`notes/07-adjacent-plaquette-commutation.md` established a complete instantiated baseline on two adjacent Fibonacci hexagons.

For the maximal all-\(\tau\) external sector:

\[
\dim \mathcal H=170,
\]

\[
\operatorname{nnz}(B_L^\tau)
=
\operatorname{nnz}(B_R^\tau)
=1551,
\]

and each ordered product has

\[
11922
\]

nonzero entries after exact reduction. The direct sparse composition performs

\[
14854
\]

nonzero scalar multiplications before accumulation in each order.

**COMPUTATIONAL-CLAIM.** All 256 external-label sectors satisfy

\[
B_L^\tau B_R^\tau=B_R^\tau B_L^\tau
\]

exactly.

That calculation is an **instantiated semantic verifier**.

It is not the right proof-complexity baseline.

---

# 2. The classical graphical lift

**CLASSICAL.** In Appendix C of Levin–Wen, the honeycomb lattice is fattened into strips. A string-net state in the fattened lattice is reduced to a linear combination of ordinary lattice states by the local string-net rules.

Crucially, this reduction is independent of the particular order in which the local rules are applied, provided the rules are self-consistent.

Let

\[
\mathcal R:
\mathcal H_{\mathrm{fat}}
\longrightarrow
\mathcal H_{\mathrm{physical}}
\]

denote this coherent reduction map.

For every plaquette \(p\) and loop type \(s\), introduce the graphical insertion operation

\[
I_p^s:
X\longmapsto X\cup \ell_p^s,
\]

where \(\ell_p^s\) is an \(s\)-loop around the plaquette.

The graphical semantics is

\[
\boxed{
B_p^s=\mathcal R\circ I_p^s.
}
\tag{1}
\]

Equation (1) is not an AEG reinterpretation invented here; it is precisely the content of the classical graphical representation of the Levin–Wen Hamiltonian.

---

# 3. Adjacent commutation is a common-apex certificate

Let \(L,R\) be adjacent plaquettes.

Starting from an arbitrary admissible state \(X\), consider the two insertion schedules:

\[
X
\xrightarrow{I_R^{s_R}}
X\cup\ell_R^{s_R}
\xrightarrow{I_L^{s_L}}
X\cup\ell_R^{s_R}\cup\ell_L^{s_L},
\]

and

\[
X
\xrightarrow{I_L^{s_L}}
X\cup\ell_L^{s_L}
\xrightarrow{I_R^{s_R}}
X\cup\ell_L^{s_L}\cup\ell_R^{s_R}.
\]

At the fattened-diagram level the terminal objects are literally identical:

\[
\boxed{
I_L^{s_L}I_R^{s_R}X
=
I_R^{s_R}I_L^{s_L}X.
}
\tag{2}
\]

Applying the same coherent reduction \(\mathcal R\) gives

\[
\boxed{
B_L^{s_L}B_R^{s_R}X
=
B_R^{s_R}B_L^{s_L}X.
}
\tag{3}
\]

Thus the certificate is not a long chain of Fibonacci-specific polynomial cancellations. It is a **diamond with a common graphical apex**.

---

# 4. Machine representation

**REFORMULATION.** `experiments/plaquette_commutation_certificate.py` represents a fattened state by

\[
(\text{base state},\;\{\text{inserted loops}\}),
\]

with loop insertions recorded canonically as an unordered set of face/label decorations.

The two schedules normalize to the same object structurally, without evaluating any F-symbol.

The proof DAG has constant size:

- 5 explicit proof/history nodes;
- 4 explicit history edges;
- zero coefficient arithmetic;
- trusted semantic boundary: graphical semantics of \(B_p^s\) and coherent reduction.

Its size is independent of the Hilbert-space block dimension.

**COMPUTATIONAL-CLAIM.** This should be contrasted with the largest instantiated benchmark above only to illustrate the distinction between **semantic evaluation** and **structural proof**.

It must not be used to claim AEG compression against a naive matrix implementation.

---

# 5. Why this is a negative AEG benchmark

The obvious attractive statement would be:

> explicit operation history compresses a 170-dimensional operator equality into a five-node certificate.

That statement is technically true but scientifically misleading.

**CLASSICAL.** Levin–Wen Appendix C already performs exactly this compression by passing from the algebraic matrix elements to the fattened graphical representation. The adjacent-plaquette proof is already a common-intermediate-diagram argument.

Therefore:

\[
\boxed{
\text{history-DAG compression}
=
\text{classical graphical-calculus compression}
}
\]

for this benchmark.

**NEGATIVE BENCHMARK.** No AEG-specific certificate-size advantage has been demonstrated.

**NEGATIVE BENCHMARK.** No AEG-specific proof-reuse mechanism has been demonstrated: the classical graphical proof is already uniform in the boundary labels and Hilbert-space dimension.

**NEGATIVE BENCHMARK.** No AEG-specific incremental-verification advantage has been demonstrated: the proof depends on local graphical semantics and coherence rather than on enumerating the affected matrix entries.

This satisfies the repository stop condition for the present line of attack.

---

# 6. The coherence-quotient barrier

The repeated negative results from the F, braid, and string-net stages can be summarized by a simple structural obstruction.

Let \(\mathsf H(x,y)\) be a set of explicit operation histories between two fixed presentations \(x,y\). Let

\[
\sim_{\mathrm{coh}}
\]

be the equivalence relation generated by the relevant coherence cells:

- triangle/pentagon for monoidal reassociation;
- hexagon for compatibility of braiding and fusion;
- the corresponding graphical local relations for string-nets.

Suppose an AEG quantity

\[
J:\mathsf H(x,y)\to S
\]

is proposed as an invariant of the exact categorical/topological structure.

There are two possibilities.

## Case A — \(J\) is coherence invariant

If

\[
h_1\sim_{\mathrm{coh}}h_2
\Longrightarrow
J(h_1)=J(h_2),
\]

then \(J\) factors through the coherence quotient:

\[
\mathsf H(x,y)
\longrightarrow
\mathsf H(x,y)/\!\sim_{\mathrm{coh}}
\longrightarrow S.
\]

**CLASSICAL.** For pure reassociation, monoidal coherence identifies all parallel reassociation composites. Therefore no nontrivial invariant of the reassociation *history itself* survives for fixed endpoints.

**CLASSICAL.** In the braided case, nontrivial braid classes survive, but those classes and their representations are already the categorical/braid-group data.

**REFORMULATION.** Thus a coherence-invariant AEG history quantity either becomes trivial on pure F-history or factors through already-known categorical/topological semantics.

## Case B — \(J\) distinguishes coherence-equivalent histories

If

\[
h_1\sim_{\mathrm{coh}}h_2
\quad\text{but}\quad
J(h_1)\ne J(h_2),
\]

then \(J\) does not descend to the categorical object.

It may still be meaningful, but only after giving the history an additional semantics such as:

- computational cost;
- memory footprint;
- provenance;
- numerical error;
- uncertainty;
- physical time or control path;
- implementation constraints.

Such a quantity is an **enrichment of the presentation/process**, not a topological invariant supplied by the fusion category itself.

---

# 7. A useful dichotomy for the AEG program

The barrier can be stated compactly as

\[
\boxed{
\begin{array}{c}
\text{history quantity invariant under coherence}\\
\Downarrow\\
\text{factors through categorical semantics}\\[6pt]
\text{history quantity not invariant under coherence}\\
\Downarrow\\
\text{requires extra process/computational semantics}.
\end{array}}
}
\]

This is not claimed as a new category-theoretic theorem. It is a strategic consequence of classical coherence for the AEG research program.

It explains why three apparently different experiments converged to the same negative result:

| benchmark | explicit-history object | classical quotient/baseline | result |
|---|---|---|---|
| F/pentagon | reassociation paths | coherent associator | same polynomial/coherence data |
| R/braid | fusion–exchange paths | parenthesized braid groupoid / braid representation | same surviving holonomy |
| string-net | loop insertion + reduction histories | graphical calculus | same constant-size proof |

---

# 8. What remains genuinely open

The negative result does **not** imply that operation history can never be useful. It sharply changes the type of question that remains legitimate.

## Direction 1 — computational enrichment

Define a history weight or resource functor

\[
W:\mathsf H\to\mathcal R
\]

where \(\mathcal R\) records actual resources: arithmetic operations, memory, communication, proof-checking work, or dependency sets.

Then study optimization over a coherence class:

\[
\boxed{
\min_{h\in[h_0]_{\mathrm{coh}}} W(h).
}
\]

This would make the retained history mathematically relevant because coherence supplies the space of equivalent implementations while the enrichment supplies a nontrivial objective.

This is closer to compiler theory / proof optimization than to a new theory of topological order.

## Direction 2 — approximate or defective coherence

For learned, truncated, noisy, or approximate F/R data, pentagon/hexagon cells need not close exactly.

Then two nominally equivalent histories can differ:

\[
\Delta(h_1,h_2)
e0.
\]

An explicit history complex could organize and localize these coherence defects.

Again, this would be an error-diagnostic/enriched problem rather than a new invariant of an exact fusion category.

## Direction 3 — physical process semantics beyond topological equivalence

If histories correspond to actual controlled processes with time, energy, locality, or noise constraints, then different coherent categorical presentations may be physically inequivalent as implementations.

AEG could then study geometry on the implementation space rather than on the exact topological quotient.

---

# 9. Recommended research decision

**NEGATIVE BENCHMARK.** Do not continue scaling the exact Fibonacci fusion/string-net calculations merely by increasing anyon count, plaquette count, or matrix dimension. The current evidence predicts that optimized categorical graphical/tensor methods will continue to absorb the same locality and coherence structure.

**REFORMULATION.** Treat the current repository as having established a useful negative theorem-of-practice:

> For exact Fibonacci fusion, braiding, and Levin–Wen string-net operations, explicit operation history faithfully reproduces the categorical graphical structure, but no independent AEG invariant or computational advantage survives once the baseline is optimized.

The next topological-order experiment, if pursued, should therefore **add an explicit enrichment that category coherence deliberately forgets** rather than re-encode more exact categorical data.

The cleanest candidate is a resource-enriched history groupoid:

\[
\boxed{
(\text{coherence class},\;\text{cost/provenance/dependency geometry}).
}
\]

This would convert the coherence quotient from an obstacle into the feasible set of an optimization problem.

---

# 10. Stage closure

The project has now answered the original red-team question

> Does AEG merely redraw a fusion category as a graph?

for the Fibonacci exact-category benchmark with considerably more precision:

**COMPUTATIONAL-CLAIM.** At the level of F/R equations, local braid blocks, plaquette factorization, and adjacent-plaquette proof certificates, the explicit-history representation has not produced structure that is absent from optimized categorical graphical methods.

**REFORMULATION.** AEG can still be used as a systematic language for making those histories explicit.

**NEGATIVE BENCHMARK.** But explicitness alone is not yet a mathematical or computational advantage.

This is the correct point to stop the un-enriched exact-category line and decide whether to proceed with a resource/defect enrichment or redirect the broader AEG program to a problem where operation history is not already annihilated by a strong coherence quotient.
