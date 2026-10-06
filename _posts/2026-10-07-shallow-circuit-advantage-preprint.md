---
layout: post
title: "实验室关于关联决定浅层线路优势的预印本上线 arXiv"
title_en: "New Preprint on Correlations Deciding a Shallow-Circuit Advantage Posted to arXiv"
date: 2026-10-07
tag: "科研进展"
tag_en: "Research"
permalink_en: "/en/news/shallow-circuit-advantage-preprint.html"
excerpt_en: "The lab's new work is now on arXiv as a preprint (arXiv:2610.04666, submitted 3 October 2026): what a test of shallow-circuit sampling advantage must read is decided by the classical class's pattern of single-bit and pair correlations, not by a distance."
body_en: |
  The lab's new work is now on arXiv as a preprint (arXiv:2610.04666, submitted 3 October 2026).

  **Correlations decide a shallow-circuit advantage**

  Quantum computers are claimed to produce samples ordinary classical computers cannot reproduce. The sharpest such claim pits constant-depth quantum circuits, given one entangled state per run, against shallow classical circuits of few-input gates and limited randomness. No efficient test was known that certifies such a claim from classical samples alone. This work shows that what such a test must read is decided by the classical class's pattern of single-bit and pair correlations, not by a distance.

  The test rests on one inequality: any machine producing the samples sits no further from the target than the fraction it mislabels plus the deviation of its string half — the bits beyond the label — from uniform. A collapse theorem, machine-checked in the Lean 4 proof assistant, confines that second term, one setting of the sampler's random input bits at a time. Four natural checks provably fail; a fifth, reading those same correlations, catches a far-from-target construction they cannot reach, and is exact on the class of few-input gates. The label test is proven, and sample-optimal in its own tolerance up to a logarithmic factor; the fifth check is sound, not only effective, on the bounded pinned-residue class of pairwise-uniform samplers.

  On the experimental side, what binds an experiment is the 43-qubit entangled resource state at fidelity near 0.99, not the readout. Two named open problems remain; a positive answer to the first would extend the guarantee to the full class.

  Paper: [arXiv:2610.04666](https://arxiv.org/abs/2610.04666)
---

实验室的新工作已在 arXiv 上线，目前为预印本（arXiv:2610.04666，2026 年 10 月 3 日提交）。

**Correlations decide a shallow-circuit advantage**

量子计算机被宣称能产生普通经典计算机无法复现的样本。这类断言里最尖锐的一版，让每次运行配备一个纠缠态的常数深度量子线路，与由少输入门和有限随机性组成的浅层经典线路对垒。此前不存在从经典样本出发、能认证这类优势的高效测试。这项工作证明：这样的测试必须读什么，由经典类别的单比特与双比特关联模式决定，而不是由某个距离决定。

测试立足一条不等式：任何产生样本的机器，离目标都不超过它错标的份额，加上它的"串半"——标签之外的比特——偏离均匀的程度。一条在 Lean 4 证明助手中机器检查的坍缩定理，按采样器随机输入位的每一种取值，逐个控制住第二项。四个自然的检查被证明必然失败；第五个——读同样的关联——能抓住它们够不着的远离目标的构造，并在少输入门类上做到精确。标签测试本身可证，且在自身容差内样本最优、至多差一个对数因子；第五个检查在"有界钉住余数类"——成对均匀、余项（串权重模素数）被少量种子钉住且种子共享有界的采样器——上不仅有效，而且可靠。

实验一侧，真正约束实验的是保真度约 0.99 的 43 比特纠缠资源态，而不是读出。论文留下两个命名的开放问题；对第一个的肯定回答将把保证扩展到完整的类。

论文：[arXiv:2610.04666](https://arxiv.org/abs/2610.04666)
