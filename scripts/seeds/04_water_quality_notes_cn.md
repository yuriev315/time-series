# 04_water_quality（水质）检索与筛选笔记

检索日期：2026-10-29；时间窗：首次公开 2023-10-29 至 2026-10-29。
结果：65 条（主列表 rank 1–50，备选 rank 51–65），全部为近三年文献，**无三年前文献**（old = 0）。

## 1. 检索词与平台（实际执行的查询）

全部通过 `scripts/search_candidates_en.py` 完成，未直接调用 API，未下载 PDF。

**arXiv**
1. `(abs:"water quality" OR abs:"dissolved oxygen") AND (abs:forecasting OR abs:prediction)`
2. `(abs:"chlorophyll" OR abs:"algal bloom" OR abs:"harmful algal" OR abs:cyanobacteria) AND (abs:forecast OR abs:forecasting OR abs:prediction)`
3. `(abs:nitrate OR abs:phosphorus OR abs:nutrient OR abs:turbidity OR abs:"suspended sediment") AND (abs:forecast OR abs:forecasting) AND (abs:river OR abs:stream OR abs:catchment OR abs:lake)`
4. `(abs:"wastewater treatment" OR abs:"water treatment plant" OR abs:"drinking water" OR abs:"residual chlorine") AND (abs:forecast OR abs:forecasting OR abs:prediction OR abs:"soft sensor")`
5. `(abs:"stream temperature" OR abs:"water temperature" OR abs:"lake temperature") AND (abs:forecast OR abs:prediction OR abs:"deep learning")`
6. `(abs:"water quality") AND (abs:LSTM OR abs:transformer OR abs:"graph neural" OR abs:"foundation model" OR abs:"transfer learning")`
7. `(abs:"water quality" OR abs:"dissolved oxygen" OR abs:salinity) AND (abs:"anomaly detection" OR abs:imputation OR abs:"missing data" OR abs:"early warning")`
8. `(abs:"water quality" OR abs:nitrate OR abs:"dissolved oxygen" OR abs:"stream temperature") AND (abs:"physics-guided" OR abs:"process-guided" OR abs:"knowledge-guided" OR abs:"differentiable")`
9. `(abs:"water quality" OR abs:"algal" OR abs:"dissolved oxygen") AND (abs:"probabilistic" OR abs:"uncertainty" OR abs:"ensemble forecast")`
10. `(abs:lake OR abs:reservoir OR abs:river) AND (abs:"benchmark dataset" OR abs:"foundation model") AND (abs:"water quality" OR ...)`

**OpenAlex（--oa）**
water quality forecasting deep learning time series；dissolved oxygen prediction river LSTM；harmful algal bloom forecasting chlorophyll-a machine learning；nitrate concentration forecasting high-frequency sensor river；stream water temperature prediction deep learning ungauged；wastewater treatment plant influent effluent forecasting machine learning；turbidity forecasting drinking water treatment plant；residual chlorine prediction water distribution network；cyanobacteria bloom early warning lake reservoir；water quality index prediction time series hybrid model；deep learning water quality prediction ungauged catchments transfer learning；phosphorus concentration prediction river machine learning time series；salinity forecasting estuary machine learning；groundwater quality nitrate time series prediction；lake water quality forecasting process-based model machine learning hybrid；hypoxia forecasting coastal bottom dissolved oxygen；suspended sediment concentration turbidity forecasting deep learning；water quality graph neural network spatiotemporal prediction monitoring stations；conductivity pH prediction river sensor data LSTM；sewer wastewater influent ammonia COD prediction deep learning；E. coli fecal bacteria beach water quality nowcasting；water quality sensor anomaly detection time series；deep learning for water quality review；stream temperature forecasting LSTM data assimilation reservoir release；algal bloom forecasting transformer attention reservoir；drinking water distribution chlorine decay machine learning forecasting；near-term ecological forecasting lake reservoir water quality ensemble；NEON forecasting challenge aquatics water temperature dissolved oxygen chlorophyll。

**单篇核验**：用 `abs <DOI>` 获取约 140 篇候选的完整摘要、作者与所有 OA 位置；arXiv 论文改用 `abs 10.48550/arxiv.<id>` 经 OpenAlex 取摘要（arXiv API 当时频繁 429）。

**未完成的查询（OpenAlex 429 限流，重试仍失败）**：time series foundation model water quality；conformal prediction water quality；dissolved organic carbon forecasting；temporal fusion transformer water quality；ConvLSTM chlorophyll satellite；aquaculture pond DO forecasting；water quality trend analysis；ocean acidification pH forecasting；China national monitoring stations；arXiv 标题组合查询。这些方向的覆盖可能偏弱（见第 4 节）。

## 2. 纳入/排除原则与主要排除记录

纳入：核心任务有时间依赖（预测/预警为主）；变量属于水质（溶解氧、营养盐、叶绿素/水华、水温作为水质变量、盐度/电导、浊度/透明度、微生物指标、余氯、出水水质）；有合法公开全文（arXiv、金色/混合 OA、PMC、机构库）；场景、方法、数据类型尽量分散。
限量收录：异常检测 1 篇（主列表）、插补 1 篇、因果/驱动分析 1 篇；综述 3 篇（主列表）+ 2 篇（备选）。预警类（9 篇）属于允许的核心任务。

主要排除：
- **早于窗口或首次公开日期存疑**：Willard et al. "Time series predictions in unmonitored sites: a survey…"（Environmental Data Science 2025，但 arXiv 2308.09766 为 2023-08，属旧文）；Rahmani et al. 2023 WRR（混合可微河流水温模型，可能有更早 ESSOAr 预印本，日期无法确认）；Barclay et al. 2023 WRR（过程引导水温，同样原因）；Wander et al. 2024 Ecosphere（ESSOAr 预印本 2023-05，早于窗口）；Savoy et al. 2023 WRR（河流叶绿素，正式在线日期接近窗口边界且无法确认）；Thorndahl et al. JEM（OpenAlex 日期恰为 2023-10-29，边界存疑）。
- **非水质/属于水文类**：径流、水位、洪水、地下水位、入库流量论文（如 TransGlow、各类 streamflow 迁移学习）全部排除；悬移质泥沙负荷类（Bezak 2025 等）偏泥沙水文，未收。
- **非时间预测**：饮用水可饮用性分类（water potability）、WQI 静态分类、遥感单景反演（如 Sentinel-2 叶绿素反演、HydroVision）、地下水砷空间 GNN、海草识别等。
- **方法过于平凡或同质堆叠**：大量 “分解（CEEMDAN/VMD）+ 优化算法 + LSTM/GRU” 的 DO/WQI 论文（Sci Rep、MDPI Water 等）仅保留 Pant 2024 作为备选代表；IoT 监测系统类、弱会议/低质量期刊（如 IJRITCC、Journal of Propulsion Technology 等）排除。
- **无摘要/无法核实**：SSRN 预印本（Ganda 地下水硝酸盐 conformal；Jang 余氯 conformal 预警）OpenAlex 无摘要，未收；Chazal 2024 贝类水域粪大肠菌短期预测无摘要，未收。
- **控制/优化而非预测**：污水厂强化学习控制、Koopman EMPC、泵站调度等排除。

## 3. 子方向覆盖表

| 子方向 | 主列表 rank | 备选 rank |
|---|---|---|
| 综述 | 2, 49, 50 | 51（框架）, 62 |
| 河流多参数/大尺度水质预测与可信度 | 3, 5, 14, 15 | – |
| 溶解氧（河流/湖泊/洪泛区） | 17, 19, 31 | 58, 59 |
| 近海/潟湖/养殖缺氧 | 9, 32, 33 | 53 |
| 营养盐（硝酸盐/总磷/氨氮/陆架海硝酸盐） | 7, 18, 20, 47 | 55, 64 |
| 叶绿素 a/藻华预测 | 6, 10, 13, 25, 26, 27, 30 | 56 |
| 藻华预警与早期预警统计 | 11, 28, 29 | 57 |
| 湖泊/水库生态近期预测（预测挑战、集合、基础模型） | 4, 8, 16 | 52 |
| 水温（河流/湖泊/寒区/气候情景） | 1, 12, 34, 35, 36 | 54 |
| 盐度/电导率 | 23, 24 | – |
| 透明度/浊度/悬浮物 | 48 | 63 |
| 微生物指标（海滩 FIB、河流大肠杆菌） | 43, 44 | – |
| 供水：水厂与管网余氯 | 22, 37, 38, 39, 40 | 60 |
| 污水处理出水/工艺 | 21, 41, 42 | 61, 65 |
| 地下水水质 | 46 | – |
| 异常检测 / 插补 | 45（异常）、20（插补/趋势重建） | 61（插补） |

方法覆盖：统计（INLA 时空、ARIMA/TFARIMA、高斯过程代理、早期预警统计、贝叶斯异常检测）；机器学习（XGBoost、RF、LightGBM、梯度提升全局模型）；深度学习（LSTM、TFT、N-BEATS、patch/通道独立架构、GAT/RGCN/DCRNN、扩散模型）；基础模型（LakeFM、Chronos/Lag-Llama）；物理-数据融合（过程引导、PINN、机理后报训练 AI、ML 产品同化进业务动力模型、多模型集合）；迁移学习（跨流域、河流→洪泛区、海滩间、无资料流域）。
数据类型：高频传感器/浮标（6, 7, 25, 30, 45）、低频人工采样/监管站网（5, 14, 15, 44, 46, 48）、遥感（11, 56, 57, 63）、模拟情景（9, 36）。
地区：美国、瑞士、西班牙、中国、日本、巴西/欧洲、新西兰、加拿大、意大利、比利时、塞尔维亚、英国、哥伦比亚、北海/西北欧陆架。

**明显缺口**：
- 管网余氯短期在线预测与水厂进水浊度预测的高质量 OA 论文偏少（多为 MDPI/弱期刊）；
- 地下水水质时间预测几乎没有高质量论文（仅收 1 篇趋势/政策分析）；
- pH/海洋酸化、溶解有机碳、水产养殖池塘水质等方向因 OpenAlex 限流未完成检索；
- 中国国控断面大规模时空预测仅收 L-GAT 与 Zheng 2025，同类 MDPI 文章很多但质量参差，未扩展；
- 概率预测/保形预测（conformal）在水质中的应用仅见 SSRN 无摘要预印本，未能收录。

## 4. 优先阅读 10 篇

1. rank 1 Padrón 2025 HESS — 可业务化的 32 天概率水温预报（TFT，CRPS 评估，新站外推）。
2. rank 4 Olsson 2025 — 10 万条真实前瞻水温/溶解氧预报与零模型对比，最可信的评测证据。
3. rank 5 Tavares 2026 — 与持续性基线比较并做跨洲零样本迁移，结论审慎。
4. rank 3 Xia 2025 — 482 流域 20 变量的深度模型可信度系统评估。
5. rank 10 Yu 2026 — 通用时序架构（patch、通道独立、跨变量注意力）与生态时间尺度的对应关系。
6. rank 8 LakeFM 2026 — 面向湖泊不规则多深度数据的基础模型。
7. rank 13 Matsushita 2026 — Chronos/Lag-Llama 在长期月度湖泊数据上与 15 种方法对比（预印本）。
8. rank 11 Schaeffer 2023 — 全美湖库蓝藻周预警，INLA 时空模型胜过深度模型。
9. rank 9 Ou 2025 — 机理模型后报训练 AI 的近海缺氧日预报。
10. rank 41 Vukmirović 2026 — 污水厂预测与朴素基线严格比较，揭示插值日评估造成的虚高。

## 5. 扩展领域建议

- **水生生态/近期生态预测（ecological forecasting）**：NEON/EFI 预测挑战、FLARE 系统、多模型集合，文献量充足，可独立成类或作为水质子类。
- **水处理过程工业（污水厂/水厂）软测量与数字孪生**：与“工业与设备”交叉，arXiv 上 Simethy、Mohammadi 等数据集/模拟器论文较多。
- **海洋生物地球化学预报（缺氧、营养盐、浮游植物同化）**：与气象海洋业务预报交叉，可单独收集。
- **遥感水质时间序列（CyAN、Sentinel-2/3）**：介于反演与预测之间，可作为遥感专题。

## 6. 无法核实或存疑条目

- rank 2 Zhi 2024 Nature Water：OpenAlex 无摘要，summary 只依据标题/元数据；内容范围待全文核实。
- rank 4 Olsson 2025、rank 58 Granata 2024：OpenAlex 日期只到年（YYYY-01-01），精确在线日期待核实（均在窗口内）。
- rank 1、46、50（HESS）与 rank 26（ESS Open Archive v3）：可能存在更早的讨论稿/预印本，具体日期未核实，但推断仍在窗口内。
- rank 6 Fournier、rank 37 Janjua：期刊在线早于 arXiv v1，first_public_date 取更早的期刊日期，date_source 已注明。
- rank 34 Chang：取 OpenAlex 中 2024-09-27 预印本记录为首次公开日期（标题略不同），正式刊 2025-05-29。
- PDF 链接：rank 15（Water Research X 金色 OA）OpenAlex 未给 PDF 直链，pdf_candidates 为空，需协调人从 DOI 落地页解析；rank 19（WRR pdfdirect）、rank 33（Frontiers /pdf；OpenAlex 原给出的是无关 FRDC 报告链接）、rank 41（MDPI /pdf）为按出版社规则构造的链接，未经核验。rank 31 Sadler、rank 53 Zheng 为 bronze OA（出版社免费阅读），可下载性待核实。
- rank 13、28、49 为预印本（bioRxiv/EarthArXiv），未经同行评审。
- MDPI 期刊在主列表中共 4 篇（rank 38、29、41、44），均因设计/场景独特而保留。
- 数量说明：已达到 65 条（50+15），但第 1 节所列若干查询因 OpenAlex 限流未完成，部分方向覆盖不足。
