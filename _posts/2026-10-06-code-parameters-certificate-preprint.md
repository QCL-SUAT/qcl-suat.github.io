---
layout: post
title: "实验室关于量子纠错码参数可复核性的预印本上线 arXiv"
title_en: "New Preprint on Checkable Quantum Code Parameters Posted to arXiv"
date: 2026-10-06
tag: "科研进展"
tag_en: "Research"
permalink_en: "/en/news/code-parameters-certificate-preprint.html"
excerpt_en: "The lab's new work is now on arXiv as a preprint (arXiv:2610.03214, submitted 2 October 2026): a code's distance becomes checkable rather than believed, by certificates whose size is itself a theorem."
body_en: |
  The lab's new work is now on arXiv as a preprint (arXiv:2610.03214, submitted 2 October 2026).

  **Quantum code parameters, checkable by a certificate of provable size**

  A code is described by three numbers: its physical qubits, its logical qubits, and the smallest error it cannot detect, counted in qubits. The first two are linear algebra; the third, the distance, is an optimum over an exponentially large set, read off a solver whose answer carries no certificate. Whether a code's parameters can be checked uniformly across codes, with a certificate of proved size, was open.

  The paper moves the unit of work from the code to a certificate — a short object, either a list, a pairing or a symbolic instance — whose correctness the kernel of the Lean proof assistant decides by computation. The certificate's size is itself a theorem: its enumeration form lists the vectors of weight below the distance d, C(n, j) summed over j < d, a polynomial in the code's length n at fixed distance d; and no bound uniform over codes in both n and d is smaller. For product families the certificate is smaller still, the bound being proved once, symbolically. Deciding that a vector lies outside the row space of the check matrix, the set of sums of its rows, becomes one matrix-vector product and one inner product: on an eighteen-qubit toric code, a surface code closed into a torus, the whole-file check of that decision falls from 42 s to 9 s. Eleven code families and thirty-nine parameter sets follow, the widest at 1872 qubits.

  Nothing beyond the three standard axioms of Lean's logic is trusted, and the paper states two limits of scope: the generator that writes a code's checks stops at twenty qubits, and the lower bound for the 144-qubit code is imported rather than proved there. A distance becomes checkable rather than believed.

  The work belongs to the same line as the lab's [QECCertificates library](/en/news/qeccertificates-open-source.html), open-sourced on 1 October: the certificate checker the paper rests on is the one formalized there.

  Authors: Shuoming An (faculty), Fusheng Yang (Sun Yat-sen University).

  Paper: [arXiv:2610.03214](https://arxiv.org/abs/2610.03214)
---

实验室的新工作已在 arXiv 上线，目前为预印本（arXiv:2610.03214，2026 年 10 月 2 日提交）。

**Quantum code parameters, checkable by a certificate of provable size**

一个量子纠错码由三个数描述：物理量子比特数、逻辑量子比特数，以及它探测不到的最小错误，按量子比特计。前两个数属于线性代数；第三个是距离，它是在指数大的集合上取的最优值，读自一个不附带证书的求解器。码参数能否在码与码之间统一地复核，且复核所凭证书的规模有可证的界，此前是开放问题。

这项工作把工作单位从码移到证书：一个短对象，或为列表、或为配对、或为符号实例，其正确性由 Lean 证明助手的内核用计算判定。证书的大小本身是一条定理：枚举形式的证书列出权重低于距离 d 的全部向量，数量为 C(n, j) 对 j < d 的求和，在固定 d 下是码长 n 的多项式；论文同时证明，不存在同时在 n 与 d 上一致更小的界。对乘积族，证书可以更小——界只需符号地证明一次。判定一个向量落在校验矩阵的行空间之外（行空间即矩阵各行相加所能得到的一切向量），化为一次矩阵-向量乘与一次内积：在 18 个量子比特的环面码（闭合成环面的表面码）上，这一步的整文件检查从 42 秒降到 9 秒。论文覆盖十一个码族、三十九组参数集，最大到 1872 个量子比特。

除 Lean 逻辑的三条标准公理之外，论文不信任任何东西；它同时写明两条边界：生成器目前写到 20 个量子比特为止，144 比特码的下界是导入的、未在本文中证明。距离由此从被相信的对象，变成可复核的对象。

这项工作与实验室 10 月 1 日开源的 [QECCertificates 库](/2026/10/01/qeccertificates-open-source.html)同属一条工作线：复核所凭的证书检查器，正是库里形式化的那一个。

作者为安硕明（实验室教师）、Fusheng Yang（中山大学）。

论文：[arXiv:2610.03214](https://arxiv.org/abs/2610.03214)
