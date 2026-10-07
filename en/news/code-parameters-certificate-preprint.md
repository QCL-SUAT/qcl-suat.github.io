---
layout: post
lang: "en"
title: "New Preprint on Checkable Quantum Code Parameters Posted to arXiv"
date: 2026-10-06
tag: "Research"
permalink_zh: "/2026/10/06/code-parameters-certificate-preprint.html"
---
The lab's new work is now on arXiv as a preprint (arXiv:2610.03214, submitted 2 October 2026, now updated to v2).

**Quantum error-correcting code parameters, checkable by a certificate of provable size**

A code is described by three numbers: its physical qubits, its logical qubits, and the smallest error it cannot detect, counted in qubits. The first two are linear algebra; the third, the distance, is an optimum over an exponentially large set, read off a solver whose answer carries no certificate. Whether a code's parameters can be checked uniformly across codes, with a certificate of proved size, was open.

The paper moves the unit of work from the code to a certificate — a short object, either a list, a pairing or a symbolic instance — whose correctness the kernel of the Lean proof assistant decides by computation. The certificate's size is itself a theorem: its enumeration form lists the vectors of weight below the distance d, C(n, j) summed over j < d, a polynomial in the code's length n at fixed distance d; and no bound uniform over codes in both n and d is smaller. For product families the certificate is smaller still, the bound being proved once, symbolically. Deciding that a vector lies outside the row space of the check matrix, the set of sums of its rows, becomes one matrix-vector product and one inner product: on an eighteen-qubit toric code, a surface code closed into a torus, the whole-file check of that decision falls from 42 s to 9 s. Eleven code families and thirty-nine parameter sets follow, the widest at 1872 qubits.

The update (v2) settles the distances of two published code families in the paper. The bivariate bicycle code's [[144,12,12]], whose lower bound the previous version imported, is now a kernel assertion — the argument is transported from an independent formalization, this paper contributing the transport and the matrix identity. The affine-permutation codes printed at [[1152,580,≤12]] and [[2304,1156,≤14]] are settled at twelve and fourteen: the upper bound of [[1152,580]] is re-derived by a Lean certificate, and the remaining bounds rest on results outside Lean. The pipeline's specification step, which writes a code's Lean definition, still carries a preset width of twenty columns — the 36-qubit instance was written by hand. Nothing beyond the three standard axioms of Lean's logic is trusted. A distance becomes checkable rather than believed.

The work belongs to the same line as the lab's [QECCertificates library](/en/news/qeccertificates-open-source.html), open-sourced on 1 October: the certificate checker the paper rests on is the one formalized there.

Paper: [arXiv:2610.03214](https://arxiv.org/abs/2610.03214)
