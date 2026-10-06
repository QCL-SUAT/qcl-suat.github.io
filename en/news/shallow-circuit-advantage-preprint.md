---
layout: post
lang: "en"
title: "New Preprint on Correlations Deciding a Shallow-Circuit Advantage Posted to arXiv"
date: 2026-10-07
tag: "Research"
permalink_zh: "/2026/10/07/shallow-circuit-advantage-preprint.html"
---
The lab's new work is now on arXiv as a preprint (arXiv:2610.04666, submitted 3 October 2026).

**Correlations decide a shallow-circuit advantage**

Quantum computers are claimed to produce samples ordinary classical computers cannot reproduce. The sharpest such claim pits constant-depth quantum circuits, given one entangled state per run, against shallow classical circuits of few-input gates and limited randomness. No efficient test was known that certifies such a claim from classical samples alone. This work shows that what such a test must read is decided by the classical class's pattern of single-bit and pair correlations, not by a distance.

The test rests on one inequality: any machine producing the samples sits no further from the target than the fraction it mislabels plus the deviation of its string half — the bits beyond the label — from uniform. A collapse theorem, machine-checked in the Lean 4 proof assistant, confines that second term, one setting of the sampler's random input bits at a time. Four natural checks provably fail; a fifth, reading those same correlations, catches a far-from-target construction they cannot reach, and is exact on the class of few-input gates. The label test is proven, and sample-optimal in its own tolerance up to a logarithmic factor; the fifth check is sound, not only effective, on the bounded pinned-residue class of pairwise-uniform samplers.

On the experimental side, what binds an experiment is the 43-qubit entangled resource state at fidelity near 0.99, not the readout. Two named open problems remain; a positive answer to the first would extend the guarantee to the full class.

Paper: [arXiv:2610.04666](https://arxiv.org/abs/2610.04666)
