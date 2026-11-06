# 09_industrial（工业与设备）检索与筛选说明

检索日期：2026-10-29；时间窗：首次公开日期 2023-10-29 至 2026-10-29（有 arXiv 版本的以 arXiv v1 为准）。
产出：`scripts/seeds/09_industrial_seed_cn.json`，共 65 条：第 1-50 名为主列表，第 51-65 名为备选。全部为窗口内文献，没有收录窗口前的旧文献。

## 1. 检索词与平台（实际使用）

都通过 `scripts/search_candidates_en.py` 调用（日期过滤由脚本完成）。

arXiv（`arxiv` 命令）：
1. `abs:"remaining useful life" AND abs:turbofan`
2. `abs:"remaining useful life" AND abs:bearing`
3. `abs:battery AND (abs:"remaining useful life" OR abs:"capacity degradation" OR abs:"cycle life") AND abs:predict*`
4. `abs:"N-CMAPSS" OR (abs:"C-MAPSS" AND abs:foundation)`
5. `abs:"remaining useful life" AND (abs:"foundation model" OR abs:"large language model" OR abs:"pre-trained")`
6. `abs:"remaining useful life" AND abs:"physics-informed"`
7. `abs:degradation AND (abs:"Wiener process" OR abs:"gamma process" OR abs:"stochastic degradation")`
8. `abs:"tool wear" AND (abs:predict* OR abs:forecast*)`
9. `abs:"soft sensor" AND (abs:"time series" OR abs:temporal OR abs:dynamic)`
10. `abs:"remaining useful life" AND (abs:leakage OR abs:benchmark OR abs:evaluation) AND (abs:split OR abs:protocol OR abs:pitfall*)`
11. `abs:"remaining useful life" AND (abs:conformal OR abs:probabilistic OR abs:"uncertainty quantification")`
12. `abs:battery AND (abs:"foundation model" OR abs:"large-scale" OR abs:benchmark) AND (abs:lifetime OR abs:"cycle life" OR abs:degradation)`
13. `abs:"tool wear" OR abs:"cutting tool" AND abs:"remaining useful life"`
14. `ti:"soft sensor" OR ti:"soft sensing"`
15. `abs:"remaining useful life" AND (abs:survival OR abs:censor*)`
16. `abs:"industrial time series" AND (abs:forecast* OR abs:"foundation model")`
17. 以下三条因 arXiv 返回 HTTP 429 而失败，没有拿到结果：`abs:"predictive maintenance" AND (abs:forecast* OR abs:"failure prediction") AND abs:"time series"`；`abs:"fuel cell" AND abs:degradation AND (abs:predict* OR abs:prognos*)`；`abs:"health indicator" AND abs:degradation AND abs:prognos*`。燃料电池与预警主题改用 OpenAlex 补检。
18. 用 `abs` 命令批量取回约 90 个候选 arXiv ID 的完整摘要（id_list 分块）。

OpenAlex（`openalex` 命令，大多加 `--oa`）：
- 标题检索（`--title`）：`remaining useful life prediction`；`tool wear prediction`
- 全文检索：`degradation modeling Wiener process remaining useful life`；`soft sensor industrial process time series`；`battery capacity degradation trajectory prediction`；`wind turbine remaining useful life prognostics`；`prognostics remaining useful life Reliability Engineering System Safety deep learning uncertainty`；`digital twin remaining useful life prediction time series`；`predictive maintenance failure prediction early warning sensor time series industrial`；`large language model prognostics health management time series`；`gearbox degradation prediction remaining useful life`；`Annual Conference PHM Society remaining useful life`；`battery lifetime prediction Nature Communications degradation machine learning`；`physics-informed neural network battery degradation prognosis`；`proton exchange membrane fuel cell degradation voltage prediction`；`railway track geometry degradation prediction`；`hard disk drive failure prediction SMART`；`pipeline corrosion growth prediction time series`；`aircraft engine N-CMAPSS remaining useful life`；`IGBT power module degradation remaining useful life prediction`
- 用 `abs <DOI>` 核对了 23 篇期刊文献的 OA 位置与摘要（如 iMOE、IJPHM 两篇、风电两篇、IGBT、MD2N、engrXiv 审计稿等）。
- 一次按标题批量核对时 OpenAlex 返回 HTTP 429，已中止，之后改为逐个 DOI 查询。

WebSearch：未使用。

## 2. 纳入/排除原则与主要排除记录

纳入原则：
- 核心任务必须带时间依赖，包括 RUL/退化轨迹预测、未来时段的故障预警、过程变量的时序预测或动态软测量。优先选预测类。
- 每条必须有合法公开的全文 PDF：53 条有 arXiv；另外 12 条只有期刊/预印本 OA（第 18、20、22、32、42、43、45、52、54、60、61、64 名），包括 Nature Communications、Scientific Reports、IJPHM（PHM Society，diamond OA）、Wiley 的 Wind Energy（gold）、MDPI、engrXiv，以及 IJPR（hybrid，另有 UNIST 机构库版本）。
- 刻意让设备类型、数据集和方法都分散，同一类应用不扎堆。设备类型：涡扇/涡轮发动机、轴承、锂电池/储能、刀具、风电齿轮箱、燃料电池、IGBT、半导体离子铣、核电蒸汽发生器、铁路轨道、过程工业/生物制药/油气井、卫星电子、管道、超滤膜。方法：随机过程、生存分析、贝叶斯、深度学习、物理融合、基础模型/LLM。
- 异常检测类只收 2 条（主列表第 14 名、备选第 65 名），都已标注。预警类收 4 条（第 47、48、64 名，以及第 43 名的 FPT 阶段）。综述 3 条（第 49、50、51 名）。

主要排除记录：
- arXiv 2503.13558（Survival Analysis with ML for Li-ion Battery RUL）：arXiv 已以“作者身份与单位无法核实”为由撤稿，排除。
- arXiv 2404.04824 / KBS 版本 “Mixup Domain Adaptations for Dynamic RUL Predictions”：OpenAlex 显示期刊版本已撤稿（RETRACTED），排除。
- Bayesian multivariate track geometry degradation（Railway Engineering Science 2025）：arXiv 2308.14240 的 v1 早于窗口，排除。
- ChatGPT-like large-scale foundation models for PHM: A survey and roadmaps（RESS 2023-11）：arXiv 预印本（2305.x）早于窗口，按规则视为旧文献，未收录。
- 知名但早于窗口、本次没有作为旧文献纳入的：C-MAPSS 原始数据集（Saxena 2008）、N-CMAPSS 数据集（Arias Chao 2021）、Severson 等 2019 电池早期寿命预测（Nature Energy）、BatLiNet（arXiv 2310.05052，v1 2023-10，早于窗口）、XJTU-SY 轴承数据集论文（2020）。CruiseBench、BatteryLife 等新基准已覆盖它们的数据，所以没有动用旧文献名额。
- Physics-informed neural network for Li-ion battery degradation stable modeling and prognosis（Nature Communications 2024）：摘要显示主要是 SOH 估计，不是对未来的预测，暂不收录。可作为替补。
- 只做故障分类/诊断的大量文献（CWRU 等）、只有标题摘要页而无 OA PDF 的 Elsevier 文章（例如 RESS 上的 Basora 2024 UQ 基准，OA 状态为 bronze 且没有 PDF 链接；Change point severity-aware RUL，为 hybrid 但没有 PDF 链接），以及弱期刊/疑似低质量来源（多篇 IJ* 类期刊的 “Predictive Maintenance … IoT” 文章），均排除。
- 硬盘 SMART 失效预测：候选里只有 bronze/低质量来源，或 OA 状态不明（例如 DiskAdapt 为 bronze 且没有 PDF），本轮未收录。

## 3. 子方向覆盖表

| 子方向 | 主列表排名 | 备选排名 |
|---|---|---|
| 涡扇/涡轮发动机 RUL（C-MAPSS/N-CMAPSS/真实机队） | 2, 7, 19, 20, 24, 25 | 58, 63 |
| 评测与泄漏批评、标签与协议 | 3, 11, 21, 22, 9（理论） | 57 |
| 轴承 RUL | 8, 11, 21 | — |
| 锂电池寿命/容量衰减/储能 | 1, 5, 12, 18, 26, 27, 28, 29, 30 | 52, 59 |
| 刀具磨损 | 31, 32 | — |
| 过程工业软测量/过程预测 | 16, 17, 33, 34, 35 | 56 |
| 工业基础模型 / LLM / TSFM | 4, 6, 13, 14, 15, 36, 37, 50 | 51, 52, 55 |
| 随机退化模型 / 生存分析 / 联合模型 | 8, 10, 23, 38, 39 | 53 |
| 数字孪生 | 6, 40 | — |
| 不确定性 RUL（贝叶斯/保形/分位数/GP） | 7, 20, 28, 29, 42, 43 | 54 |
| 其他设备（风电、燃料电池、IGBT、半导体、铁路、核电） | 40, 41, 42, 43, 44, 45, 46 | 60, 61, 62 |
| 故障预警（预测窗口内是否失效、变点） | 47, 48（14 为异常检测类） | 64, 65 |
| 综述 | 49, 50 | 51 |

明显缺口：
- 齿轮箱以外的旋转机械（泵、压缩机）、航空起落架、船舶系统都没有找到合格的 OA 预测论文。
- 硬盘/数据中心设备失效预测，以及工业基础模型在真实工厂长期部署的评估，都没有合格条目。
- 刀具磨损只有 2 篇，高质量 OA 论文偏少，大多是 MDPI 或一般期刊。
- 软测量文献多为“当前时刻推断”，真正多步预测的只有第 16、17 名。
- 物理信息神经网络（PINN）RUL 论文很多，但多为 SOH 估计或质量一般，主列表只通过第 30、40 名间接覆盖物理融合。

## 4. 优先阅读 10 篇

1. 第 3 名 Leakage-Robust Evaluation…（2607.16493）：量化滑动窗口切分泄漏把准确率从 20-60% 抬到 99.9%，是数据集划分批评的直接证据。
2. 第 22 名 Auditing Operating-Condition Normalization in C-MAPSS…（engrXiv 10.31224/8145）：1800 次受控运行显示归一化与重拟合策略会改变 C-MAPSS 的 RMSE 排名。
3. 第 2 名 CruiseBench（2607.19380）：给 N-CMAPSS 一个固定、可复现的巡航段协议。
4. 第 1 名 BatteryLife（2502.18807）：目前最广的电池寿命数据集与统一基准。
5. 第 4 名 Self-Supervised Pretraining for PHM（2610.35280）：在泄漏受控条件下，预训练对 RUL 无稳定收益。
6. 第 14 名 Do TSFMs Pay Off for Industrial Monitoring?（2608.22968）：计入成本后，轻量基线仍有竞争力。
7. 第 15 名 IND-Eval（2610.16652）：专门面向工业时间序列的 TSFM 预测基准。
8. 第 11 名 Empirical Calibration … under Operating-Regime Shift（2607.08273）：按工况留出评测，并看条件覆盖率。
9. 第 8 名 RULSurv（2405.01614）：在 RUL 建模中显式处理删失数据。
10. 第 9 名 Generalization bounds and sample complexity for RUL（2607.23454）：从理论上回答“需要多少条失效轨迹”。

## 5. 扩展领域建议

- 电池老化与储能寿命可以考虑单独成类。本次候选非常多（PINN、迁移学习、LLM、现场数据），这里只能抽样，并且与“能源与电力”交叉明显。
- 制造过程/半导体工艺时序（虚拟量测、批次过程、发酵）适合与软测量合并，作为一个“过程工业预测”专题。
- 基础设施退化（铁路轨道、管道腐蚀、桥梁）适合独立收集，与“交通与出行”“水文与水资源”交叉。
- PHM 评测方法学（泄漏、标签设计、协议、校准）值得做一个跨领域专题，可与“通用方法”的评测类文献对照。

## 6. 无法核实或存疑的条目

- 第 24 名 THGNN（2405.04336）：OpenAlex 显示后来刊于 IEEE TNNLS，但本次没有取得期刊 DOI，venue 字段已注明待核实。
- 第 7、41、48、49、50 名的期刊信息（TASE、MSSP、RESS）来自 OpenAlex 或 arXiv 元数据。PDF 路线用的是 arXiv 版本，期刊版本可能不是 OA。
- 第 22 名是 engrXiv 预印本，未经同行评审，OpenAlex 标记为 acceptedVersion，期刊去向不明。第 3、4、9 以外的多篇 2026 年 arXiv 预印本同样是未评审稿件，评审状态以 arXiv comments 为准。
- 第 32 名 MD2N（IJPR）：OpenAlex 标为 hybrid OA，出版社 PDF 链接带 needAccess 参数，可能需要验证。另有 UNIST 机构库 PDF 作为备用。
- 第 18、42 名及备选第 52 名（Nature 系期刊）：OpenAlex 给的 pdf 链接是 `_reference.pdf` 形式。若下载失败，应改用 `https://www.nature.com/articles/<id>.pdf` 或 PMC 版本（第 18 名已列出 PMC 与 Chalmers 机构库链接）。
- 第 1 名（v7）、第 5 名（v7）、第 27 名（v3）等有多个 arXiv 版本，数字指标以 v1 之后的修订版摘要为准。
- 大部分条目的数据频率、预测跨度、切分方式摘要中没有写，已统一标“待全文核实”。
- 备选第 65 名与主列表第 14 名属于异常检测类，按规则限量收录并已在 task_type 中标注。
