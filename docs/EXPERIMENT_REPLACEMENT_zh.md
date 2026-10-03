# 旧论文实验与本次两模型评测：逐项对照及正文替换清单

核对时间：2026-10-03 UTC。本文供修改论文正文前审阅；**本次仅新增对照资料，尚未把旧实验数值改进 LaTeX 正文**。数据来自 [Octo 完整配置 CSV](../data/reproduced-2026-10-02/octo_success_rates.csv) 和 [π₀.₅ 完整配置 CSV](../data/reproduced-2026-10-02/pi05_success_rates.csv)。[42 配置并排 CSV](../data/reproduced-2026-10-02/two_model_42_config_comparison.csv)、[任务汇总 CSV](../data/reproduced-2026-10-02/two_model_family_aggregate.csv)、[SHA-256](../data/reproduced-2026-10-02/SHA256SUMS.txt) 可直接用于制表。原始 π₀.₅ 日志、逐回合成败索引、视频与产物清单见[项目仓库的完整评测记录](https://github.com/SaladMike/RoboBenchMart_dissertation/tree/main/results/pi05-2026-10-02)。

## 一、证据范围与最重要的变化

| 维度 | 当前论文正文/旧实验 | 本次实际可核对的实验 | 正文应如何改 |
| --- | --- | --- | --- |
| 模型 | Octo、SmolVLA、π₀、π₀.₅，四模型本地适配 | 仅 Octo、π₀.₅ 两个**已微调公开权重**完成原子任务评测；本机没有这四模型的训练记录 | 改为两模型检查点评测；删除把本轮称为四模型重训的叙述 |
| 配置与回合 | 主表 Pose/Layout/Pairing；每 task–item–fixture 100 次 | `bash/eval_model.sh` 42 配置，Seeds/Pose/Layout 各 12、Pairing 6；每配置 30 次；每模型 1,260 回合 | 分母逐格改为 90/60，不再沿用 300/200；加入 Seeds |
| 成功率 | 旧表是 0–7% 等四模型数值 | Octo 4/1,260；π₀.₅ 39/1,260；详见下文分任务表 | 旧成功率、图和论断全部从新 CSV 重新计算 |
| 复合任务 | Pick 3 和 Fridge sequence 两列均为 0 | 本轮**未运行复合任务评测** | 删除这两列，正文不写“本轮复合成功率为 0” |
| 失败标注 | 2,906 失败 episode、11 类原因百分比 | 本轮没有重新人工标注；π₀.₅ 的 1,221 次失败不是已标注样本 | 删除旧失败分布和由其推出的因果说法；可写成待做分析 |
| 训练数据 | 声称 2,976 成功演示、1,401,169 transitions，并据此训练四模型 | 本地有 12 个演示索引 JSON，各 248 条 episode 元数据，合计 2,976 **索引项**；没有对应训练 HDF5 轨迹或本地训练记录；本次使用已有检查点 | 将“本地用于重训的完整语料”改为“公开检查点的来源背景/项目现有元数据”，不要用索引项证明可重新训练 |
| 场景/资源 | 把完整 benchmark 或 50 GB 资源作为隐含前提 | 已核验的评测场景下载为 466 文件、87,643,138 字节，修订 `3dabfaaf9bdf2ba886264a1160dab68ac7043d00`；另依赖 `assets/`。Octo 7 文件 833,438,151 字节；π₀.₅ 22 文件 12,430,591,218 字节 | 准确区分本次评测所需资源与完整训练语料/完整资产包；不写“本次下载了 50 GB” |
| 可审计性 | 旧主表/失败标签没有完整 episode 记录 | 两模型各 42 行汇总 CSV；π₀.₅ 有 42 份配置日志和 1,260 MP4。Octo 公开提交目前仅汇总 CSV，原始视频未随之发布 | 列明两模型证据深度不同，避免称逐回合严格配对 |

这里的 4/1,260 与 39/1,260 只作为文件完整性核对数，**不能**把异质任务直接平均成用于模型排名的统一总分。下面所有分任务数字均从本轮 CSV 整数成功次数求和后除以整数回合数，百分比保留两位小数。`—` 表示不存在的门任务 Pairing，不是 0。

## 二、旧论文结果与本轮结果并列

旧论文 `chapter-5/chapter-5.tex` 主表如下，单位为旧稿声称的成功率百分数。这里照录旧稿以标出需要替换的位置，**不能与新表视为同一实验的增减**：旧表每配置 100 次，模型、训练和证据来源也不同。旧稿 π₀ 的 Floor–Pairing 单元格标为 `NR†`，因为其原始计数未保留。

| 旧模型 | 条件 | Basket % | Floor % | Board % | Open % | Close % | Pick 3 % | Fridge seq. % |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Octo | Pose | 1 | 1 | 2 | 3 | 4 | 0 | 0 |
| Octo | Layout | 2 | 1 | 1 | 2 | 7 | 0 | 0 |
| Octo | Pairing | 0 | 0 | 0 | -- | -- | 0 | 0 |
| SmolVLA | Pose | 0 | 0 | 0 | 1 | 2 | 0 | 0 |
| SmolVLA | Layout | 0 | 0 | 0 | 1 | 2 | 0 | 0 |
| SmolVLA | Pairing | 0 | 0 | 0 | -- | -- | 0 | 0 |
| pi0 | Pose | 1 | 1 | 1 | 2 | 2 | 0 | 0 |
| pi0 | Layout | 1 | 1 | 1 | 2 | 2 | 0 | 0 |
| pi0 | Pairing | 0 | NR† | 0 | -- | -- | 0 | 0 |
| pi05 | Pose | 1 | 1 | 1 | 2 | 2 | 0 | 0 |
| pi05 | Layout | 1 | 1 | 1 | 1 | 2 | 0 | 0 |
| pi05 | Pairing | 1 | 1 | 3 | -- | -- | 0 | 0 |

本次真实评测结果，格式为“成功次数/评测次数（成功率）”：

| 模型 | 条件 | Basket | Floor | Board | Open | Close |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Octo | Seeds | 0/90 (0.00%) | 0/60 (0.00%) | 0/90 (0.00%) | 0/60 (0.00%) | 1/60 (1.67%) |
| Octo | Pose | 0/90 (0.00%) | 0/60 (0.00%) | 0/90 (0.00%) | 0/60 (0.00%) | 0/60 (0.00%) |
| Octo | Layout | 0/90 (0.00%) | 0/60 (0.00%) | 0/90 (0.00%) | 0/60 (0.00%) | 3/60 (5.00%) |
| Octo | Pairing | 0/60 (0.00%) | 0/60 (0.00%) | 0/60 (0.00%) | — | — |
| pi05 | Seeds | 0/90 (0.00%) | 0/60 (0.00%) | 0/90 (0.00%) | 0/60 (0.00%) | 15/60 (25.00%) |
| pi05 | Pose | 0/90 (0.00%) | 0/60 (0.00%) | 0/90 (0.00%) | 1/60 (1.67%) | 10/60 (16.67%) |
| pi05 | Layout | 0/90 (0.00%) | 0/60 (0.00%) | 0/90 (0.00%) | 1/60 (1.67%) | 12/60 (20.00%) |
| pi05 | Pairing | 0/60 (0.00%) | 0/60 (0.00%) | 0/60 (0.00%) | — | — |

π₀.₅ 成功全部来自开/关门：Seeds 15/360、Pose 11/360、Layout 13/360、Pairing 0/180。Octo 分别是 1/360、0/360、3/360、0/180。两个模型的抓放三类任务在四种条件下均为 0。π₀.₅ 的 Close 在 Seeds/Pose/Layout 分别为 15/60、10/60、12/60；Octo 则为 1/60、0/60、3/60。π₀.₅ 的 Open 在 Pose/Layout 各 1/60。门任务的 Layout 复用训练场景，因此不能解读为新的几何布局迁移。由于多个配置为 0/30，条件差值也容易受成功率地板效应影响。

### 42 个配置逐项对照

| 编号 | 条件 | 任务 | Octo 成功/30 | π₀.₅ 成功/30 |
| ---: | --- | --- | ---: | ---: |
| 1 | Seeds | board_duff_train | 0/30 | 0/30 |
| 2 | Seeds | board_nestle_train | 0/30 | 0/30 |
| 3 | Seeds | board_vanish_train | 0/30 | 0/30 |
| 4 | Seeds | open_fridge_train | 0/30 | 0/30 |
| 5 | Seeds | close_fridge_train | 0/30 | 8/30 |
| 6 | Seeds | open_showcase_train | 0/30 | 0/30 |
| 7 | Seeds | close_showcase_train | 1/30 | 7/30 |
| 8 | Seeds | floor_beans_train | 0/30 | 0/30 |
| 9 | Seeds | floor_slam_train | 0/30 | 0/30 |
| 10 | Seeds | basket_fanta_train | 0/30 | 0/30 |
| 11 | Seeds | basket_nivea_train | 0/30 | 0/30 |
| 12 | Seeds | basket_stars_train | 0/30 | 0/30 |
| 13 | Pose | board_duff_robo | 0/30 | 0/30 |
| 14 | Pose | board_nestle_robo | 0/30 | 0/30 |
| 15 | Pose | board_vanish_robo | 0/30 | 0/30 |
| 16 | Pose | open_fridge_robo | 0/30 | 0/30 |
| 17 | Pose | close_fridge_robo | 0/30 | 7/30 |
| 18 | Pose | open_showcase_robo | 0/30 | 1/30 |
| 19 | Pose | close_showcase_robo | 0/30 | 3/30 |
| 20 | Pose | floor_beans_robo | 0/30 | 0/30 |
| 21 | Pose | floor_slam_robo | 0/30 | 0/30 |
| 22 | Pose | basket_fanta_robo | 0/30 | 0/30 |
| 23 | Pose | basket_nivea_robo | 0/30 | 0/30 |
| 24 | Pose | basket_stars_robo | 0/30 | 0/30 |
| 25 | Layout | board_duff_uns | 0/30 | 0/30 |
| 26 | Layout | board_nestle_uns | 0/30 | 0/30 |
| 27 | Layout | board_vanish_uns | 0/30 | 0/30 |
| 28 | Layout | open_fridge_uns | 0/30 | 1/30 |
| 29 | Layout | close_fridge_uns | 0/30 | 6/30 |
| 30 | Layout | open_showcase_uns | 0/30 | 0/30 |
| 31 | Layout | close_showcase_uns | 3/30 | 6/30 |
| 32 | Layout | floor_beans_uns | 0/30 | 0/30 |
| 33 | Layout | floor_slam_uns | 0/30 | 0/30 |
| 34 | Layout | basket_fanta_uns | 0/30 | 0/30 |
| 35 | Layout | basket_nivea_uns | 0/30 | 0/30 |
| 36 | Layout | basket_stars_uns | 0/30 | 0/30 |
| 37 | Pairing | board_nivea_ood | 0/30 | 0/30 |
| 38 | Pairing | board_fanta_ood | 0/30 | 0/30 |
| 39 | Pairing | floor_fanta_ood | 0/30 | 0/30 |
| 40 | Pairing | floor_duff_ood | 0/30 | 0/30 |
| 41 | Pairing | basket_nestle_ood | 0/30 | 0/30 |
| 42 | Pairing | basket_slam_ood | 0/30 | 0/30 |

任务名后缀 `train → Seeds`、`robo → Pose`、`uns → Layout`、`ood → Pairing`。Basket/Board 在前三个条件各有 3 个配置，因此合并分母为 90；Floor/Open/Close 各有 2 个，分母为 60；Pairing 仅三类抓放任务各有 2 个，分母为 60。完整小数与原始 `source_log` 路径以 CSV 为准。

## 三、数据、模型与执行协议的实际边界

1. **场景**：本地核验 `emb-ai/RoboBenchMart_demo_envs` 固定修订的 466 个文件；本地可看到 18 个场景目录，142 个场景配置 JSON 及 142 个对应布局 JSON。这是“可用资源文件数”，不是 142 次独立受控实验，也不是完整 50 GB 训练集。场景包和 `assets/` 依项目使用方式另行下载，不与本文轻量 CSV 混同。
2. **演示**：12 个 `demos/motionplanning/*_248traj_4workers.json` 各含 248 条 episode 索引，合计 2,976 条元数据。索引不是轨迹张量；本地没有这些任务的训练 HDF5。旧稿 1,401,169 transitions 不能仅由这些索引验证；索引的 `elapsed_steps` 求和也不能直接当作 transitions。若正文保留旧收集实验与时长，须单独找到原始轨迹和计时证据，否则改为上游资源描述并删除本机重训表述。
3. **检查点与代码**：Octo 使用 `emb-ai/RoboBenchMart_octo` 修订 `f3c8de450fc08fb5737d32442a2b1e6ab2993244` 的 `1000000` 检查点，评测服务 `history=1`、动作块 50；π₀.₅ 使用 `emb-ai/RoboBenchMart_pi05` 修订 `533ad107347c3568dc2456d1586b665889f0ed18`，OpenPI 配置 `pi05_eval_rbm`。本机评测不是四模型同设备、同算力预算的重新训练。Octo 旧论文配置称训练历史 2 帧，本轮服务实际 1 帧，必须如实说明。
4. **评测脚本**：两轮都以项目 `bash/eval_model.sh` 的 42 个原子配置为总体；Board/Floor 上限 750 步、Basket 600、Fridge 500、Showcase 1,000；按项目成功谓词判定。机器人头部与躯干动作固定为零，动作块开环执行 50 步。`Pose` 使用 10000 起始机器人位姿种子；`Layout/Pairing` 使用 42000 起始评测种子；`Seeds/Pose` 从演示索引选前 30 个配置种子。场景选取及种子细节以脚本为准。
5. **并行与可比性**：Octo 最终 CSV 的前 17 个配置来自串行运行，后 25 个来自四个独立服务；π₀.₅ 用四个仿真客户端共享一个 OpenPI 服务。随机数消费顺序与服务状态可能不同，不能声称两个模型逐回合严格配对或与论文旧主表直接做同协议显著性比较。两轮均为已微调权重的推理评测，不是训练完成证明。
6. **原始结果**：π₀.₅ 四工作进程、汇总器及总批次退出码均为 0，42 份配置日志均有一行最终 `Results:`；1,260 MP4、42 HDF5、42 JSON 已索引。JSON 的 `episodes` 为空、HDF5 为 800 字节，不含逐回合轨迹；但 42 份日志的 `Results:` 列出成功回合编号，且与 1,260 段视频文件名对应。项目仓库 `episode_outcomes.csv` 据此给出逐回合成败索引；它来自运行日志，而非独立人工视频判读。Octo 此前仅公开 42 行 CSV，逐回合产物未被一同上传。这一限制必须放进论文数据可用性段。

## 四、论文逐处修改清单（待你审阅后改正文）

| 文件/位置 | 目前内容 | 建议替换或删除 |
| --- | --- | --- |
| `dissertation-metadata.tex`、`c-front-matter/abstract.tex` | 标题和摘要覆盖四模型训练、2,976 完整演示、旧数值与失败分析 | 标题若暗示四模型训练要收窄；摘要改为两模型评测和实际配置/成功数，训练和数据只陈述可验证范围；删旧失败百分比 |
| `chapter-1/chapter-1.tex` 研究问题、目标、贡献与结构 | RQ3 描述四模型适配和 2,906 标签；“共同数据集”与训练结论 | RQ3 改为两个公开微调检查点在四条件下的任务成功率；贡献写可复核评测和协议核查；未做的复合任务/人工标签标为将来工作 |
| `chapter-2/chapter-2.tex` 文献综述与本项目定位 | 文献综述可保留；项目对比表及“四模型策略研究”会过期 | 保留外部文献，核对对“本论文做了什么”的四模型、训练和复合任务用语；模型介绍可作为背景，不必删 π₀/SmolVLA 文献 |
| `chapter-3/chapter-3.tex` 场景、资产、训练语料、实现范围 | 2,976 轨迹/1,401,169 transitions/10 小时被作为本轮完整训练输入；资产库数量可能被误当成目标数 | 区分资产库、实际任务目标、已下载场景和索引元数据；无原始轨迹佐证的训练规模、耗时不得作为本轮本机测量；几何生成等系统内容仅在有原始证据时保留 |
| `chapter-4/chapter-4.tex` §Training protocol | RTX 4090、batch 8、四模型 100k/30k 步、LoRA 排程与时长 | 改成检查点来源和推理服务配置；不再声称本轮执行这些训练；若讲上游训练配方，必须引独立来源并标清不是本轮实验 |
| 同章 §Evaluation scenarios、§Success and side-effect checks | 每 triplet 100 次，按 300/200 聚合；情景、种子与判定 | 改成 42×30、Seeds 12/Pose 12/Layout 12/Pairing 6、90/60 分母；从实际脚本核对门任务 Layout 场景复用、位姿种子、动作接口与成功谓词 |
| 同章 §Failure annotation、§Validity、§Protocol traceability | 2,906 人工标注、11 类分布和基于旧记录的有效性论断 | 删除作为本轮实验结果的旧标签和比例；保留确有代码证据的协议边界；把未标注失败与不成对 episode 作为限制 |
| `chapter-5/chapter-5.tex` 主表和相关图 | 四模型、100 次、Pick 3/Fridge seq.、旧百分数 | 以本文件新表替换，Seeds 增行、SmolVLA/π₀ 与复合列删除；重算图和每段文字，不再把旧 1%、7% 等与新实验混写 |
| 同章 RQ1/RQ2 分析 | mesh timing、118 货架和 10 小时收集等仍来自旧实验 | 若本轮没有重测，明确标成旧工程记录并给数据出处；若要求论文“旧实验全部不要”，这些数值与图也需删除或重新测量。当前仓库只含聚合/绘图输入，无法把它们自动变成新实验 |
| 同章 RQ3、失败原因、分布偏移、协议核查与未来工作 | 四模型排序、失败标签、旧 Pose/Layout 差、复合零成功 | 全部按两模型实际值重写；只保留已由当前脚本验证的协议事实；不要用门任务 Layout 推断布局迁移，不从零成功推出架构能力上限 |
| `chapter-6/chapter-6.tex` 结论 | 四模型固定步数训练、旧主表范围、失败份额与复合结论 | 以两模型任务级结果和已核验的限制重写，删除无本轮证据的结论 |
| `c-back-matter/appendix-b.tex`、`tools/rerun/*`、图生成脚本 | 四模型 LoRA 表、逐商品旧结果、失败分类与旧 CSV | 附录改为 42 配置、模型修订、命令/日志/产物清单；旧 `tools/rerun` 标为历史模板，不能直接用于生成新正文图表；如要求彻底替换旧实验，须移除旧图数据或单独归档 |
| `README.md` 和数据可用性说明 | 仅一般构建提示 | 加本文档与新 CSV 入口、外部权重/场景固定修订、Git LFS 原始产物、无法审计的项目边界 |

论文的程序性方法、场景生成算法和文献不必机械删除，但旧的**实测数值**必须逐项追溯。尤其旧 RQ1/RQ2 工程测量与本轮两模型评测不是同一组证据；如果你的要求是“之前论文实验全部替换”，这些工程实测也须重做，不能把旧测量改个措辞就当成本轮数据。

## 五、建议正文新表标题与表注

> **Task success of two released checkpoints under 42 atomic evaluation configurations.** Each model is evaluated for 30 episodes per configuration. Basket and Board pool 90 episodes per condition, Floor/Open/Close pool 60, and Pairing applies only to the three pick-and-place families (60 each). Counts and percentages are reported together. Door-task Layout reuses training scenes; the results therefore measure the executed test conditions rather than a uniform geometric shift. These are evaluation results of released checkpoints, not local retraining results.

如果后续要补“完全复现训练”：先找到并校验 2,976 条演示的实际图像/状态/动作轨迹及划分、归一化统计、训练代码及其精确修订、配置、种子、步数、硬件与模型选择规则，再运行训练，并为 π₀、SmolVLA、复合任务和失败标注另建新实验批次。当前两模型的 42 配置评测不能证明这些项目已完成。
