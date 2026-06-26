# AI-Assisted Exploration: Exact Metric Properties of the Modular Syracuse Graph G_p

**Status:** Computational draft / awaiting expert validation  
**Date:** June 2026  
**Author:** BESSIERE Josselin

---

## What this is

This repository contains a draft exploring the structural properties of the modular Syracuse graph 
G_p defined on Z/2^pZ. The work was produced through an iterative human-AI collaboration:

- **Human contribution:** formulation of the research question, structural intuition, 
  guidance of the exploration direction, and evaluation of plausibility through numerical 
  verification (e.g., p=3 adjacency matrix powers) and consistency checks.
- **Computational contribution:** formal derivations, LaTeX drafting, proof structuring, 
  and symbolic verification.

**Important:** I do not have formal training in advanced mathematics. I cannot independently 
verify every step of the proofs presented here. This document is offered as a **conjectural 
draft** for expert evaluation, not as a peer-reviewed theorem.

---

## How this was made

This draft was generated through iterative dialogue with a large language model (Claude/GPT). 
The human author posed questions, requested formalizations, and selected coherent directions 
from multiple AI-generated proposals. The AI handled the technical execution (proof writing, 
LaTeX formatting, symbolic computation). The human author verified that the results were 
numerically consistent for small cases and that the overall structure was logically sound, 
without being able to validate each proof step independently.

---

## Main Claims

For the modular Syracuse graph G_p (where odd n maps to 3n+1 mod 2^p and even n has two 
successors n/2 and n/2+2^{p-1}):

- **Diameter:** diam(G_p) = 2p − 1
- **Primitivity exponent:** exp(G_p) = 2p

The argument uses a correspondence with the binary De Bruijn graph B(2,p) via the 
Bernstein–Lagarias conjugacy, plus a local path-subdivision at odd vertices.

---

## Relation to existing work

Laarhoven & de Weger (2013) established the isomorphism between the modular binary Collatz 
graph C(p) and the De Bruijn graph B(2,p). **To my knowledge**, the exact metric properties 
of the associated Syracuse graph G_p (with the non-divided odd rule 3n+1) have not been 
previously determined. If these results are already known, please open an issue and I will 
update this page immediately.

---

## Files

- [`paper/syracuse_debruijn_draft.pdf`](paper/syracuse_debruijn_draft.pdf) — Full LaTeX draft
- (Optional) `src/verification_p3.py` — Numerical verification for p=3

---

## Call for feedback

If you are a mathematician working on Collatz dynamics, graph theory, or related fields:

- **Are these exact formulas known?** If yes, please share the reference.
- **Is the proof correct?** If you find a gap or error, please open an issue.
- **Is this worth formalizing?** If the results hold, I would welcome collaboration 
  with an expert co-author who could validate and publish a rigorous version.

No expectation of authorship is implied on my part. I am simply seeking to understand 
whether this direction is worth pursuing.

---

## License

This draft is released under CC BY 4.0. If you use these ideas in future work, 
a citation or acknowledgment of this source would be appreciated.