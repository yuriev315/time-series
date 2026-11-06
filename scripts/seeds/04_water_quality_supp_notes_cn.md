# 04_water_quality（水质）补充候选笔记（rank 66–90）

检索日期：2026-10-29；时间窗：首次公开 2023-10-29 至 2026-10-29。
背景：首批 65 条（`04_water_quality_seed_cn.json`）只得到 42 篇已核验全文，主要原因是 Wiley/AGU、ACS、PNAS、Elsevier 等出版社拦截自动下载。本批补充 25 条，**全部为近三年文献（old = 0）**，并按 arXiv id、DOI、标准化标题与首批 65 条比对，无重复；同时与其他领域 seed 文件及 `registry_cn.json` 比对，也无重复。

## 1. 全文路线约束（本批执行情况）

只收全文来自以下主机的论文：arXiv（14 篇）、Nature OA（Nat Commun、Sci Rep、npj Clean Water，共 4 篇）、Copernicus ESSD（1 篇）、Frontiers（3 篇）、Springer Open（Applied Water Science，1 篇）、MDPI（2 篇，择优使用）。
- 2 篇 arXiv 论文（rank 76、85）的正式版在 Elsevier（Harmful Algae、Environmental Research），但 arXiv 版可直接获取，pdf_candidates 留空，由协调者按 arXiv id 下载。
- Thames 溶解氧（rank 71）同时给出 Nature PDF、arXiv 与 KIT 机构库三条路线。
- Frontiers 的 3 篇 OpenAlex 未给 pdf_url，按 Frontiers 官网标准 PDF 链接格式填写（`.../articles/<DOI>/pdf`），rank 77 另有 sapientia.ualg.pt 机构库链接。Applied Water Science 同理，用 `link.springer.com/content/pdf/<DOI>.pdf`。
- 未收任何只能经 Wiley/AGU、ACS、PNAS、RSC、AMS、ScienceDirect、PMC、ResearchSquare、ESS Open Archive 获取的论文。

## 2. 检索词与平台（实际执行）

**arXiv（scripts/search_candidates_en.py arxiv）**
1. `(abs:"water quality" OR abs:"dissolved oxygen") AND (abs:forecasting OR abs:forecast OR abs:prediction)`
2. `(abs:"harmful algal" OR abs:cyanobacteria OR abs:chlorophyll OR abs:"algal bloom") AND (abs:forecast OR abs:forecasting OR abs:"early warning")`
3. `(abs:"water temperature" OR abs:"stream temperature" OR abs:"lake temperature") AND (abs:forecast OR abs:prediction) AND (abs:lake OR abs:river OR abs:stream)`
4. `(abs:"water quality" OR abs:turbidity OR abs:nitrate OR abs:phosphorus OR abs:salinity OR abs:conductivity OR abs:"fecal") AND (abs:"time series" OR abs:forecasting OR abs:LSTM OR abs:transformer)`
5. `(abs:aquaculture OR abs:"fish farm" OR abs:pond) AND (abs:"dissolved oxygen" OR abs:"water quality" OR abs:ammonia) AND (abs:forecast OR abs:prediction)`
6. `(abs:wastewater OR abs:"sewage" OR abs:"treatment plant") AND (abs:forecast OR abs:forecasting) AND (abs:influent OR abs:effluent OR abs:quality OR abs:ammonia OR abs:nitrogen)`
7. `(abs:"drinking water" OR abs:chlorine OR abs:"water distribution") AND (abs:forecast OR abs:"time series") AND abs:quality`
8. `(abs:"Escherichia coli" OR abs:"E. coli" OR abs:enterococci OR abs:"fecal indicator" OR abs:"bathing water" OR abs:"beach") AND (abs:forecast OR abs:prediction OR abs:nowcast) AND abs:water`
9. `(abs:groundwater) AND (abs:nitrate OR abs:salinity OR abs:"water quality" OR abs:arsenic) AND (abs:forecast OR abs:"time series" OR abs:prediction)`
10. `(abs:estuary OR abs:"saltwater intrusion" OR abs:"salt intrusion" OR abs:hypoxia OR abs:"ocean acidification") AND (abs:forecast OR abs:forecasting OR abs:"machine learning")`
11. `(abs:"suspended sediment" OR abs:turbidity OR abs:"dissolved organic carbon") AND (abs:forecast OR abs:"deep learning" OR abs:LSTM)`
12. `ti:"water quality"`；`ti:"dissolved oxygen"`
13. `(ti:lake OR ti:reservoir OR ti:river OR ti:stream) AND (ti:forecast OR ti:forecasting OR ti:predicting OR ti:prediction) AND (abs:nutrient OR abs:phosphorus OR abs:nitrogen OR abs:oxygen OR abs:phytoplankton OR abs:temperature OR abs:salinity)`
14. `(abs:phytoplankton OR abs:eutrophication OR abs:"red tide") AND (abs:forecast OR abs:forecasting OR abs:"time series")`
15. `(abs:salinity OR abs:"specific conductance" OR abs:chloride) AND (abs:river OR abs:estuary OR abs:delta) AND (abs:forecast OR abs:"deep learning" OR abs:LSTM)`
16. `(abs:"water quality") AND (abs:spatiotemporal OR abs:spatio-temporal OR abs:graph) AND (abs:forecasting OR abs:prediction)`
17. `(abs:"total phosphorus" OR abs:"ammonia nitrogen" OR abs:"permanganate" OR abs:"chemical oxygen demand") AND (abs:forecast OR abs:forecasting OR abs:prediction)`

**OpenAlex 检索**：`water quality forecasting deep learning river dissolved oxygen`、`algal bloom forecasting early warning lake`、`water quality forecasting`（--title）、`dissolved organic carbon forecasting`（--title）全部返回 HTTP 429（本次会话 OpenAlex 检索端点持续限流，多次重试仍失败）。OpenAlex 单篇查询（`abs <DOI>`）正常，因此改为：**用 WebSearch 发现 → 用 `abs <DOI>` 或 `abs 10.48550/arxiv.<id>` 逐篇核验日期、摘要和 OA 位置**。arXiv API 中途也出现过 429，部分 arXiv 摘要改经 OpenAlex 获取。

**WebSearch（仅用于发现，共 18 次；因 OpenAlex 检索限流而多于常规）**：Copernicus（HESS/BG/GMD/ESSD/OS）水质预测（2 次）；HESS 硝酸盐/DOC/泥沙 LSTM；nature.com 水质时间序列预测；Frontiers/PLOS/IOP/Springer 有害藻华预测；npj Clean Water 污水预测；Frontiers Marine Science 藻华/缺氧/pH；养殖池塘溶解氧；海洋酸化 pH 预测；水厂原水浊度/余氯预测；海滩 E. coli/肠球菌预报；地下水硝酸盐时间序列；Copernicus 湖泊业务预报；Sci Rep 藻华预警；水质保形预测/概率预测；咸潮上溯预测；ERL 河流水质；河流浊度预报。

## 3. 纳入/排除原则与主要排除记录

纳入标准与首批相同（核心任务有时间依赖、预测/预警优先、变量属于水质、合法公开全文）；此外优先补充首批笔记列出的缺口：pH、地下水、养殖、供水余氯短期预测、微生物/病毒、咸潮、海洋生物地球化学。

主要排除：
- **与首批近重复**：2602.05178 "Benchmarking AI Models for Daily Coastal Hypoxia Forecasting"（与首批 rank 9 Ou 等同一团队，用的是同一墨西哥湾后报数据）；2403.18923 MCES 湖泊溶解氧特征选择（与首批 rank 17 同一团队、同一湖泊数据）；2505.01948 MSGL 河流水温降尺度（河流水温方向已饱和）。
- **早于窗口**：HESS 27/3823/2023 Rhine–Meuse LSTM 咸潮预报（2023 年初）；Frontiers 2023 藻华/贝毒机器学习综述（fmars.2023.1127649）；npj Clean Water 2021 难民营余氯预测；2402.09271/2402.09266（arXiv 2024 上传，但正式版分别于 2023、2022 已发表，属旧文）。
- **非时间预测或偏离水质**：饮用水可饮用性分类（Applied Water Science s13201-026-02817-x、2607.15775）、沉淀水浊度静态回归（Frontiers fenve.2024.1401180）、Poyang 流域空间回归（MDPI w17162496）、Sentinel-2 叶绿素/浊度单景反演（2510.09736、2401.03792）、地下水砷空间 GNN（2607.19392）、加州海流溶解氧极值统计（2408.12287，以空间分布为主）、ESSD 全球 pH 三维重建（essd-17-719-2025，开放大洋格点产品）；泥沙浓度时空格局（HESS 29/2975，偏泥沙水文）；DOC 输出分析（HESS 29/2377）。
- **方法过弱或来源不宜**：Sci Rep s41598-025-03612-5（单作者、指标表述混乱）；MDPI Water w16243547（IPSO-CNN-GRU-TAM 同质堆叠）；2401.01491（作者注明内容需完善）；2411.01527、2409.10898 等 WQI 静态分类/对比。
- **领域不明确**：2503.04981 河网保形预测（摘要未说明真实数据是否为水质）。
- **趋势分析，enum 无对应任务类型**：Frontiers fmars.2026.1873334 ALOHA 站 pH 长记忆/趋势分析（pH 方向有价值，但属于纯趋势与持续性分析，未收；如需补 pH 可作为后备）。

## 4. 本批新增的子方向覆盖

| 子方向 | rank |
|---|---|
| 藻华早期预警（微生物分子指标） | 66 |
| 湖泊水质基准数据集 | 67 |
| 降雨驱动的河流水质预测 / 河网时空预测 | 68, 78 |
| 湖泊水温 + 溶解氧（检索增强迁移） | 69 |
| 海洋生物地球化学/浮游植物预报（仿真器、全球格点） | 70, 82 |
| 河流溶解氧（超统计 + Transformer） | 71 |
| 河口咸潮上溯预报（供水安全） | 72 |
| 供水系统多节点余氯 3 小时预测 | 73 |
| 污水厂水质 24 小时预测 / N2O 高频数据集 | 74, 86 |
| 近海有毒甲藻与贝毒预测/预警 | 75, 76, 77 |
| 河流水温跨区域泛化 | 79 |
| 污水病毒（病原体）预测 | 80 |
| 地下水硝酸盐 / 地下水盐化 | 81, 89 |
| 河口叶绿素 a 卫星序列预测 | 83 |
| 水库分层水温（可解释 KAN） | 84 |
| 亚热带水库叶绿素 a 驱动与机理模型 | 85 |
| 综述：遥感 + AI 河流水质预测 | 87 |
| 养殖水体溶解氧 | 88 |
| 地表水 pH/电导/溶解氧/水温长期时空外推 | 90 |

任务类型：预测 17、预警 3、基准/数据集 2、因果/驱动分析 2、综述 1。
方法：统计/机理（种群动态、EOF、超统计、动态水文-生态模型）、机器学习（RF、XGBoost、LightGBM、DoME、流式学习）、深度学习（LSTM、GRU、N-BEATS、Informer、UNet、ConvLSTM、图神经网络）、物理-数据融合（物理一致性检索、物理信息 CNN 仿真器）、可解释（SHAP、KAN 符号回归）、终身学习、双重机器学习。
水体与地区：湖泊（美国中西部、全美 21 湖）、水库（美国 Red River、华南）、河流（泰晤士河、美国东海岸、阿拉巴马）、河口（珠江磨刀门、黑海）、近海（亚得里亚海、伊比利亚/葡萄牙）、全球海洋、陆架海一维水柱、供水管网（中国）、污水厂（法国、沙特、丹麦）、地下水（以色列、阿拉巴马）。

**仍存在的缺口**：pH/海洋酸化预测（只有趋势分析类）；溶解有机碳（DOC）预测；水厂原水浊度短期预报；中国国控断面大规模时空预测的高质量 OA 论文；保形预测/概率预测在水质中的应用。这些方向在允许主机内未找到合格的近三年论文，或 OpenAlex 检索限流导致未能系统检索。

## 5. 优先阅读（本批）

1. rank 66 Mudge 2025 Nat Commun：宏蛋白质组时间序列提前 24 小时以上预示藻华，是全新的预警数据源。
2. rank 67 LakeBeD-US 2025 ESSD：21 湖、17 变量、5 亿条观测的公开基准。
3. rank 70 Skakala 2026：机理模型仿真器从 10 天到年代际，再分析训练后预报技巧超过母模型。
4. rank 68 RaiNet 2025：降雨-水质滞后建模并公开多模态数据集。
5. rank 69 PIER 2026：物理一致性检索增强，356 湖 41 年。
6. rank 72 Tian 2024：咸潮滞后归因与 1–3 天预报。
7. rank 75/77：同一种有毒甲藻的机器学习（流式 vs 批量）与机理种群模型预警，适合对照阅读。

## 6. 存疑或需全文核实的条目

- rank 67、71、83：首次公开日期取正式刊 OpenAlex 日期，另有 ESSD 讨论稿或 Research Square 预印本，日期更早但都在窗口内。
- rank 83 Black Sea（Sci Rep 2026）：OpenAlex 给出的 pdf_url 是 `_reference.pdf`，本文件改填标准 `.pdf` 链接，需下载时确认。
- rank 89 以色列地下水盐化：摘要侧重驱动/因果分析，时间维度如何建模（LSTM 输入）需全文核实。
- rank 90 加州 70 年：未来 50 年外推的验证方式需全文审视。
- rank 88 GRU–N-Beats：数据来源、预测步长摘要未给出。
- 所有标注“待全文核实”的字段（频率、预见期、切分方式等）摘要中未给出。
