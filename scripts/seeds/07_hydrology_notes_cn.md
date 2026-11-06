# 07_hydrology 水文与水资源 —— 检索与筛选笔记

检索日期：2026-10-29；时间窗：首次公开日期 2023-10-29 至 2026-10-29（有 arXiv 版本时按 arXiv v1 计）。
结果：65 条，其中主榜 50 条（46 条近期、4 条窗口外必要文献）+ 备选 15 条（全部为近期）。

## 1. 检索词与平台（实际使用）

### arXiv（通过 scripts/search_candidates_en.py arxiv，自动限定窗口）
1. `(abs:streamflow OR abs:runoff OR abs:"rainfall-runoff") AND (abs:LSTM OR abs:transformer OR abs:"deep learning")`
2. `abs:"ungauged" AND (abs:streamflow OR abs:basins OR abs:catchments)`
3. `(abs:"differentiable" AND (abs:hydrolog* OR abs:"rainfall-runoff"))`
4. `(abs:flood AND abs:forecast* AND (abs:"graph neural" OR abs:"machine learning" OR abs:"deep learning"))`
5. `(abs:drought AND (abs:forecast* OR abs:prediction) AND (abs:SPEI OR abs:SPI OR abs:"drought index"))`
6. `(abs:groundwater AND (abs:"water level" OR abs:"groundwater level") AND (abs:forecast* OR abs:prediction))`
7. `(abs:"soil moisture" AND abs:forecast* AND (abs:"deep learning" OR abs:LSTM OR abs:transformer))`
8. `(abs:reservoir AND (abs:inflow OR abs:operation OR abs:release) AND (abs:forecast* OR abs:prediction) AND (abs:hydrolog* OR abs:streamflow OR abs:dam))`
9. `(abs:"snow water equivalent" OR abs:snowmelt) AND (abs:forecast* OR abs:prediction)`
10. `(abs:"water level" AND (abs:river OR abs:lake) AND abs:forecast*)`
11. `(abs:"foundation model" OR abs:"zero-shot" OR abs:"large language model") AND (abs:streamflow OR abs:hydrolog* OR abs:runoff)`
12. `(abs:CAMELS OR abs:Caravan) AND (abs:streamflow OR abs:hydrolog*)`
13. `(abs:"data assimilation" AND abs:streamflow)`
14. `ti:differentiable AND (abs:hydrolog* OR abs:streamflow OR abs:water)`
15. `abs:"physics-informed" AND (abs:streamflow OR abs:"hydrologic model" OR abs:"hydrological model")`（首次 429，重试成功）
16. `abs:"mass-conserving" AND (abs:LSTM OR abs:hydrolog*)`
17. `(abs:probabilistic OR abs:uncertainty) AND abs:streamflow AND abs:forecast*`
18. `(abs:"seasonal" OR abs:"subseasonal" OR abs:"sub-seasonal") AND (abs:streamflow OR abs:runoff OR abs:"river discharge")`
19. `(abs:"National Water Model" OR abs:"GloFAS" OR abs:"post-processing") AND (abs:streamflow OR abs:discharge)`
20. `(ti:"river discharge" OR ti:"streamflow" OR ti:"runoff") AND (ti:global OR ti:continental OR ti:national OR ti:"large-scale")`
21. `(abs:hydrolog* OR abs:streamflow) AND abs:"time series foundation model"`
22. `(ti:groundwater) AND (ti:forecast* OR ti:prediction OR ti:predicting)`
23. `(ti:drought) AND (ti:forecast* OR ti:prediction OR ti:predicting OR ti:"early warning")`
24. `(ti:flood) AND (ti:forecast* OR ti:prediction OR ti:"early warning") AND (abs:river OR abs:discharge OR abs:streamflow OR abs:"water level")`
25. `(abs:"graph neural network" OR abs:GNN) AND (abs:streamflow OR abs:"river network" OR abs:discharge)`
26. `(abs:hydrolog* AND abs:"large language model")`
27. `(ti:"evapotranspiration" OR ti:"terrestrial water storage" OR ti:GRACE) AND (ti:forecast* OR ti:prediction)`
28. `(ti:"water demand" OR ti:"water consumption") AND ti:forecast*`
29. `(abs:"extreme" AND abs:streamflow AND (abs:"out-of-sample" OR abs:"extrapolat*" OR abs:"climate change"))`（无结果）
30. 两条 `(abs:Shen AND abs:hydrolog*) ...` 之类的辅助查询（无有用结果）

### OpenAlex（scripts/search_candidates_en.py）
- 计划了 23 条全文检索（如 "LSTM streamflow prediction large-sample CAMELS"、"groundwater level forecasting deep learning"、"drought forecasting machine learning SPEI"、"reservoir inflow forecasting"、"snow water equivalent forecasting machine learning" 等），但 OpenAlex **检索接口持续返回 429**（多个 worker 共用额度），全部失败。
- 单篇查询（`abs <DOI>`）可用：用于核实 16 个期刊 DOI，以及通过 `10.48550/arXiv.<id>` 获取约 50 篇 arXiv 论文的完整摘要与 OA 链接（arXiv API 同期大量 429）。

### WebSearch（仅用于发现，结果均再用 helper 核实）
- HESS 2024 LSTM / 可微分模型；HESS 2025 业务洪水预报 LSTM；δHBV 可微分模型（Shen 组）；CAMELS 新数据集（DE/FR/IND/SPAT）；德国地下水位 TFT/N-HiTS（Kunz）；水库入流/下泄预报；干旱预报（npj/HESS/NHESS）；山洪预警（NHESS/HESS）；hess-2023-275 讨论稿日期。

## 2. 纳入/排除原则与主要排除记录

纳入：时间依赖的预测/预警/模拟为核心任务；水文或水资源变量（径流、水位、洪水、干旱、地下水、水库入流、积雪、土壤湿度、陆地水储量）；有合法公开全文（arXiv、Copernicus/Nature/WRR/npj 等 OA）。同一模型族只保留代表作（如扩散径流模型主榜仅留 DRUM 与 h-Diffusion，HydroDiffusion 入备选；河网 GNN 主榜仅留一正一反两篇）。

主要排除：
- **窗口外知名文献**（仅 4 篇作为必要基准纳入主榜：Nearing 2024 Nature〔arXiv 2307.16104，2023-07-30〕、Caravan 2023、Tsai 2021 dPL、Kratzert 2019 EA-LSTM）。未纳入：CAMELS（Addor 2017）、Kratzert 2018 LSTM、Frame 2022 极端事件、Klotz 2022 不确定性、Gauch MTS-LSTM 2021、Wunsch 2021/2022 地下水 CNN、Feng 2020/2022 δ 模型。
- **Feng et al. 2024 GMD δHBV-globe1.0**（10.5194/gmd-17-7181-2024）：正式发表 2024-09-26，但讨论稿 gmd-2023-190 很可能早于 2023-10-29，日期存疑，未纳入。
- **Gomez et al. 2024 HESS 地下水 1D-CNN**（10.5194/hess-28-4407-2024）：正式发表 2024-10-07，但 EGUsphere 预印本 egusphere-2023-1836 预计 2023 年 8–9 月公开，按“早期公开版本”原则排除。
- 水质变量（溶解氧、营养盐、浊度、地下水砷/盐化/重金属，如 2602.07478、2607.19392、2605.00056）→ 属 04_water_quality；河流水温（2410.19865）→ 属水质。
- 降水预报/降尺度本身（如 2608.01626、2411.16098）→ 属 05 气象与气候。
- 二维淹没/水动力代理（FloodCast 2403.12226、Inunda、DiffSWE2d、GNN multimesh 2604.02876）：偏水力学空间模拟，非时间序列预测主线，未纳入。
- 量子 ML 洪水/干旱（2407.01001、2407.08617、2502.20703）、方法内容较弱或很短的会议稿（2405.10375、2606.02791 5 页）、单一案例简单模型比较（2505.18645、2609.26244、2404.07924）。
- 卫星储量估算/河流测量读数（2502.19989、2512.23454）、干旱分类而非预测（2506.04696）、校准代理（HydroAgent 2605.17792）等非预测任务。
- 城市用水需求预测（2501.00158、2509.07515、2512.06714）：属供水管网运营，建议另立领域，未纳入。

## 3. 子方向覆盖表

| 子方向 | 主榜 rank | 备选 rank |
|---|---|---|
| 全球/大陆尺度径流与洪水预报（业务化） | 1, 3, 6, 10, 35 | 52 |
| 大样本 LSTM 范式与经典基线 | 2, 50 | |
| 降雨-径流新架构（SSM、TFT、通用/基础模型基准） | 21, 22, 23, 47 | 53, 58, 63 |
| 可微分 / 物理-数据融合 | 4, 5, 9, 12, 29, 31, 32, 49 | 64, 65 |
| 概率预报与不确定性（扩散、分位数、集合校准） | 7, 11, 17, 27, 28, 29 | 51, 52 |
| 洪水预报与预警（小时/短时、误差校正、频率分析） | 3, 4, 7, 11, 13, 30, 38 | 55 |
| 河网空间信息 / 图网络 / 因果时空 | 6, 25, 26, 27, 37 | 54 |
| 无资料流域（PUB） | 3, 5, 33, 34 | |
| 水位（河流、湿地） | 24, 38, 39 | 59 |
| 地下水位 | 14, 15, 40, 46 | |
| 干旱 / 骤旱（含 S2S） | 16, 17, 48 | 60, 61 |
| 土壤湿度（作为水文变量） | 10, 16, 47 | 61 |
| 积雪 / SWE / 融雪径流 | 10, 18, 41, 43 | 57 |
| 水库入流与调度相关预测 | 19, 39 | 56 |
| 陆地水储量 | 45 | |
| 数据集（Caravan、CAMELS 系列） | 8, 20, 42 | 62 |
| 数据同化 | 11, 12 | |
| 异常检测（径流质控，少量纳入） | 44 | |

地区覆盖：美国（多篇）、全球、德国、意大利、加拿大魁北克、日本、澳大利亚、欧洲、非洲（林波波河、非洲 S2S 干旱）、印度（备选数据集）。

明显缺口：
- 中国/南亚季风区的高质量 OA 径流预报论文偏少（OpenAlex 全文检索失败，期刊论文主要靠 WebSearch 发现）。
- 水库入流与调度：期刊论文较少，主榜只有 2 篇（AdaTrip、FIDLAR）；WebSearch 发现的 J. Hydrol. 2024 梯级水库 LSTM（10.1016/j.jhydrol.2024.130608）OA 状态未核实，未纳入。
- 湖泊水位、冰川融水径流、季节径流统计后处理（如 GloFAS/NWM 后处理）覆盖薄弱。
- 统计方法类偏少（主榜 15、45、46 及 13 中的 ARIMA 对照）。

## 4. 优先阅读 10 篇

1. rank 1 AIFL（全球日径流 LSTM，再分析→IFS 两阶段迁移）——业务预报驱动下的数据驱动全球基线，按时间外推评测。
2. rank 2 HESS Opinions: Never train an LSTM on a single basin——大样本训练的方法论共识。
3. rank 3 Nearing et al. Nature（窗口外）——全球无资料流域洪水预警的标杆与常用对比对象。
4. rank 4 dHBV2.0MTS-MC 小时全国洪水模拟——可微分模型在小时、河网尺度上对比 NWM 与 LSTM。
5. rank 5 Song et al. WRR 2025——可微分模型面向国家水模型的系统性证据。
6. rank 6 RiverMamba——全球 0.05° 网格、利用河网空间关系的 7 天洪水预报。
7. rank 7 DRUM——扩散模型做极端洪水概率预报的代表。
8. rank 14 Kunz et al. HESS 2025——5,288 口井、12 周的全局地下水位预测。
9. rank 16 IT-Drought——骤旱预警与可解释性。
10. rank 28 Ranked Right, Sized Wrong——深度学习集合不确定性在极端流量下的失效，直接关系预警可信度。

## 5. 扩展领域建议

- **城市供水与用水需求预测**（DMA 流量、管网压力、泵站调度）：arXiv 上有一批近期论文（2501.00158、2509.07515、2512.06714、2608.08790），值得单独收集。
- **洪水淹没/水动力代理模型**（PINN、神经算子、GNN 网格代理，如 FloodCast、Inunda、DiffSWE2d）：时空场预测，可作为独立的“水力学代理建模”方向。
- **陆地水储量（GRACE）重建与预测**：与插补/重建交叉（2606.23833 等）。
- **冰湖溃决与冰川灾害预警**（2601.12330 IceWatch 等）。
- **LLM/代理式水文建模**（HydroAgent、AQUAH、2605.16178）：新兴方向，可在通用方法中跟踪。

## 6. 无法核实或存疑的条目

- **API 状况**：OpenAlex 检索接口全程 429，期刊发现主要依赖 WebSearch + 单篇 DOI 核实；arXiv API 也频繁 429，部分 arXiv 摘要改由 OpenAlex（arXiv DOI 10.48550）获取。
- **rank 3 Nearing（old）**：OpenAlex 的 Nature 条目未链接 arXiv；arXiv 2307.16104（v1 2023-07-30）为同一工作的预印本（题名不同），据此判为窗口外。
- **rank 49 Tsai、rank 50 Kratzert 2019（old）**：first_public_date 用的是 OpenAlex 期刊日期；对应 arXiv（2007.15751、1907.08456）v1 的具体日期未取到（API 429），但都明显早于窗口。
- **rank 2 Kratzert HESS Opinions**：WebSearch 显示 HESSD 讨论稿 hess-2023-275 于 2024-01-18 公开，在窗口内。
- **备选 rank 64（Yu, hess-2023-237）、65（Song, hess-2023-258）**：HESSD 讨论稿公开日期未核实，可能接近 2023-10-29，启用前需确认。另一篇同类（Liu 等，hess-2023-235，丹麦混合模型）因同样原因已移出。
- **rank 5 Song WRR**：ESSOAr 预印本（2024-09 前后）与期刊日期都在窗口内。
- **rank 61 Otero（备选）**：只拿到摘要开头片段（arXiv API 429，OpenAlex 无摘要）；另有 Research Square 预印本 2026-07-10，在窗口内。
- **rank 62 CAMELS-IND**：OpenAlex 没有 PDF 链接，pdf_candidates 是按 ESSD 的 URL 规则推断的，需下载时核实。题名写 228 个流域，摘要写 472 个流域，按原文照录。
- **rank 20 Caravan、rank 49 Tsai**：OA 来自 Nature/Scientific Data 出版方，另有 PMC 链接。
- **rank 38 R2RNet**：期刊版（J. Hydrol. Reg. Stud.）在 OpenAlex 中无 PDF 链接，请用 arXiv 2503.19943。
- **rank 40 Salis**：期刊版（MLST）无 PDF 链接，请用 arXiv 2603.25779。
- **rank 34 HYPER**：期刊版（JGR-MLC）无 PDF 链接，请用 arXiv 2507.18423。
- **rank 60 Gao（备选）**：OpenAlex 无 PDF 链接，请用 arXiv 2607.17511。
- 摘要里没有写明的频率、预见期、切分方式统一记为“待全文核实”。
