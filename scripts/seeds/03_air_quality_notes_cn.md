# 03_air_quality（空气质量）检索与筛选笔记

检索日期：2026-10-29；时间窗：首次公开日期 2023-10-29 至 2026-10-29。
产出：`03_air_quality_seed_cn.json`，共 65 条（主表 1-50，备选 51-65）。主表中近期文献 49 条，旧文献 1 条（第 50 条 PM2.5-GNN）；备选 15 条全部为近期文献。

## 1. 检索词与平台（实际使用）

### arXiv（`scripts/search_candidates_en.py arxiv`，自动按窗口过滤）
1. `(abs:"air quality" OR abs:"PM2.5") AND (abs:forecasting OR abs:prediction)` -n 40
2. `(abs:"air pollution" OR abs:ozone OR abs:"nitrogen dioxide") AND abs:forecast` -n 40
3. `(abs:"air quality" OR abs:pollutant OR abs:PM2.5) AND (abs:graph OR abs:"graph neural")` -n 30
4. `(abs:"low-cost sensor" OR abs:"low cost sensor") AND (abs:PM2.5 OR abs:"air quality")` -n 25
5. `(abs:ozone OR abs:O3) AND (abs:"deep learning" OR abs:"machine learning") AND abs:forecast` -n 25
6. `(abs:"air quality" OR abs:"PM2.5" OR abs:aerosol) AND (abs:"foundation model" OR abs:"large language model")` -n 25
7. `(abs:"air quality" OR abs:PM2.5 OR abs:smoke) AND (abs:probabilistic OR abs:uncertainty OR abs:conformal OR abs:quantile)` -n 30
8. `(abs:"wildfire smoke" OR abs:"dust storm" OR abs:haze) AND (abs:forecast OR abs:prediction)` -n 25
9. `(abs:"chemical transport model" OR abs:CMAQ OR abs:"WRF-Chem" OR abs:CAMS OR abs:GEOS-Chem) AND (abs:emulator OR abs:"deep learning" OR abs:"bias correction")` -n 30（结果大多被“CAM”类 XAI 论文污染，实际用处小）
10. `(abs:satellite OR abs:TROPOMI OR abs:AOD) AND (abs:PM2.5 OR abs:NO2) AND (abs:forecast OR abs:"spatiotemporal")` -n 25
11. `(abs:aerosol OR abs:"atmospheric composition" OR abs:"air quality") AND (abs:"machine learning" OR abs:"data-driven" OR abs:transformer) AND (abs:"medium-range" OR abs:global OR abs:ECMWF)` -n 25
12. `(abs:"air quality" OR abs:PM2.5 OR abs:pollution) AND (abs:nowcasting OR abs:"early warning" OR abs:exceedance OR abs:episode)` -n 25

### OpenAlex（`openalex ... --oa`，窗口内）
1. machine learning surface ozone forecast bias correction chemical transport model
2. deep learning PM2.5 forecast China air quality model operational
3. graph neural network air quality forecasting monitoring stations
4. wildfire smoke PM2.5 forecast machine learning
5. dust storm forecast deep learning
6. air quality forecasting Africa low-cost sensors machine learning
7. NO2 forecast satellite TROPOMI machine learning
8. ozone exceedance early warning prediction
9. air pollution episode heavy haze prediction deep learning
10. air quality forecast Europe CAMS machine learning post-processing
11. air quality time series foundation model zero-shot forecasting
12. review deep learning air quality forecasting
13. seasonal prediction haze PM2.5 winter climate predictability
14. 标题检索：Transferable Hourly Ozone Forecasting with Transformers；Expert-Guided Cross-Model Transfer Learning for Accelerating Operational PM2.5 Forecasting

### 全文摘要核实
- 对全部候选用 `abs` 取完整摘要与 OA 位置。arXiv API 在批量 `abs` 时持续返回 429（多代理共享 IP），因此改为用 OpenAlex 查询 arXiv DOI（`10.48550/arXiv.<id>`），只访问 api.openalex.org；arXiv v1 日期取自前面 arXiv 检索结果列表中的 `v1=` 字段。
- WebSearch（仅用于发现/补证，共 5 次）：ML 臭氧偏差订正 GMD；全球气溶胶 AI 预报（发现 AI-GAMFS、AIFS-COMPO 线索）；AirPhyNet/Air-DualODE 会议信息；Copernicus 讨论稿编号日期（未找到）；PM2.5-GNN arXiv v1 日期与完整标题。

## 2. 纳入/排除原则与主要排除记录

纳入原则：
- 核心任务涉及时间依赖（预报/预警/时间序列分析），以预测为主；主表 50 条中预测 42、预警 2、基准/数据集 2、综述 4；非预测类（因果、临界信号分析）只放在备选。
- 方法上避免同质堆叠：同一城市 + LSTM/CNN-LSTM/GRU 的应用论文一律不收；同类站点网络 GNN 只保留在物理先验、偏差订正、未来协变量、极值建模等方面各有特点的代表。
- 覆盖：污染物（PM2.5、PM10、O3、NO2、CO、沙尘/气溶胶、能见度）；区域（中国、印度、韩国、日本、欧洲德/意/瑞典/罗马尼亚、英国、美国、墨西哥、哥伦比亚、乌干达、非洲五城、澳大利亚、全球）；时间尺度（小时临近、1-6 天、次季节 10-30 天、季节、气候情景）；数据源（监测站、低成本/移动传感器、卫星 Sentinel-5P/MODIS/AOD、再分析 CAMS/ERA5、CTM 输出、交通数据）。
- 只收有合法公开全文的条目（arXiv、Copernicus/MDPI/Frontiers/PLOS/Nature OA、Wiley OA、PMC、机构库）。

主要排除记录：
- 早于时间窗的知名文献（不收）：AirFormer（AAAI 2023, arXiv 2211.15979）、Group-Aware GNN（TKDD 期刊版 OpenAlex 日期 2023-11-04，但 OpenAlex 记录 W3197700565 为 2021 年收录，首次公开应早于窗口）、Liu 等 2022 ACP 深度学习订正化学-气候模式臭氧。PM2.5-GNN（2020）作为唯一旧文献保留（经典基线/数据集）。
- Riccio 等 2024 ACP「Technical note: ... improving CAMS using a novel statistical post-processing method」：期刊上线 2024-02-06，但有 EGUsphere 讨论稿 egusphere-2023-1015，按编号推断约在 2023 年年中公开，首次公开日期很可能早于窗口，排除。
- Mao 等 2024 ACP（中国多年代臭氧趋势，CTM+ML）与 Gouldsbrough 等 2024 ACP（EMEP4UK 降尺度）：同样有 2023 年 EGUsphere 讨论稿（egusphere-2023-1052、egusphere-2023-632），且以趋势重建为主，排除。
- Vicente 等 2023-11 Atmospheric Pollution Research（加泰罗尼亚高浓度臭氧事件）：OpenAlex 无摘要，无法按摘要标注，排除。
- arXiv 2402.06574（PM10 ARBX(1)）：期刊版 2019 年已发表，arXiv 只是后传，属旧文献，排除。
- 已撤回/作者声明有问题：GraphSVR（2605.03795，提交者撤回）、DTW-CNN-GRU 长期预报（2510.22863，作者撤稿修改）、Cork NO2（2507.04196，作者称提交过早）、EmissionNet（2507.05416，附图错标）。
- 方法平凡或同质：CNN-LSTM PM2.5（2508.11215）、Bucharest（2511.00532）、Nigeria Prophet vs LSTM（2508.16244）、Tehran/Macau/Shanghai 等单城 DL 对比、印度若干 AQI 预测期刊、QHAdamW ANN（IJETT）、多篇低水平综述（IJAE、IJARCCE 等）。
- 偏离时间序列核心：低成本传感器校准（Veli 2508.02724、XGBoost 现场校准 2506.15840、GWR 校准 2510.05646、Ravindra npj CAS 2024）、静态制图/估计（卫星 NO2 地面估计、NO2 欧洲高分辨率地图 2609.24634、Bayesian 伦敦月均融合 2506.10688）、图像/天空照片估计、LLM 聊天界面（VayuBuddy、VayuChat）、极地臭氧耗损事件 NWP 可预报性（2410.11592，属平流层/边界层臭氧化学与天气，非空气质量）。
- 留作后备但未入表（质量尚可）：Neural CDE-GAT（Sci Rep 2026，仅北京 5 站）、MSDGNN（PLOS ONE 2025）、MVG-KAN（2606.24347）、AirFlow（2608.09775）、HEART 马德里（2502.19042）、AirCade（ICASSP 2025, 2505.20119）、离线耦合全球模型（2503.18405，与 MVAR 同组）、AirMPA（2610.25797）、AQ-Net（2502.11941，无摘要）、跨分辨率注意力（2603.11725，与 TopoFlow 同组）、SPIN 归纳克里金（2511.16013）、KNN-SINDy 插补（2409.11640）、Expert-guided UFS-AQM 迁移（ESSOAr 预印本）、Hubei 冬季 PM2.5 季节预测（MDPI Atmosphere 2025）、Iasi 以外的 SEA 城市概率预警（Jurnal RESTI，期刊较弱）、npj Clean Air 观点文（Wang 等 2026，十个方向）。

## 3. 子方向覆盖表

| 子方向 | 主表 rank | 备选 rank |
|---|---|---|
| 全球/区域格点 AI 预报（含基础模型、业务系统） | 1, 2, 3, 6, 7, 8 | 63 |
| 概率/集合/生成式预报 | 4, 5, 20 | 57 |
| 物理引导站点网络时空模型（GNN/Neural ODE/算子） | 9, 10, 11, 12, 33 | 52 |
| CTM 后处理/偏差订正/替代模型 | 13, 14, 34, 35 | 54, 55, 56, 62, 65 |
| 极端事件与超标预警 | 16, 17, 18, 19, 20, 41 | 64 |
| 野火烟雾 | 20, 21, 22 | 61 |
| 沙尘/气溶胶 | 3, 23, 24, 43 | 65 |
| 次季节与季节可预报性 | 25, 26 | 53 |
| 基准/数据集/评测协议 | 27, 28, 29, 21 | — |
| 时序基础模型与 LLM | 1, 27, 29, 30 | 63 |
| 外生变量设计（未来协变量、多层气象、交通） | 31, 32, 45 | 51, 59 |
| 低成本/移动传感器序列 | 37, 38, 39 | — |
| 室内空气质量 | 40, 49 | 58 |
| 不同污染物：O3 / NO2 / CO / 能见度 | O3: 4, 15, 46；NO2: 31；CO: 42；能见度: 35, 43 | O3: 56, 57 |
| 非中国区域（欧、美、拉美、非洲、南亚、日韩、澳） | 12-16, 19-22, 26, 29, 33, 36, 37, 41, 44, 45 | 59 |
| 统计方法（GP、EVT、贝叶斯层次、集合加权） | 16, 19, 20, 26, 37, 45 | 53, 60, 61, 64, 65 |
| 综述 | 46, 47, 48, 49 | — |
| 经典基线（旧） | 50 | — |

明显缺口：
- 卫星融合的短期预报只有备选 59 一条较弱的会议论文；卫星多用于静态估计，窗口内高质量的“卫星驱动预报”较少。
- SO2 没有专门条目（只在多污染物条目中出现）。
- 健康关联（污染→就诊/入院预测）未收：检索到的 2607.17024 用周度国家级数据做嵌套交叉验证，时间依赖弱，未纳入；如需要可单独检索医疗交叉方向。
- 共形预测只在 E-STGCN 中作为附带部分；专门的空气质量共形预测论文在窗口内未找到高质量候选。

## 4. 优先阅读 10 篇

1. rank 1 Aurora（Nature）——地球系统基础模型在空气质量预报上超过业务系统，代表范式转变。
2. rank 2 AIFS-COMPO——ECMWF 业务路线的数据驱动成分预报，与 CAMS IFS-COMPO 直接对比。
3. rank 4 AirFusion——扩散模型做 30 成员臭氧集合预报，并量化天气不确定性。
4. rank 5 Foehn——全球公里级概率 PM2.5 预报，校准集合与提前 4 天极端探测。
5. rank 9 AirPhyNet——物理引导站点网络模型的常用基线（ICLR）。
6. rank 16 E-STGCN——极值理论 + 图网络 + 共形区间，统计期刊发表。
7. rank 20 HAQES（BAMS）——多机构野火空气质量集合预警，统计加权提升命中率、降低虚警。
8. rank 28 AirQualityBench——保留原生缺测的全球评测，揭示“干净数据集”上的优势不可迁移。
9. rank 29 Cost-aware TSFM 评测（Sci Rep）——揭示未来协变量泄漏造成的伪优势，并给出成本维度。
10. rank 46 Hickman 等 GMD 综述——TOAR 视角下臭氧 ML 全景与挑战。

## 5. 扩展领域建议

- 大气成分数据同化与 AI（学习式同化、EnKF 变体、卫星同化 TEMPO/GEMS）：本领域只收了 D-DNet 与 VTS-EnKF，内容足以单独成类。
- 野火（火辐射功率、火蔓延）预测：检索中出现 GNN 全球 FRP 中期预测（2610.11022）、FIRA 火蔓延模型（GeoHealth 2025），与烟雾预报衔接，可独立收集。
- 能见度/雾霾气象预报：与空气质量交叉，可归入气象与气候。
- 排放清单的近实时估计与反演（电厂日排放 2604.06661、TROPOMI 排放反演）：属于时间序列反演问题，可作为独立方向。
- 健康影响预测（污染→呼吸道/心血管就诊）：建议在“医疗与公共卫生”下专门检索。

## 6. 无法核实或存疑条目说明

- rank 50 PM2.5-GNN：旧文献；arXiv v1 日期 2020-02-10 来自 WebSearch 看到的 arXiv 页面信息，因 arXiv API 限流未用助手复核。
- rank 65 VTS-EnKF（GMD 2024）：存在 GMD 讨论稿 gmd-2023-219，公开日期未能核实，可能早于 2023-10-29；如核实早于窗口，应从备选中删除。
- rank 36 阿布拉谷（ASCMO 2023-12-22）：OpenAlex 未列出讨论稿位置；ASCMO 通常有讨论阶段，若讨论稿早于窗口应降为旧文献或删除。
- rank 15 Transferable Hourly Ozone（EGUsphere 2026）：仍为公开评审中的预印本，尚未正式接收。
- rank 49（Indoor Air 综述）与 rank 62（AI-Air）：OpenAlex 日期为年份首日占位（2026-01-01 / 2025-01-01），具体上线日待核实，但均在窗口内。
- rank 41（Sustainable Cities and Society，Elsevier 混合 OA）：OpenAlex 给出 sciencedirect PDF 链接，可能需要浏览器验证；如下载失败可用备选替换。
- rank 29、43 的 Scientific Reports PDF：OpenAlex 给出的是 `_reference.pdf` 链接，已同时列出标准 `nature.com/articles/<id>.pdf` 地址（rank 43 另有 PMC PDF）。
- rank 8 TopoFlow：arXiv 注释称已被 npj Climate and Atmospheric Science 接收，期刊 DOI 未在 OpenAlex 中见到。
- rank 10 Air-DualODE：网上有 ICLR 录用说法，但未见官方列表，venue 按 arXiv 预印本记录。
- rank 37 Kampala：摘要只说 AirQo 传感器网络，未明确污染物，目标写为“待全文核实”。
- 若干 arXiv 条目（如 rank 39 WaveCatBoost）期刊版题名与 arXiv 题名不同，表中使用 arXiv 题名并在 venue 中注明期刊版题名。
