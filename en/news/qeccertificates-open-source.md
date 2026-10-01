---
layout: post
lang: "en"
title: "QCL Open-Sources QECCertificates, a Lean 4 Library for Quantum Error Correction"
date: 2026-10-01
tag: "Open Source"
permalink_zh: "/2026/10/01/qeccertificates-open-source.html"
---
The lab has open-sourced **QECCertificates** on GitHub: a Lean 4 library that provides machine-checkable certificates for the code parameters and fault distances of quantum error correction codes.

**Why this exists**

Code parameters are found by search, and a search ends in a solver's verdict. The public schema behind the qLDPC Challenge records what that costs: an uncertified distance is only reported as an upper bound — for a non-CSS code because the Pauli-weight certifier "is not available yet", for a circuit-level distance because the exact tier "is deferred future work". There are two ways out: trust the tool that printed the number, or make the number come with something a third party can check. QECCertificates takes the second way: the encoding of the search problem, the soundness of the certificate checker, and the composition of the two are theorems, and every load-bearing declaration is printed in an audit region so that a reader can see which axioms it rests on.

**What is in the library**

- **GF(2) linear algebra**: trusted row reduction, kernel bases, rank certificates, dual witnesses, exact-distance bracketing, hypergraph and lifted products, the Künneth formulas;
- **Pauli**: the translation between the operator-tree and symplectic representations;
- **The certificate framework**: a kernel-checked LRAT/RUP checker with its soundness theorem, encoding faithfulness in both directions — a model of the CNF *is* a light logical operator — and symmetry breaking that preserves unsatisfiability;
- **Codes**: stabilizer, CSS and subsystem codes; gauging and measurement-protocol representations; the shared instance families (Bacon–Shor, BB, HGP, lifted product).

**What is guaranteed**

57 modules in all, with the audit region covering every non-private theorem and lemma in the package — no un-audited corner. Zero `sorry`, zero custom axioms, zero `native_decide`; no audited declaration depends on an axiom outside the three standard ones (propext, Classical.choice, Quot.sound). The certificate checker shares no code with any solver: an UNSAT verdict is re-derived from the formula and the proof file alone.

The project is released under Apache-2.0 and archived on Zenodo for academic citation (DOI: [10.5281/zenodo.23056679](https://doi.org/10.5281/zenodo.23056679)).

Repository: [github.com/QCL-SUAT/QECCertificates](https://github.com/QCL-SUAT/QECCertificates)
