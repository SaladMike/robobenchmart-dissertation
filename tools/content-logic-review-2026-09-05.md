# 论文内容与逻辑审阅

审阅日期：2026-09-05。对象：`main.tex` 实际载入的摘要、六章正文、附录 A，以及当前 `build/main.pdf`（读取到 77 个物理页）。通读源文，重新计算表格派生数值，并查看场景图、资产图、Pareto 图、计时图、主结果表和附录表所在的完整 PDF 页面。未改动论文源文、图表或实验数据；未运行模型、模拟器或重新训练。

## 总体判断

这篇论文有明确的工程内容和基本成立的章节主线：零售任务需求 → 场景与数据系统 → 策略适配与测试 → 低成功率及协议局限 → 后续可检验问题。按系统与基准构建论文评价，它已有实质内容；按已经完成的 VLA 泛化比较研究评价，证据仍不足。

最关键的薄弱处是：工程系统的有效性主要由实现描述和少量运行记录支撑，而策略学习和迁移的核心问题尚未得到有区分力的实验回答。承认局限是必要的，但不能替代对核心贡献的正面验证。

摘要与结论已经基本一致，均没有把近零成功率解释为整个 VLA 架构家族的能力上限。第 2 章对相邻工作的定位也比较克制。当前不需要推翻六章结构，优先修正以下局部逻辑和证据问题。

## 1. 高优先级：把未知的训练充分性写成了已知的主要原因

位置：[chapter-1.tex:50](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-1/chapter-1.tex:50)、[chapter-2.tex:87](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-2/chapter-2.tex:87)、[chapter-6.tex:28](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-6/chapter-6.tex:28)。

原句包括：

- “That last item does most of the work.”
- “A few hours on one card is not a fair test of a three-billion-parameter policy”
- “one of them swallows the rest”
- “and so does how far each was trained from convergence”
- “Training sufficiency remains the binding limitation.”

问题：本文没有验证收敛程度，更没有隔离算力、数据、优化及控制接口的影响。因此可以确认“无法判断训练是否充分”，不能确认“预算是主要原因”，也不能确认模型距离收敛的程度相互不同。第 6 章第 16 行明确说这些因素纠缠，以上句子却给预算赋予了未经验证的因果地位。单卡和若干小时本身也不是判定训练不充分的标准。

建议将第 1 章相关论断替换为：

> Training sufficiency was not established. The observed failure rates cannot be attributed separately to compute, the demonstration corpus, optimisation, or the executed control protocol.

第 2 章相关收敛断言改为：

> Architecture, pretraining and adaptation method vary across the four pipelines, while the degree of convergence remains unknown for each.

第 6 章改为：

> The absence of evidence about training sufficiency is a major limitation on interpretation.

## 2. 高优先级：失败标签的占比不能直接当作阶段到达率

位置：[chapter-5.tex:170](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:170)、[chapter-5.tex:172](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:172)。

原句：“The $\pi$ models more often reach interaction”；“A model that reaches and interacts more often also creates more opportunities to disturb neighbouring items.”

问题：表 5.2 的分母是被选中标注的失败，既不是全部评测，也不是到达抓取阶段的全部回合。第 4 章第 96 行又说明采样框和 episode 标识未保留。任务、条件的采样权重不同，就可能改变总体占比；earliest-primary 标签也不能完整恢复各阶段的到达事件。因此不能由这些占比断言模型更常到达接触阶段，或已经证明接触机会与扰动物品之间的权衡。

建议替换为：

> The retained annotation aggregates place a larger share of the two $\pi$ pipelines' sampled failures at interaction or later stages. Because the realised sampling frame and episode-level stage events are unavailable, these shares do not establish a higher probability of reaching contact.

> The 7\% displacement share for $\pi_{0.5}$ motivates a check of collateral motion conditional on contact; it does not establish a trade-off between interaction frequency and disturbance.

## 3. 高优先级：把“基线必须先成功”设成所有诊断实验的前提，逻辑过强

位置：[chapter-5.tex:234](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:234)、[chapter-5.tex:236](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:236)、[chapter-6.tex:32](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-6/chapter-6.tex:32)。

原句：“no other ablation in this section can be read”；“there is currently no performance for a condition to change”；“Everything else in this section depends on establishing that training baseline first.”

问题：零基线限制向下退化的可观察幅度，却不妨碍检测修正接口、改变执行步长或加入恢复数据后的向上改善。第 5 章第 236 行又要求两项实验同时进行，与“其他一切均须等待”冲突。若接口或动作执行存在问题，单纯延长训练也未必是适当的第一步。

建议替换为：

> A reliable in-domain baseline is needed before interpreting downward transfer losses. Interface checks and controlled interventions that may improve a floor-limited baseline can proceed before or alongside convergence-checked adaptation.

此外，第 236 行不能只凭“grasp 标签变少”就把“大量接触失败”归因于开环执行：标签也可能转移到更早的阶段。建议替换末句为：

> A matched horizon sweep can test whether shorter open-loop intervals improve completion and grasp success conditional on reaching a valid pre-grasp state. A reduction in the grasp-label share alone would not establish that effect.

## 4. 高优先级：系统贡献的验证还不够集中，存在一个错误的必要性论证

位置：[chapter-3.tex:158](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-3/chapter-3.tex:158)。

原句：“A shelf-only benchmark ... would remove the mobile-base component, however, and it would keep camera--fixture geometry almost constant.”

问题：孤立货架也可以配移动底盘，并随机化起点、视角和局部接近路径。全文又明确所有任务从正确货架前方开始，没有跨店导航。因此这句话不能证明“完整店面是测试移动操作所必需的”，也不能证明当前完整店面比局部货架有已测得的收益。

建议替换为：

> A shelf-only environment could retain local mobile-base positioning and viewpoint variation. Full-store generation additionally supports broader scene context and future navigation tasks, although its incremental effect on the reported policy outcomes was not isolated here.

证据层面的建议：把场景构建成功率、有效种子数、独特布局数、几何通路检查、演示尝试数与接受率集中成一张验证表。已有记录能支持多少就报告多少，不能补造数值。对张量场的必要性，最直接的是在相同碰撞与通道规则下比较“使用方向门控”和“不使用门控”；当前定性比较表不能替代这一实验。

## 5. 中优先级：LoRA 表头与数值的含义冲突

位置：[appendix-b.tex:11](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/c-back-matter/appendix-b.tex:11)。

原文表头：“LoRA rank / $\alpha$”；两个 $\pi$ 模型的值为“16 / 32”。但表注和第 4 章第 48 行说这两个数分别为 backbone 与 action expert 的 rank。

问题：同一列对 SmolVLA 表示 rank/alpha，对两个 $\pi$ 模型表示两个模块的 rank。读者会自然误读为 $r=16,\alpha=32$。当前 CSV 则分别记录两个模块的 rank 和 alpha 都为 16、32，但它是本地配置汇总，不是训练日志。

建议改为独立列或逐模块条目：“Module”、“LoRA rank $r$”、“LoRA $\alpha$”。如果实际配置文件能够确认 CSV，则分别填 VLM 的 $r=16,\alpha=16$，action expert 的 $r=32,\alpha=32$；无法确认的字段写 not recorded。

可替换的说明句：

> LoRA rank and scaling are reported separately for each adapted module; the backbone and action-expert ranks must not be read as a rank–alpha pair.

## 6. 中优先级：Pareto 前沿与归一化解释存在可复算的问题

位置：[chapter-3.tex:110](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-3/chapter-3.tex:110)、[chapter-3.tex:117](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-3/chapter-3.tex:117)、[pareto.json:176](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/tools/data/pareto.json:176)。

原句：“eleven are non-dominated”；“retaining 29\% of the source triangles”。

复算结果：在保存的 43 个坐标上，以两个目标都越小越好进行非支配筛选，得到 10 个前沿点。文件将 `(0, 1)` 与 `(0, 0.9929)` 同时列入前沿，但前者被后者支配。若未舍入原始距离能够区分这两个点，应保留那份精度并据此重新计算，不能直接沿用当前列表。

另一个问题：图轴叫 normalised triangle count，正文却解释成原始三角形数的百分比。没有给出归一化公式，不能确认 0.29 就等于原始面数的 29%。归一化值中出现多个 0，也说明必须交代缩放方法。`best` 中的 `(0.122,0.287)` 与候选表的 `(0.122,0.2857)` 也不完全相同，需要从同一候选记录导出。

在无法恢复原始尺度时，建议使用：

> The selected candidate has normalised coordinates approximately (0.12, 0.29). These coordinates should not be interpreted as fractions of the source mesh without the normalisation formula.

按当前保留坐标修正图及前沿列表后，图注可写：

> Forty-three candidates are retained; ten are non-dominated under minimisation of the two stored coordinates.

## 7. 中优先级：低成功率并不能证明满货架是更适合实验的选择

位置：[chapter-3.tex:125](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-3/chapter-3.tex:125)、[chapter-3.tex:203](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-3/chapter-3.tex:203)。

原句：“Fully packed shelves were ... the right choice ... since the evaluated policies already perform poorly without stock variation.”

问题：固定库存状态可以减少一种分布变化；但满货架可能增加遮挡、碰撞和抓取难度。低成功率不能推出满货架比稀疏货架更适宜，也不能证明库存变化只会使任务更难。

建议两处统一替换为：

> Fully stocked shelves hold occupancy fixed in the reported study. This controls one source of variation, but no ablation establishes whether full stocking helps or hinders policy success relative to sparser arrangements.

## 8. 中优先级：门任务没有商品名，不等于没有 grounding

位置：[chapter-5.tex:246](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:246)。

原句：“Their instruction never names a product, which removes grounding from the picture”。

冲突：第 3 章第 131–133 行说明 showcase 有指定门，任务还要确定正确 fixture；附录第 89 行将错误 product、fixture 或 instance 都定义为 target 错误。

建议替换为：

> Door tasks remove product-identity grounding, but policies must still identify the instructed fixture or door and localise its handle.

## 9. 中优先级：复合任务的零分缺少独立的试验分母和组合清单

位置：[chapter-4.tex:71](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-4/chapter-4.tex:71)、[chapter-5.tex:16](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:16)、[chapter-5.tex:135](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:135)。

现有描述明确列出了原子任务的 200/300 次聚合分母，却没有同样明确交代 Pick 3 的三商品组合、Fridge sequence 的任务配置，以及每个复合任务条件的实际总回合数。不能自动把原子任务的 triplet 定义套到三商品序列上。

这是记录完整性问题，不是“零结果一定错误”。建议新增复合任务协议表，列出商品/fixture 组合、每组试验数、总数、单阶段与整段终止条件。若原始记录无法恢复，应明确写：

> No completed composite episode is reported in the retained aggregates. The realised configuration counts and total trial denominators for these cells could not be reconstructed, so the zeros are reported without interval estimates.

仅在确认无法恢复后使用这句话，不能把本次未找到等同于作者从未保存。

## 10. 中优先级：附录仍声称下游事件已保留在 rollout 记录中

位置：[appendix-b.tex:64](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/c-back-matter/appendix-b.tex:64)。

原句：“Later consequences are retained in the rollout record but are not counted again.”

问题：第 4 章第 96 行、第 5 章第 146 行与结论强调 episode-level 记录无法重聚合。上述句子可能指当时的视频而不是目前的归档，但文中没有区分，读者会误以为现有材料支持下游事件追溯。

建议替换为：

> Later consequences may be visible during annotation, but only the earliest primary category contributes to the reported aggregates. Episode-level records sufficient to reconstruct those downstream events are not available in the archived bundle.

## 11. 次优先级：计时图与正文对“停止测试”与“容量上限”的表述不统一

位置：[chapter-3.tex:205](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-3/chapter-3.tex:205)、[chapter-5.tex:64](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:64)、[chapter-5.tex:69](/Users/xumaokuan/Downloads/robobenchmart-dissertation-source/chapter-5/chapter-5.tex:69)。

正文第 5 章第 64 行正确限定为 original 系列没有继续测量；第 3 章和图注却说超过 4 个单元便 impractical。保留的计时点没有超过 4 的 original 测量，也没有定义 impractical 的内存或耗时阈值，因此这只能作为当时的定性观察，不能当作已测容量上限。

建议图注相关句替换为：

> The recorded original-mesh series ends at four units; the simplified-mesh series contains measurements up to 118 units. These measurements do not establish a maximum supported scene size for either configuration.

## 已核对成立的内容

- 12 × 248 = 2,976，演示总数的内部算术一致；1,401,169 transitions 在主要章节一致。该核对不等于验证原始 HDF5。
- 附录 Seeds/Pose/Layout 共 144 个详细单元，111 个非零，范围 0–9，均值约 1.5417%，正文写 1.5 与舍入一致。
- Pose/Layout 主表按详细表等样本聚合并 round-half-up 后一致。
- 20 个 Pose→Layout 变化中，10 个为 0，9 个绝对变化为 1/3 至 2/3 个百分点，剩余 Octo Close 为 +2.5 个百分点。
- 四行失败占比均合计 100%；这只能验证表格算术，不能验证 2,906 条标签的真实性或抽样构成。
- 主表将无法恢复计数的 pi0 Floor Pairing 标为 NR，比把历史舍入百分比反推成功次数妥当。
- 第 5 章第 112 行已经正确说明：Wilson 区间重叠不能作为比较显著性的规则。`tools/review-brief.md` 中“区间重叠所以比较不成立”和“15 个变化为零”的描述已过时，不应据此改坏当前正文。
- 文献抽查：[Sari Sandbox 原文](https://arxiv.org/abs/2508.00400)支持三种店面和 250+ 商品的介绍；[MarketGen 原文](https://arxiv.org/abs/2511.21161)支持 1100+ 商品、两类任务和 sim-to-real 介绍；[SmolVLA 原文 §4.3](https://arxiv.org/html/2506.01844v1)明确写主要模型为 450M 参数，因此不能仅凭其他发布名称把论文的 450M 判错。这些来源也不能证明本文实际使用了哪个 checkpoint。

## 章节评价与修改顺序

| 部分 | 评价 | 最值得处理的事情 |
|---|---|---|
| 摘要 | 与结论基本一致，证据范围清楚 | 保持固定步数实验的定位 |
| 第 1 章 | 场景需求、RQ 与贡献能串起来 | 清除预算主因断言，避免超出局部移动操作范围 |
| 第 2 章 | 文献脉络合理，已讨论最邻近系统 | 修正未经测量的收敛程度断言 |
| 第 3 章 | 工程内容最充分，也是论文主要支撑 | 更集中地验证系统；修正完整店面的必要性论证、满货架论证和 Pareto 数据 |
| 第 4 章 | 条件、接口、成功判据交代较细 | 补足复合任务分母、控制时间尺度和实际配置记录 |
| 第 5 章 | 能区分观察值与泛化结论，但局部推理不一致 | 修正失败占比解释和消融优先级；保留可复算的数字 |
| 第 6 章 | 总结与摘要基本闭合 | 将后续工作改为可并行的验证/诊断与后续迁移评测 |
| 附录 | 详细结果有用 | 拆清 LoRA 参数语义，统一记录可用性的说法 |

优先级：先修确定的技术错误和过强推理，再整理系统验证证据；若能补实验，先确认演示能通过实际控制接口回放、动作归一化与时序正确，并进行小样本拟合/训练曲线检查及匹配种子的执行步长对照。只有在基线达到可测水平后，才能有力解释向下的迁移损失。

本次意见是内容与论证审阅，不是对原始实验的独立复现，也不是学位通过与否的判断。
