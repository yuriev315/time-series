# 08_transport（交通与出行）检索与筛选笔记

检索日期：2026-10-29；时间窗：首次公开 2023-10-29 至 2026-10-29（有 arXiv 版本者以 arXiv v1 为准）。
结果：`08_transport_seed_cn.json` 共 65 条，其中主列表 1-50、备选 51-65。主列表近期 47 条，早期 3 条（94%）；备选 15 条全部为近期。
所有条目的字段都只依据 arXiv API 返回的摘要、comment 和 journal_ref 填写，未读全文，未知项写“待全文核实”。

## 1. 检索词与平台（实际使用）

平台：arXiv API（经 `scripts/search_candidates_en.py`）；OpenAlex（同一脚本，但本次全程返回 HTTP 429，没有拿到任何结果）；WebSearch 2 次，仅用于发现线索。

arXiv 查询（`arxiv` 子命令，日期由脚本自动过滤）：
1. `(ti:traffic AND (ti:forecasting OR ti:prediction)) AND cat:cs.LG`
2. `(ti:traffic AND (ti:"large language model" OR ti:LLM OR ti:"foundation model"))`
3. `(abs:"spatio-temporal" OR abs:spatiotemporal) AND (ti:"foundation model" OR ti:"universal" OR ti:"pre-trained" OR ti:"prompt") AND abs:traffic`
4. `(ti:benchmark OR ti:dataset) AND (ti:traffic OR ti:spatiotemporal OR ti:"spatio-temporal")`
5. `(abs:PeMS OR abs:"METR-LA" OR abs:LargeST) AND (ti:rethinking OR ti:revisiting OR ti:simple OR ti:baseline OR ti:benchmark OR ti:evaluation OR ti:pitfalls OR ti:"really")`：返回结果与主题基本无关
6. `(abs:traffic) AND (ti:probabilistic OR ti:uncertainty OR ti:conformal OR ti:diffusion) AND (ti:forecasting OR ti:prediction)`
7. `(ti:"bike sharing" OR ti:"bike-sharing" OR ti:"ride-hailing" OR ti:taxi OR ti:"ride-sourcing" OR ti:"micromobility") AND (ti:demand OR ti:forecasting OR ti:prediction)`
8. `abs:traffic AND (abs:"spatio-temporal" OR abs:spatiotemporal) AND (abs:"data leakage" OR abs:"evaluation protocol" OR abs:"fair comparison" OR abs:"overestimate" OR abs:"simple baseline" OR abs:"do we really need")`
9. `(ti:XXLTraffic OR ti:LargeST OR abs:"extremely long") AND abs:traffic`
10. `abs:traffic AND (abs:"time series foundation model" OR abs:"zero-shot") AND (abs:Chronos OR abs:TimesFM OR abs:Moirai OR abs:"Lag-Llama")`
11. `(ti:metro OR ti:subway OR ti:"rail transit" OR ti:"public transport" OR ti:transit OR ti:bus) AND (ti:"passenger flow" OR ti:ridership OR ti:demand OR ti:"origin-destination" OR ti:forecasting OR ti:prediction)`
12. `(ti:flight OR ti:airport OR ti:"air traffic" OR ti:airline OR ti:railway OR ti:train) AND (ti:delay OR ti:demand OR ti:passenger OR ti:forecasting) AND (abs:"time series" OR abs:forecasting)`
13. `(ti:port OR ti:vessel OR ti:ship OR ti:container OR ti:freight OR ti:logistics) AND (ti:arrival OR ti:throughput OR ti:volume OR ti:demand) AND (ti:forecasting OR ti:prediction)`
14. `(ti:"travel time" OR ti:ETA OR ti:"arrival time") AND (ti:prediction OR ti:estimation OR ti:forecasting) AND (abs:traffic OR abs:road OR abs:bus)`
15. `(ti:survey OR ti:review) AND (ti:traffic OR ti:"spatio-temporal" OR ti:spatiotemporal OR ti:transportation OR ti:mobility) AND (ti:forecasting OR ti:prediction OR ti:"foundation model" OR ti:"large language")`
16. `abs:traffic AND (ti:"physics-informed" OR ti:"physics-guided" OR ti:macroscopic OR ti:"traffic flow model" OR ti:"LWR" OR ti:"kinematic wave") AND (ti:forecasting OR ti:prediction OR ti:estimation)`
17. `abs:traffic AND (ti:"large-scale" OR ti:scalable OR ti:efficient OR ti:linear) AND (ti:"spatio-temporal" OR ti:spatiotemporal OR ti:traffic) AND (ti:forecasting OR ti:prediction)`
18. `abs:traffic AND (ti:"distribution shift" OR ti:"out-of-distribution" OR ti:OOD OR ti:continual OR ti:"test-time" OR ti:"concept drift" OR ti:"non-stationary") AND (...)`
19. `abs:traffic AND (ti:incident OR ti:event OR ti:accident OR ti:disruption OR ti:holiday OR ti:weather OR ti:anomaly) AND (ti:forecasting OR ti:prediction) AND (abs:flow OR abs:speed OR abs:demand)`
20. `abs:traffic AND (ti:tensor OR ti:"Gaussian process" OR ti:Bayesian OR ti:"low-rank" OR ti:"state space" OR ti:Kalman OR ti:autoregressive) AND (ti:forecasting OR ti:prediction)`
21. `abs:traffic AND (ti:"cross-city" OR ti:transfer OR ti:"few-shot" OR ti:"zero-shot" OR ti:"data-scarce" OR ti:"unobserved") AND (ti:forecasting OR ti:prediction)`
22. `ti:UrbanGPT OR ti:CASAformer OR ti:RPMixer OR ti:BigST OR ti:"STD-PLM" OR ti:"STG-LLM" OR ti:UrbanDiT OR ti:"ST-LLM+" OR ti:"STEM-LM"`
23. `abs:traffic AND (ti:imputation OR ti:"missing data" OR ti:"anomaly detection") AND (ti:spatiotemporal OR ti:"spatio-temporal" OR ti:traffic)`
24. `(abs:"spatial dependency" OR abs:"graph structure" OR abs:"spatial module" OR abs:"spatial information") AND abs:traffic AND (ti:necessary OR ti:"really" OR ti:rethinking OR ti:revisiting OR ti:"is all you need" OR ti:simple OR ti:understanding)`
25. `(abs:traffic OR abs:demand OR abs:mobility) AND (ti:"uncertainty quantification" OR ti:"quantile" OR ti:"prediction interval" OR ti:"calibrat" OR ti:"conformal") AND (...)`
26. `(ti:"origin-destination" OR ti:"OD flow" OR ti:"OD matrix" OR ti:"crowd flow" OR ti:"urban flow") AND (ti:forecasting OR ti:prediction)`
27. `abs:traffic AND (ti:congestion) AND (ti:forecasting OR ti:prediction OR ti:"early warning")`
28. 用 `abs` 子命令按 id_list 批量取全文摘要，共 100 个 id，含核对 1707.01926、2306.08259、2301.12603 的 v1 日期。

OpenAlex 查询（三次均为 429，无结果）：`Are state-of-the-art deep learning traffic prediction models truly effective`；`traffic forecasting deep learning Communications in Transportation Research`；`short-term traffic flow prediction graph neural network Transportation Research Part C`；`CASAformer congestion-aware sparse attention traffic speed prediction`。

WebSearch（只用于发现）：“arXiv 2024 2025 traffic forecasting benchmark critique …”，找到 2608.20980 的线索；“Communications in Transportation Research 2024 2025 traffic forecasting …”，找到 CASAformer 线索，但未能用工具核实。

## 2. 纳入/排除原则与主要排除记录

纳入原则：
- 以预测为主：主列表 43 条“预测”、6 条“基准/数据集”、1 条综述。异常检测（2412.10892）和插补（2501.19364）只放在备选。
- STGNN 不堆叠同质变体，每条方法线只保留 1-2 篇：图 Transformer、空间分块、线性图卷积、全 MLP/通道独立、SSM、神经 CDE、谱扩散、SDE 扩散、GMM 输出、共形、闭式协方差、PFN、Koopman、张量分解、物理引导。
- 评测批评与基准排在前面，每篇空间时间论文都写明了空间信息起什么作用。

主要排除（含窗口外的知名文献）：
- 窗口外的经典文献，只保留 3 篇作为 old。DCRNN（1707.01926）是 METR-LA/PEMS-BAY 的出处；LargeST（2306.08259）是大规模基准；SimST（2301.12603）讨论 GNN 是否必要。其余排除：STGCN（1709.04875）、Graph WaveNet（2019）、STID/STNorm（2022）、D2STGNN（2022）、STAEformer（2308.10425，2023-08）、PDFormer（2023）、DiffSTG（2023-01）、STGNPP（2311.08635，AAAI 2023 正式发表早于窗口）、“On the importance of stationarity, strong baselines and benchmarks in transport prediction problems”（2203.02954）。
- 首次公开日期存疑，按会议版本更早处理并排除：2412.03307（共享单车 OD，journal_ref 为 ITSC 2023，Bilbao 2023-09）；2403.09969（船舶到港时间，comment 为 ITSC 2023）。
- 作者自己标注了问题：2412.00167（OD 需求，comment 称内部复核发现若干问题）。
- 不是时间序列预测：2403.05029 BjTT（文本到交通的生成任务）；2602.15069（静态的最小拥堵驾驶时间估计）；2409.03937（LLM 跨城 OD，任务是预测目的地 POI）；2401.17095 MaTE（未观测路段状态估计，不是预测）。
- 不属于本领域：蜂窝/无线网络流量（2512.22178、2410.15322 UoMo、2510.11282 等）、互联网流量、信号控制 LLM、自动驾驶轨迹预测。
- 期刊独有、无法用工具核实：CASAformer（Communications in Transportation Research 2025，WebSearch 线索为低速段预测批评）。OpenAlex 被限流，无法核实 DOI 和 OA PDF，因此没有收录，建议协调人在 OpenAlex 恢复后补核。
- 同一主题的近似重复：2407.12238 与 2603.16857（同一作者的共形 GNN，只保留后者）；2410.00373 与 2411.11448（同一组作者的空间漂移研究，前者降为备选）；2602.05133、2606.15642、2602.01936（同一作者的“混沌感知/物理多相共识”跨城迁移系列，未收录）。

## 3. 子方向覆盖（rank 列表）

| 子方向 | 主列表 | 备选 |
|---|---|---|
| 评测批评 / 空间模块必要性 | 1, 3, 13, 49 | 51 |
| 基准数据集 | 4, 5, 46, 48（47 为数据来源） | — |
| 交通基础模型 / TSFM / 零样本 | 2, 6, 23, 24, 28, 36 | 52, 53 |
| LLM 用于交通预测 | 7, 25, 26, 27, 39, 45 | 58 |
| 大规模 / 高效 STGNN 与非图模型 | 14, 15, 16 | 55, 56 |
| 分布漂移 / 持续学习 / 迁移 | 17, 18, 29, 30 | 51, 65 |
| 概率预测 / 不确定性 | 19, 20, 21, 22, 35 | 54, 61 |
| 事件 / 事故 / 天气 / 扰动影响 | 8, 9, 10, 12, 33, 34, 35 | 57, 58, 62 |
| 统计 / 物理-数据融合 | 11, 30, 31, 32, 12 | — |
| 公共交通（地铁/公交/BRT） | 9, 10, 11, 12, 37, 38 | 58 |
| 网约车 / 出租车 / 共享单车 / 行人 | 5, 22, 33, 36, 39, 40 | — |
| 航空 / 铁路 | 41, 42 | 59 |
| 港口 / 物流 | 45 | 60 |
| 旅行时间 / 拥堵 | 43, 44 | 61 |
| 综述 | 50 | 64 |
| 插补 / 异常检测（少量） | — | 62, 63 |

明显缺口：
- 港口与物流只有 1 篇主列表（LLM 集装箱吞吐量）。船舶到港 2403.09969 因日期存疑而排除。
- 航空客运需求（航线、OD 级）与铁路客流的高质量窗口内论文较少。
- 停车占用预测没有检索。
- 交通安全（事故风险）预测按“事件影响”的角度处理，未单独收集。
- 期刊（TR-C、T-ITS OA、COMMTR）中没有 arXiv 版本的文章因 OpenAlex 限流基本缺失，这是本次最大的系统性缺口。

## 4. 优先阅读 10 篇

1. rank 1：A Critical Audit of Spatiotemporal Forecasting Benchmark Datasets and Models。调好时间线性基线后，GNN 的增益显著缩小或被反超，解读排行榜前应先读。
2. rank 2：Time Series Foundation Models as Strong Baselines in Transportation Forecasting。Chronos-2 零样本在 10 个交通数据集上有竞争力，应作为必备基线。
3. rank 3：Do We Really Need Adaptive Global Spatial Attention for Traffic Forecasting?。受控消融显示空间注意力相对均匀混合没有一致优势。
4. rank 4：XXLTraffic。超长时间跨度且有分布漂移的交通基准，检验部署期稳健性。
5. rank 5：RideBench。带天气、节假日、大型活动外生标注的滴滴网约车基准。
6. rank 6：OpenCity。开源交通时空基础模型，可与 rank 2 的通用 TSFM 对照。
7. rank 8：Incident-Guided Spatiotemporal Traffic Forecasting。把事件影响拆成空间扩散与时间衰减，并附对齐数据集。
8. rank 9：Predicting Subway Passenger Flows under Incident Situation with Causality。用合成控制估计事件因果效应，再嵌入预测。
9. rank 10：Hierarchical Forecast Reconciliation for Urban Rail Transit Demand Prediction under Operational Disruptions。站点与 OD 层次一致性，扰动期效果有提升，并如实报告与统计方法相当。
10. rank 11：Bayesian Markov regime-switching VAR for bus travel time and occupancy（TR-B）。高质量统计方法，给出联合不确定性。

## 5. 扩展领域建议

- 移动/蜂窝网络流量预测：检索中大量出现（UoMo、无线流量 LLM 等），方法与交通 STGNN 高度同构，值得单独成类。
- 人类移动与轨迹/下一地点预测：包括 LLM 移动预测和通用移动基础模型。
- 交通安全/事故风险时空预测：包括事故风险、事故持续时间，可作为预警类任务。
- EV 充电需求：rank 2 的数据包含 EV 充电，应归入能源与电力。
- 旅游/航空预订时间序列（如 TripCast 2410.18612，预订提前期的二维结构），可并入通用方法或单列。

## 6. 无法核实或存疑的条目

- OpenAlex 全程 429，所有 DOI 与 OA PDF 都没有经 OpenAlex 核实。`pdf_candidates` 一律只给 arXiv PDF，DOI 均取自 arXiv 元数据（journal_ref/doi 字段）。
- rank 48 LargeST 的 venue 写为“NeurIPS 2023 Datasets and Benchmarks（待全文核实）”；rank 14 RPMixer 的“KDD 2024”与 rank 44 CP-MoE 的“KDD 2024 ADS”也来自记忆，摘要元数据中没有，均已标注待核实。
- rank 2（2602.24238）只有 6 页，是短文。rank 45（港口 LLM）、rank 36（行人，投稿中）为预印本，证据强度一般。
- rank 28 GAS-PFN 于 2026-10-27 提交，不足一周，尚无外部评价；摘要中的对比设定（各模型只给 90 分钟历史）对通用 TSFM 不利，已在 reason 中注明。
- rank 39 DiDi MVGR 与 rank 5 RideBench 使用滴滴数据。RideBench 数据是“合成自”滴滴市场数据（摘要原话 synthesized），真实度需看全文。
- 2402.00397（MTPB，跨城少样本）有摘要但最终未收录（arXiv 注明与 2308.09727 文本重叠）；STDA-Meta（2310.20223）在窗口内但未收录。主列表 rank 13 与备选 rank 51 作者重叠，属于同一研究线。
- rank 49 SimST（2301.12603）作为 old 收录；rank 47 DCRNN 与 rank 48 LargeST 的 old_reason 已填写。
