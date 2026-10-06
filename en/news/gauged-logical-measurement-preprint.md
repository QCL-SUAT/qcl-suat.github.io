---
layout: post
lang: "en"
title: "New Preprint on the Cost of Each Side Condition in a Gauged Logical Measurement Posted to arXiv"
date: 2026-10-07
tag: "Research"
permalink_zh: "/2026/10/07/gauged-logical-measurement-preprint.html"
---
The lab's new work is now on arXiv as a preprint (arXiv:2610.04306, submitted 3 October 2026).

**The cost of each side condition in a gauged logical measurement**

A logical measurement reads out protected information, and the noise it survives sets how much a quantum computation can absorb. Gauging builds one from a graph on the measured qubits — one extra qubit on each edge — turning a global operator into local parity checks. Its tolerance splits in two: the distance of the code left behind, and the rounds a fault can hide in. Williamson and Yoder proved both components stay at or above the code's distance, but the guarantee bundles four side conditions, none of them priced. This work shows they are not worth the same.

The condition that reads most like bookkeeping — that the first and last rounds be perfect — is the one that carries the temporal part: dropping it flattens the fault distance, the least weight of a fault that passes unseen and flips the readout, to one for every code and round count, in a model whose detectors compare adjacent rounds; the full protocol collapses on the instance measured. The expansion condition, that no small set of qubits be sealed off, does not decide the outcome: two paths on the same qubits, both outside the covered regime, give distances one and two. The round count is tight only where comparing rounds is the whole rule; the full protocol reaches the distance a round early.

Both components are computed exactly on a gauged bivariate bicycle code and a Bacon–Shor measurement, inside a proof assistant. Threshold estimates consume such numbers; side conditions can be priced.

Paper: [arXiv:2610.04306](https://arxiv.org/abs/2610.04306)
