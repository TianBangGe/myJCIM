# 知识增强的有机分子还原电位预测研究

> 最后更新：2026-09-16
> 当前阶段：D3TaLES 数据审计、清洗与固定划分已完成；无 KG 模型基线尚未开始。

本文档用于持续记录项目已经完成的工作、关键研究决策、数据版本、实验产物和后续任务。以后每确认完成一个新任务，都应同步更新“当前进度”“对应成果”和“更新日志”，避免研究过程与论文记录脱节。

---

## 1. 研究目标

本项目拟研究：

> 文献中可迁移的“官能团—电子效应—还原机制”知识，能否提高图神经网络对未见分子骨架的还原电位预测能力，并为预测结果提供可追溯的化学解释。

当前暂定论文题目：

> **《知识增强的有机氧化还原分子还原电位图神经网络预测与解释研究》**

核心科研假设：

> 当测试分子的整体骨架未出现在训练集中时，可迁移的官能团与还原机制知识能够为纯数据驱动模型提供额外先验，从而改善 scaffold-level generalization。

---

## 2. 已冻结的研究方案

| 项目 | 当前决定 |
|---|---|
| 数据集 | D3TaLES Final Public Dataset |
| 研究对象 | 中性有机分子 |
| 唯一主要任务 | `reduction_potential` 单目标回归 |
| 主评价划分 | 不含手性的 Bemis–Murcko Scaffold Split |
| 辅助评价划分 | Random Split |
| 分子图模型 | GINE |
| 显式分子特征 | RDKit 2D descriptors |
| 外部知识 | 文献还原机制知识图谱 |
| 知识融合 | Mean Pooling 与 Knowledge Attention 对照 |
| 溶剂处理 | 固定数据背景，不建立 Solvent Branch |
| 禁止作为输入 | HOMO、LUMO、IP、EA、DFT 能量及其他目标衍生字段 |

本项目暂不把以下内容纳入主要研究路线：

- 多溶剂预测；
- 氧化电位主任务或氧化—还原多任务学习；
- 三维构象神经网络；
- DFT 计算结果作为模型输入；
- 分子生成与虚拟筛选；
- 实验合成验证；
- 在线调用大语言模型进行预测。

选择还原电位作为主任务，不是因为其样本数量更多，而是因为它与前期 ReSolved 基线、已构建的还原机制知识图谱和最终解释目标具有一致的任务语义。

---

## 3. 当前进度总览

### 已完成

- [x] 保留 ReSolved 作者代码、数据和已有模型文件；
- [x] 完成文献 KG 小规模试点；
- [x] 完成 KG 候选关系人工审核；
- [x] 完成第一版 SMARTS 规则；
- [x] 确定 D3TaLES 为新数据集；
- [x] 确定 `reduction_potential` 为唯一主要目标；
- [x] 完成 D3TaLES 原始数据审计；
- [x] 完成中性分子筛选与 SMILES 标准化；
- [x] 完成重复分子分析与冲突处理；
- [x] 冻结清洗数据集 `D3TaLES-Reduction-v1`；
- [x] 完成不含手性的 Scaffold Split；
- [x] 完成 Random Split；
- [x] 验证 Scaffold Split 三个集合之间没有骨架交集。

### 已确定但尚未实施

- [ ] 给 KG 关系增加 `prediction_scope`；
- [ ] 给 KG 关系增加 `condition_scope`；
- [ ] 从完整文献 KG 中确定 Prediction Subgraph；
- [ ] 在 D3TaLES 全量分子上重新执行 SMARTS 匹配；
- [ ] 生成 D3TaLES 分子—概念边；
- [ ] 构建 Shuffled-KG 对照；
- [ ] 实现 Knowledge Attention。

### 尚未开始

- [ ] B1：RF/XGBoost + RDKit descriptors；
- [ ] B2：Descriptor-MLP；
- [ ] B3：GINE；
- [ ] B4：GINE + Descriptor；
- [ ] B5：B4 + Shuffled-KG + Mean Pooling；
- [ ] B6：B4 + Real-KG + Mean Pooling；
- [ ] B7：B4 + Real-KG + Knowledge Attention；
- [ ] 五随机种子正式实验；
- [ ] 消融实验和解释性分析。

---

## 4. 项目目录

```text
myJCIM/
├── ReSolved/                  # 原始Baseline与KG试点
├── ReSolvedDB/                # ReSolved原始数据资源
├── configs/                   # 后续实验配置
├── data/
│   ├── raw/                   # 原始D3TaLES CSV
│   ├── interim/               # 冲突记录等中间产物
│   ├── processed/             # 冻结后的建模数据
│   └── splits/                # 固定数据划分
├── notebooks/                 # 人工逐格运行的数据处理Notebook
├── reports/
│   ├── data/                  # 统计、元数据和审核记录
│   ├── figures/               # 数据与实验图表
│   └── results/               # 后续模型结果
├── src/
│   ├── data/                  # 后续正式数据管线
│   ├── descriptors/           # RDKit描述符处理
│   ├── kg/                    # KG匹配、编码与对照
│   ├── models/                # GINE和融合模型
│   └── training/              # 训练与评价
├── tests/                     # 自动测试
└── README.md                  # 本项目进度文档
```

`notebooks/` 用于探索、逐格检查和展示中间结果；当规则完全确定后，可再将稳定流程整理为 `src/` 下的可重复执行脚本。目前数据处理逻辑仍以经过人工运行和核查的 Notebook 为准。

---

## 5. ReSolved 基线保留情况

原作者代码和相关资源保留在：

- [`ReSolved/ReSolved/`](ReSolved/ReSolved/)
- [`ReSolved/ReSolvedDB/`](ReSolved/ReSolvedDB/)
- [`ReSolvedDB/`](ReSolvedDB/)

当前已经保留的主要内容包括：

- 作者的模型、训练和评价代码；
- ReSolved 数据；
- 已有模型权重；
- 原始项目说明；
- 早期 KG 试点代码及产物。

这些内容作为前期基线和历史成果保留。新的 D3TaLES 数据管线和后续 B1–B7 实验不会直接覆盖原作者目录。

本 README 不声称目前已经在 D3TaLES 上复现任何模型性能；D3TaLES 无 KG 基线尚未开始。

---

## 6. 已完成的知识图谱试点

KG 试点位于 [`ReSolved/kg_pilot/`](ReSolved/kg_pilot/)。

### 6.1 文献和关系审核

已完成的统计：

| 内容 | 数量 |
|---|---:|
| 注册文献来源 | 12 |
| LLM 候选关系 | 60 |
| 人工审核记录 | 120 |
| 正式批准关系 | 30 |
| 被拒绝候选 | 30 |
| 正式关系涉及概念节点 | 44 |
| 正式关系类型 | 9 |
| 直接证据落地关系 | 9 |

正式使用的 9 类关系为：

- `arises_from`
- `has_electronic_effect`
- `has_inductive_effect`
- `has_redox_state`
- `has_resonance_effect`
- `promotes_delocalization`
- `shifts_reduction_potential`
- `stabilizes_state`
- `transmitted_through`

相关文件：

- [`sources.csv`](ReSolved/kg_pilot/sources.csv)：文献来源登记；
- [`passages.jsonl`](ReSolved/kg_pilot/passages.jsonl)：证据段落；
- [`llm_candidates.jsonl`](ReSolved/kg_pilot/llm_candidates.jsonl)：LLM 候选关系；
- [`review_log.csv`](ReSolved/kg_pilot/review_log.csv)：人工审核记录；
- [`concept_relations.csv`](ReSolved/kg_pilot/concept_relations.csv)：正式批准关系；
- [`schema.json`](ReSolved/kg_pilot/schema.json)：KG 实体和关系模式；
- [`quality_report.json`](ReSolved/kg_pilot/quality_report.json)：质量检查报告。

### 6.2 SMARTS 与旧数据试点

已建立 17 条结构 SMARTS 规则，并在旧 ReSolved 数据中选取 100 个分子完成试点：

| 项目 | 结果 |
|---|---:|
| 试点分子 | 100 |
| SMARTS 规则 | 17 |
| 分子—概念边 | 256 |
| 被知识覆盖的分子 | 100 |
| 试点结构覆盖率 | 100% |
| 无效 SMILES | 0 |
| 目标字段泄漏问题 | 0 |

相关文件：

- [`smarts_rules.csv`](ReSolved/kg_pilot/smarts_rules.csv)
- [`pilot_molecules.csv`](ReSolved/kg_pilot/generated/pilot_molecules.csv)
- [`molecule_concepts.csv`](ReSolved/kg_pilot/generated/molecule_concepts.csv)
- [`build_report.json`](ReSolved/kg_pilot/generated/build_report.json)

### 6.3 当前限制

上述 100 个分子和 256 条分子—概念边属于旧 ReSolved 试点，不能直接用于 D3TaLES。

可以复用的是：

- 文献来源；
- 证据段落；
- 已审核关系；
- KG schema；
- SMARTS 规则及审核思路。

必须重新执行的是：

- D3TaLES 分子结构匹配；
- SMARTS 命中人工抽查；
- D3TaLES 分子—概念边生成；
- KG 覆盖率统计；
- `prediction_scope` 与 `condition_scope` 标注。

---

## 7. D3TaLES 原始数据审计

审计 Notebook：[`01_d3tales_data_audit.ipynb`](notebooks/01_d3tales_data_audit.ipynb)

原始文件：[`data/raw/d3tales_public.csv`](data/raw/d3tales_public.csv)

原始文件 SHA256：

```text
40dc15b8dd00800a23b4ad6f57456634c8163a237cd7cb32aafa9addb7db492d
```

### 7.1 原始数据规模

| 项目 | 数量 |
|---|---:|
| 原始记录 | 35,777 |
| 字段 | 98 |
| `reduction_potential` 非空 | 30,356 |
| `solv_reduction_potential` 非空 | 30,356 |
| 两个还原电位字段共同非空 | 30,356 |
| 两字段最大绝对差 | 0 |

因此正式建模只使用 `reduction_potential`，不重复使用 `solv_reduction_potential`。

### 7.2 中性分子与 SMILES

| 处理步骤 | 剩余数量 | 本步删除 |
|---|---:|---:|
| 原始记录 | 35,777 | 0 |
| 还原电位非空 | 30,356 | 5,421 |
| `groundState_charge == 0` | 30,145 | 211 |
| RDKit SMILES 有效 | 30,145 | 0 |

### 7.3 重复分子审计

| 项目 | 数量 |
|---|---:|
| 有效候选记录 | 30,145 |
| 唯一 Canonical SMILES | 30,117 |
| 重复分子组 | 27 |
| 多余重复记录 | 28 |
| 重复组最大目标极差 | 1.215 eV |

审计阶段没有立即删除重复记录，而是先统计每组目标极差并绘制分布，再据此确定正式规则。

主要产物：

- [`d3tales_data_audit.json`](reports/data/d3tales_data_audit.json)
- [`d3tales_data_flow.csv`](reports/data/d3tales_data_flow.csv)
- [`d3tales_duplicate_groups.csv`](reports/data/d3tales_duplicate_groups.csv)
- [`d3tales_source_distribution.csv`](reports/data/d3tales_source_distribution.csv)
- [`d3tales_data_audit.png`](reports/figures/d3tales_data_audit.png)

---

## 8. D3TaLES 清洗数据冻结

清洗 Notebook：[`02_d3tales_cleaning.ipynb`](notebooks/02_d3tales_cleaning.ipynb)

冻结版本名称：

```text
D3TaLES-Reduction-v1
```

### 8.1 重复处理规则

根据 27 个重复组的目标极差分布，采用以下规则：

- 同一 Canonical SMILES 的目标极差不超过 `0.05 eV`：目标值取均值；
- 目标极差超过 `0.05 eV`：整组作为冲突记录排除；
- 所有冲突原始记录单独保存，保证过程可追溯。

处理结果：

| 项目 | 数量 |
|---|---:|
| 取平均的重复组 | 12 |
| 排除的冲突组 | 15 |
| 冲突组原始记录 | 31 |
| 原本唯一的分子 | 30,090 |
| 最终唯一分子 | **30,102** |

### 8.2 最终目标统计

| 统计量 | `reduction_potential` |
|---|---:|
| 均值 | 6.799163 |
| 标准差 | 1.039974 |
| 最小值 | 3.418 |
| 最大值 | 11.000 |

清洗前后目标分布基本重合，说明少量重复和冲突处理没有明显改变总体分布。

最终清洗文件：

- [`d3tales_reduction_neutral_v1.csv`](data/processed/d3tales_reduction_neutral_v1.csv)

清洗文件 SHA256：

```text
377c6cee92531d0a93e24b4644a118de54d88ae2b1915ff15564c70a80498705
```

追溯文件：

- [`d3tales_conflicting_duplicates_v1.csv`](data/interim/d3tales_conflicting_duplicates_v1.csv)
- [`d3tales_duplicate_decisions_v1.csv`](reports/data/d3tales_duplicate_decisions_v1.csv)
- [`d3tales_cleaning_flow_v1.csv`](reports/data/d3tales_cleaning_flow_v1.csv)
- [`d3tales_cleaning_metadata_v1.json`](reports/data/d3tales_cleaning_metadata_v1.json)
- [`d3tales_cleaning_comparison.png`](reports/figures/d3tales_cleaning_comparison.png)

---

## 9. 固定数据划分

划分 Notebook：[`03_d3tales_splits.ipynb`](notebooks/03_d3tales_splits.ipynb)

统一配置：

```text
Train / Validation / Test = 80% / 10% / 10%
固定种子 = 42
```

### 9.1 Scaffold Split 主划分

主划分使用：

```text
Bemis–Murcko scaffold
includeChirality=False
```

采用不含手性的 scaffold 是为了防止同一拓扑骨架的不同立体异构体进入不同集合。

第一次划分曾直接使用保留手性信息的 scaffold 字符串。虽然字符串交集为 0，但去除手性后发现：

- train–valid 有 75 个骨架交集；
- train–test 有 79 个骨架交集；
- valid–test 有 24 个骨架交集；
- 验证集和测试集中共有 154 个分子与训练集共享非手性骨架。

因此第一次划分未被冻结。随后从 Canonical SMILES 重新生成 `includeChirality=False` 的标准 scaffold 并重新运行，泄漏问题已经消除。

最终结果：

| 集合 | 分子数 | 实际比例 | Scaffold 数 |
|---|---:|---:|---:|
| Train | 24,081 | 79.998% | 9,555 |
| Validation | 3,010 | 9.999% | 3,010 |
| Test | 3,011 | 10.003% | 3,011 |

最终非手性 scaffold 总数为 15,576，三个集合之间的 scaffold 交集均为 0。

Scaffold Split 目标统计：

| 集合 | 均值 | 标准差 | 最小值 | 最大值 |
|---|---:|---:|---:|---:|
| Train | 6.809240 | 1.050899 | 3.418 | 11.00 |
| Validation | 6.746121 | 0.979505 | 3.530 | 10.69 |
| Test | 6.771600 | 1.008574 | 4.204 | 10.99 |

该数据具有大量单分子 scaffold：15,576 个 scaffold 中，12,688 个只包含一个分子。因此标准的“按 scaffold 规模降序、依次填充集合”策略会使验证集和测试集主要由单分子新骨架组成。这使主测试更严格，论文中应明确说明。

### 9.2 Random Split 辅助划分

Random Split 使用同一数据版本、同一比例和种子 42：

| 集合 | 分子数 | 实际比例 |
|---|---:|---:|
| Train | 24,081 | 79.998% |
| Validation | 3,010 | 9.999% |
| Test | 3,011 | 10.003% |

Random Split 只作为辅助性能参考，论文主要结论以 Scaffold Split 为准。

冻结文件：

- [`scaffold_seed42.csv`](data/splits/scaffold_seed42.csv)
- [`random_seed42.csv`](data/splits/random_seed42.csv)
- [`d3tales_split_summary_v1.csv`](reports/data/d3tales_split_summary_v1.csv)
- [`d3tales_split_metadata_v1.json`](reports/data/d3tales_split_metadata_v1.json)
- [`d3tales_split_distributions_v1.png`](reports/figures/d3tales_split_distributions_v1.png)

后续所有 B1–B7 模型必须复用这些划分文件，不能为不同模型重新划分数据。

---

## 10. 当前环境记录

数据阶段实际运行环境：

| 软件 | 版本 |
|---|---|
| Python | 3.10.21 |
| pandas | 2.3.3 |
| NumPy | 1.26.4 |
| RDKit | 2022.09.5 |

本地 Notebook 应使用包含上述依赖的 Conda 环境。系统 Python 3.9 中存在 pandas 与 NumPy 二进制不兼容问题，因此不应用系统 Python 运行本项目 Notebook。

---

## 11. 后续实验矩阵

| 编号 | 模型 | 研究问题 | 状态 |
|---|---|---|---|
| B1 | RF/XGBoost + RDKit | 传统描述符模型能达到什么水平？ | 未开始 |
| B2 | Descriptor-MLP | 非线性描述符模型能达到什么水平？ | 未开始 |
| B3 | GINE | 纯分子图能达到什么水平？ | 未开始 |
| B4 | GINE + Descriptor | 显式描述符能否补充 GNN？ | 未开始 |
| B5 | B4 + Shuffled-KG + Mean Pooling | 增加 KG 模块和参数本身是否带来提升？ | 未开始 |
| B6 | B4 + Real-KG + Mean Pooling | 正确的领域知识是否有效？ | 未开始 |
| B7 | B4 + Real-KG + Knowledge Attention | 自适应知识选择是否进一步有效？ | 未开始 |

核心证据链：

```text
B3 vs B4：描述符是否有效
B4 vs B5：仅增加KG模块是否有效
B5 vs B6：真实知识语义是否有效
B6 vs B7：Knowledge Attention是否有效
```

Shuffled-KG 不能使用简单随机向量。它应尽量保持：

- 相同节点与关系数量；
- 相同 embedding 维度；
- 相同 KG encoder 和融合结构；
- 相同模型参数规模；
- 每个分子的连接数量和概念总体频率基本不变；
- 仅打乱 molecule–concept 的语义对应关系。

---

## 12. 下一步任务

当前下一项正式任务是：

> **生成只基于 SMILES 的 RDKit 2D 描述符，并建立 B1 传统机器学习基线。**

开始模型训练前，应先完成：

1. 确定 RDKit 2D 描述符清单；
2. 删除全空列、常数列和不稳定字段；
3. 只使用训练集统计量进行缺失值填充和标准化；
4. 保存描述符名称与预处理参数；
5. 使用固定 Scaffold Split 训练 B1；
6. 使用固定 Random Split 完成辅助实验；
7. 报告 MAE、RMSE 和 \(R^2\)。

目前尚未执行上述任务，也没有可报告的模型性能。

---

## 13. 对论文写作可直接使用的材料

### 数据章节

可以使用：

- 原始数据规模和字段数量；
- 还原电位非空样本数量；
- 中性分子筛选理由与数量；
- SMILES 有效性检查；
- Canonical SMILES 去重方法；
- 重复组极差分布；
- 0.05 eV 决策规则；
- 冲突数据处理结果；
- 清洗前后目标分布；
- 最终 30,102 个分子的数据版本。

### 数据划分章节

可以使用：

- Scaffold Split 为主、Random Split 为辅的理由；
- Bemis–Murcko scaffold 的定义；
- `includeChirality=False` 的防泄漏理由；
- 80%/10%/10% 固定划分；
- 三个集合的样本数、目标统计和 scaffold 数；
- 三个集合 scaffold 交集为 0；
- 数据中大量 singleton scaffold 带来的严格泛化场景。

### KG 构建章节

可以使用：

- 文献来源登记流程；
- LLM 候选关系生成；
- 人工审核流程；
- 正式关系与证据句绑定；
- SMARTS 规则设计；
- 小规模结构覆盖试点；
- 目标字段泄漏检查。

KG 在 D3TaLES 上的覆盖率和性能贡献尚未得到，因此当前不能在论文中声称 KG 已经改善预测性能。

---

## 14. README 更新规则

以后每完成并确认一个任务，应同步执行以下更新：

1. 在“当前进度总览”中勾选对应任务；
2. 在相关章节记录方法、参数和真实结果；
3. 链接对应 Notebook、数据、配置、图表或模型文件；
4. 记录随机种子、软件版本和文件 SHA256；
5. 明确区分“已完成”“已确定但未实施”和“计划”；
6. 如果发现并修正错误，保留错误原因和修正过程；
7. 在下方更新日志追加一条记录，不删除旧记录。

除非重新生成并登记新版本，否则不得因为后续模型结果不理想而修改已经冻结的数据清洗规则或数据划分。

---

## 15. 更新日志

### 2026-09-16

- 创建项目标准目录结构；
- 完成 D3TaLES 数据审计 Notebook；
- 确认两个还原电位字段在共同非空记录上完全一致；
- 完成中性分子筛选、Canonical SMILES 标准化和重复组分析；
- 冻结 `D3TaLES-Reduction-v1`，最终包含 30,102 个唯一中性分子；
- 完成 Scaffold Split 和 Random Split；
- 发现第一次 Scaffold Split 保留手性导致隐蔽骨架交集；
- 改为 `includeChirality=False` 后重新划分；
- 最终确认 train、validation、test 之间非手性 scaffold 交集均为 0；
- 创建本 README，开始持续记录研究进度。

### 2026-09-15 及以前

- 保留 ReSolved 作者代码、数据和模型资源；
- 完成文献 KG 小规模试点；
- 建立 12 个来源、60 条候选关系和 120 条审核记录；
- 确认 30 条正式关系、44 个概念节点和 9 类关系；
- 建立 17 条 SMARTS 规则；
- 在旧 ReSolved 数据的 100 个分子上生成 256 条分子—概念边并通过试点质量检查。
