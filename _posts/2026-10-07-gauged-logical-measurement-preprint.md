---
layout: post
title: "实验室关于规范逻辑测量附加条件代价的预印本上线 arXiv"
title_en: "New Preprint on the Cost of Each Side Condition in a Gauged Logical Measurement Posted to arXiv"
date: 2026-10-07
tag: "科研进展"
tag_en: "Research"
permalink_en: "/en/news/gauged-logical-measurement-preprint.html"
excerpt_en: "The lab's new work is now on arXiv as a preprint (arXiv:2610.04306, submitted 3 October 2026): the four side conditions behind a gauged logical measurement's tolerance guarantee are not worth the same — the demand that the first and last rounds be perfect carries the whole temporal part."
body_en: |
  The lab's new work is now on arXiv as a preprint (arXiv:2610.04306, submitted 3 October 2026).

  **The cost of each side condition in a gauged logical measurement**

  A logical measurement reads out protected information, and the noise it survives sets how much a quantum computation can absorb. Gauging builds one from a graph on the measured qubits — one extra qubit on each edge — turning a global operator into local parity checks. Its tolerance splits in two: the distance of the code left behind, and the rounds a fault can hide in. Williamson and Yoder proved both components stay at or above the code's distance, but the guarantee bundles four side conditions, none of them priced. This work shows they are not worth the same.

  The condition that reads most like bookkeeping — that the first and last rounds be perfect — is the one that carries the temporal part: dropping it flattens the fault distance, the least weight of a fault that passes unseen and flips the readout, to one for every code and round count, in a model whose detectors compare adjacent rounds; the full protocol collapses on the instance measured. The expansion condition, that no small set of qubits be sealed off, does not decide the outcome: two paths on the same qubits, both outside the covered regime, give distances one and two. The round count is tight only where comparing rounds is the whole rule; the full protocol reaches the distance a round early.

  Both components are computed exactly on a gauged bivariate bicycle code and a Bacon–Shor measurement, inside a proof assistant. Threshold estimates consume such numbers; side conditions can be priced.

  Paper: [arXiv:2610.04306](https://arxiv.org/abs/2610.04306)
---

实验室的新工作已在 arXiv 上线，目前为预印本（arXiv:2610.04306，2026 年 10 月 3 日提交）。

**The cost of each side condition in a gauged logical measurement**

逻辑测量负责读出受保护的信息，它在噪声下存活的程度决定一台量子计算能吸收多少错误。规范构造（gauging）从待测量子比特上的一个图把它造出来——每条边配一个额外量子比特——把一个全局算子化为局域的奇偶校验。它的容错度分成两半：留下的码的距离，和一个故障能藏匿的轮数。Williamson 与 Yoder 证明了这两个分量都不低于码的距离，但保证打包依赖四条附加条件，此前没有一条被单独定价。这项工作表明它们的价值并不相等。

看起来最像记账的一条——要求第一轮与最后一轮测量完美——恰恰承载了时间分量：去掉它，故障距离（能不被察觉地通过并翻转读数的最小故障权重）在探测器比较相邻轮的模型下，对每个码、每个轮数都塌到 1；完整协议在所测的那个实例上整体坍塌。扩展性条件（不允许一小撮量子比特被封闭起来）则不决定结果：同样一些量子比特上的两条路径，都在定理覆盖范围之外，给出的距离一个是 1、一个是 2。轮数只在"比较轮就是全部规则"的地方是紧的；完整协议提前一轮就达到距离。

两个分量在一个规范化的双变量自行车码（bivariate bicycle code）与一次 Bacon–Shor 测量上被精确计算，全部在证明助手内完成。阈值估计正是以这类数为原料；附加条件是可以定价的。

论文：[arXiv:2610.04306](https://arxiv.org/abs/2610.04306)
