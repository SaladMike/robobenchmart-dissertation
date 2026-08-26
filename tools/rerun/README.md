# 重跑结果填写模板

每个 CSV 里已经填好**当前论文里的数值**，直接覆盖成新结果即可。
没有重跑的行**留着原值不要动**，我会据此判断哪些是新数据、哪些沿用旧数据。

## 填写顺序（按依赖关系）

| 文件 | 对应 | 是否必填 |
|---|---|---|
| `05_training_config.csv` | chapter-4:47, appendix-b:9 | **先填这个** —— 它决定其余结果算哪一组 |
| `01_main_results.csv` | tab:main-results | 必填 |
| `02_per_item.csv` | tab:per-item（含 Seeds 条件） | 必填 |
| `03_pairing_per_product.csv` | appendix-b:87 | 必填 |
| `04_failure_share.csv` | tab:failure-share | 必填，每行合计须为 100 |
| `06_timings.csv` | fig:mesh-performance | 硬件相关 |
| `07_throughput.csv` | chapter-5:79 | 原始数据已丢，全空待填 |
| `08_scalars.csv` | 正文散落数字 | 只填变化的 |

## 不用填的东西

**派生数字我来算**，不要手工填：

- §5.5 所有 Pose→Layout 差值 —— 从 `01` 算
- §5.3 Seeds→Pose 的对比数字 —— 从 `02` 算
- §5.7 正文引用的失败占比 —— 从 `04` 算
- §5.4 原子任务逐项分析里的数值 —— 从 `01` 算
- 第六章结论、摘要里的数字 —— 从上面各表算

**这些结果与训练方法无关，完全不用重跑**：
fig:store-generation、tab:layout-generation-ab、fig:asset-library、
fig:asset-pareto、fig:anchor-sequence、tab:retail-benchmark-comparison。
演示语料本身（2,976 episodes / 1,401,169 transitions）也不变。

## 几个约定

- 成功率一律填**百分数整数**，和现在的表一致（如 `55` 不是 `0.55`）
- `01` 里门任务的 Pairing 是 `--`（该条件不存在），**不要改成 0**
- `05` 的 `reran` 列填 `yes` / `no`。若出现部分重跑，
  chapter-4 的效度节必须说明两组不可直接比较
- `06` 里原始网格系列当初止步于 4 单元，4090 上能跑到几个就填到几个

## 填完之后

告诉我一声，我会：

1. 用新数值替换 5 张表和相关图的数据文件
2. 重算并替换正文里所有派生数字
3. 更新 chapter-4 训练配置段和 appendix-b 配置表（含 LoRA 超参）
4. 重新核对 tab:verification 的七条偏差对新运行是否仍然成立
5. 重新编译并检查前后一致性
