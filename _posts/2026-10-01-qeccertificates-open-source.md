---
layout: post
title: "实验室开源量子纠错证书库 QECCertificates"
title_en: "QCL Open-Sources QECCertificates, a Lean 4 Library for Quantum Error Correction"
date: 2026-10-01
tag: "开源"
tag_en: "Open Source"
permalink_en: "/en/news/qeccertificates-open-source.html"
excerpt_en: "QCL has open-sourced QECCertificates, a Lean 4 library that provides machine-checkable certificates for the code parameters and fault distances of quantum error correction codes."
body_en: |
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
---

实验室在 GitHub 开源了量子纠错证书库 **QECCertificates**：一个用 Lean 4 写成的形式化库，为量子纠错码的码参数与故障距离提供机器可复核的证书。

**为什么做这件事**

码参数是搜出来的，而一次搜索以某个求解器的判决收尾。公开的 qLDPC Challenge schema 把这件事的代价写在了自己的文档里：未经认证的距离只报成上界——非 CSS 码是因为 Pauli 重量认证器尚未提供，线路级距离是因为精确档列为未来的工作。出路有两条：相信打印出这个数的那个工具，或者让这个数自带一样第三方能检查的东西。QECCertificates 走第二条路：搜索问题的编码、证书检查器的可靠性，以及两者的复合，都是定理；每条承重声明都印在审计区里，读者能看到它依赖哪些公理。

**库里有什么**

- **GF(2) 线性代数**：可信行消元、核基、秩证书、对偶见证、精确距离的夹逼、超图积与提升乘积、Künneth 公式；
- **Pauli 层**：算符树与辛表示之间的翻译；
- **证书框架**：内核复核的 LRAT/RUP 检查器及其可靠性定理，双向的编码忠实性——CNF 的一个模型就是一个轻逻辑算符——以及保持不可满足性的对称性破缺；
- **码论层**：稳定子码、CSS 码与子系统码，gauging 与测量协议的表示，以及 Bacon–Shor、BB、HGP、提升乘积等共享实例族。

**它保证了什么**

全库共 57 个模块，审计区覆盖包里每一条非私有定理与引理——没有审计不到的角落。零 `sorry`、零自定义公理、零 `native_decide`；受审计声明不依赖 propext、Classical.choice 与 Quot.sound 之外的任何公理。证书检查器与任何求解器不共享一行代码——UNSAT 判决只由公式与证明文件重新推出。

项目以 Apache-2.0 许可发布，已归档到 Zenodo 供学术引用（DOI：[10.5281/zenodo.23056679](https://doi.org/10.5281/zenodo.23056679)）。

仓库地址：[github.com/QCL-SUAT/QECCertificates](https://github.com/QCL-SUAT/QECCertificates)
