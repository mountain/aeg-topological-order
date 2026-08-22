# R(2,2) Open-Problem Source Ledger

> **Historical source status.** `R(2,2)` was adopted here as an unresolved target from the 2026 source literature. The theorem track in this repository subsequently closes that target: see `notes/59-r22-encoding-soundness-and-noncategorifiability.md` and `STATUS.md` for the current result. The descriptions below record what was known/imported at the point the benchmark was chosen.

## Meng--Yu 2026

Yue Meng and Zhiqiang Yu, *Classification of some Z/2Z x Z/2Z-quadratic fusion categories of rank 6*, arXiv:2608.06064 (2026).

- **CLASSICAL input:** definition of rank-six V4-quadratic rings and the self-dual family `R(m,n)`.
- **Target specialized here:** `R(2,2)` with simples `{1,g,h,gh,X,Y}`, `gX=Y`, and `X^2=1+h+2X+2Y`.
- **Open-problem role at adoption:** the paper is a partial categorification classification; `R(2,2)` entered this repository as an unresolved target rather than as a benchmark with known F-symbols.
- **Repository result:** the later exact theorem audit proves that `R(2,2)` is non-categorifiable over `C`; this conclusion is not imported from the source paper.
- **Not imported:** no associator/F-symbol solution for `R(2,2)` is assumed.

## Liu--Palcoux--Ren 2022/2026 version

Zhengwei Liu, Sebastien Palcoux, Yunxiang Ren, *Triangular Prism Equations and Categorification*, arXiv:2203.06522.

- **CLASSICAL methodological precedent:** in the spherical case the triangular-prism equations are equivalent to the pentagon equations up to change of basis.
- **Strategic relevance:** the work explicitly uses localization to manage categorification complexity and demonstrates that an equivalent coherence presentation can be substantially better as a solver representation.
- **AEG use here:** motivation only. The R(2,2) theorem engine uses the standard multiplicity-aware pentagon/invertibility problem; triangular-prism or spherical assumptions are not imported into the obstruction theorem.