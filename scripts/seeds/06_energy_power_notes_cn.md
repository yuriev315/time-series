# 06_energy_power（能源与电力）检索与筛选笔记

检索日期：2026-10-29；时间窗口：首次公开日期 2023-10-29 至 2026-10-29（有 arXiv 版本的以 arXiv v1 日期为准）。
产出：`scripts/seeds/06_energy_power_seed_cn.json`，共 65 条：第 1-50 名为主清单，第 51-65 名为备选（全部为近三年）。
主清单中近三年 47 条、三年前 3 条（94%）；备选 15 条全部为近三年。

## 1. 检索词与平台（实际执行过的查询）

所有查询都通过 `scripts/search_candidates_en.py` 执行（arXiv 查询自动加了日期过滤）。

arXiv API：
1. `ti:"load forecasting" AND (abs:probabilistic OR abs:quantile)`
2. `ti:"electricity price" AND (ti:forecast* OR abs:forecasting)`
3. `(ti:"wind power" OR ti:"wind speed") AND ti:forecast*`
4. `(ti:photovoltaic OR ti:"solar power" OR ti:"PV power" OR ti:irradiance OR ti:"solar forecasting") AND (ti:forecast* OR ti:nowcast*)`
5. `(abs:satellite OR abs:"sky images" OR abs:"all-sky") AND (ti:solar OR ti:irradiance) AND abs:forecast*`
6. `(ti:building OR ti:buildings) AND (ti:energy OR ti:load OR ti:consumption) AND (abs:forecast* OR abs:benchmark)`
7. `(ti:"EV charging" OR ti:"electric vehicle charging" OR ti:"charging demand" OR ti:"charging load") AND abs:forecast*`
8. `(ti:"natural gas" OR ti:"gas demand" OR ti:"gas consumption" OR ti:"heat demand" OR ti:"heat load" OR ti:"district heating") AND abs:forecast*`
9. `(abs:"foundation model" OR abs:"foundation models") AND (ti:energy OR ti:load OR ti:electricity OR ti:power OR ti:grid)`
10. `(ti:"mid-term" OR ti:"medium-term" OR ti:"long-term" OR ti:"annual" OR ti:"monthly") AND (ti:load OR ti:demand OR ti:electricity) AND ti:forecast*`
11. `(abs:"generalized additive" OR abs:GAM OR abs:"Kalman") AND (abs:"electricity load" OR abs:"electricity demand" OR abs:"electricity consumption")`
12. `(ti:hierarchical OR ti:reconciliation OR ti:coherent) AND (abs:electricity OR abs:energy OR abs:"smart meter") AND abs:forecast*`
13. `(ti:review OR ti:survey OR ti:tutorial) AND (ti:energy OR ti:load OR ti:electricity OR ti:wind OR ti:solar OR ti:renewable) AND ti:forecast*`
14. `(ti:dataset OR ti:benchmark OR ti:competition OR ti:challenge) AND (ti:energy OR ti:load OR ti:electricity OR ti:"smart meter" OR ti:power) AND abs:forecast*`
15. `(ti:household OR ti:residential OR ti:"smart meter") AND (ti:load OR ti:consumption OR ti:demand) AND ti:forecast*`
16. `(abs:"extreme weather" OR abs:heatwave OR abs:"cold snap" OR abs:"COVID") AND (ti:load OR ti:demand OR ti:electricity) AND abs:forecast*`
17. `(ti:"net load" OR ti:"behind-the-meter" OR ti:"distribution grid" OR ti:"substation" OR ti:transformer) AND ti:forecast* AND (abs:load OR abs:demand)`
18. `(ti:anomaly OR ti:"energy theft" OR ti:imputation OR ti:"missing data") AND (ti:"smart meter" OR ti:load OR ti:"energy consumption" OR ti:photovoltaic OR ti:"wind turbine")`
19. `(ti:conformal OR ti:"online learning" OR ti:adaptive OR ti:"concept drift") AND (ti:load OR ti:electricity OR ti:wind OR ti:solar OR ti:energy) AND ti:forecast*`：**失败**（arXiv 返回 HTTP 429，未重试）
20. `abs` 命令按 10 个一组批量取了 100 个候选的完整 arXiv 元数据与摘要（id_list），JSON 中的摘要依据全部来自这里。

OpenAlex：
- `openalex 'probabilistic wind power forecasting' --oa`、`'day-ahead photovoltaic power forecasting numerical weather prediction' --oa`、`'electricity load forecasting temperature calendar effects' --oa`、`'wind power ramp forecasting' --oa`、`'wind power forecasting' --title --oa`：**全部失败**（HTTP 429，共享限额被占满）。
- `abs 10.1109/OAJPE.2020.3029979`：成功（Hong 等 2020 综述的 OA 位置与摘要）。

WebSearch：未使用。

影响：由于 OpenAlex 检索几乎全部被限流，本清单的候选**主要来自 arXiv**。期刊论文只在有 arXiv 版本时才被纳入（arXiv 元数据中的 journal_ref/DOI 显示其中多条已在期刊或会议正式发表或接收，例如 Applied Energy、Renewable Energy、Energy and AI、IEEE TSTE、IEEE Access、IJF、PLOS ONE、MWR、Solar Energy）。Copernicus《Wind Energy Science》等没有 arXiv 版本的 OA 期刊论文本轮没有覆盖到，见第 4 节缺口。

## 2. 纳入/排除原则与主要排除记录

纳入原则：
- 核心任务必须有时间依赖（以预测为主）。每篇都记录目标、跨度、外生变量（天气/日历/经济/文本等）以及空间信息的作用。
- 在目标（负荷/电价/风/光/热/气/EV）、跨度（分钟级临近预报到多年）、空间层级（户、馈线、变电站、区域、国家、跨国）和方法（GAM/分位数回归/状态空间/计量经济、树模型、深度学习、扩散生成、基础模型、物理-数据融合）之间分散选择。同一模型套不同城市的近似重复论文不收。
- 每条都有合法 PDF 路线：除 Hong 2020（IEEE OAJPE 金色 OA + 波兰弗罗茨瓦夫理工大学 RePEc 工作论文版）外，全部有 arXiv 版本。
- 三年前文献只保留 3 篇评测/基准基础文献（见下）。

三年前文献（主清单内，均有 old_reason）：
- rank 2：Hong et al. 2020《Energy Forecasting: A Review and Outlook》（IEEE OAJPE，DOI 10.1109/OAJPE.2020.3029979）
- rank 22：Lago et al.《Forecasting day-ahead electricity prices…open-access benchmark》（arXiv 2008.08004，Applied Energy 2021）
- rank 23：BuildingsBench（arXiv 2307.00142，2023-06-30，早于窗口约 4 个月）

已排除的知名但早于窗口的文献（均不收）：
- Hong et al. 2016 GEFCom2014 竞赛论文（IJF），Hong & Fan 2016 概率负荷预测教程综述（IJF）：早于窗口，且 IJF 非 OA。
- Nowotarski & Weron 2018 概率电价预测综述（RSER）：早于窗口，付费。
- Obst, de Vilmarest & Goude 2021 COVID 期间自适应 GAM 负荷预测：早于窗口；其后续工作以 rank 3（2609.17000）为代表（另有未入选的 2503.24019）。
- Ziel & Steinert 2016 供需曲线电价模型：早于窗口；以 rank 8（2512.17758）为近年代表。
- Wang et al. 2019 智能电表数据分析综述：早于窗口。

其他主要排除：
- 2411.00337（Coherent Hierarchical Probabilistic Forecasting of EV Charging Demand）：arXiv v1 是 2024-11，但 DOI 10.1109/TIA.2023.3344544 显示 2023 年已有期刊版本，首次公开日期可能早于窗口，无法核实，所以排除。
- 2311.08550（ARIMA+Kalman+LSTM 风速）：arXiv 注释写有“error in submission file”。2504.06532 已被撤回。2610.10459（NeuralBES）因未获雇主授权已撤回。都排除。
- 2603.29179（印度峰值负荷 Transformer）：是 2022 年会议论文的晚发 arXiv 版本，属“旧论文新版本”，排除。
- 2401.08233（形状特征风速风电）：期刊版本为 2023 年，且所在期刊较弱，排除。
- 2608.11446、2608.13039（区域供热 XGBoost/可解释性）：对应 2024-2025 年的会议/期刊版本，方法偏简单，排除。
- 方法较简单、单一 LSTM 应用、或同质化的论文：如 2510.16719、2604.24306、2506.23504（AlexNet+LSTM 电价）、2510.06476、2604.23500 等。
- 主题偏离（不以时间预测为核心）：如电网优化/控制/调度（2603.23748、2602.17239）、建筑能耗模拟（2511.19463、2608.06772）、窃电检测（2602.16181）、太阳风/空间天气（2507.17298、2609.26683）。
- 本轮因篇幅而未纳入、质量可接受的候选（可作二级备选）：2511.13603（电价方差稳定变换，EPSR）、2610.02256（TRACE 文本+电价基准）、2411.11350（Chronos 零/少样本负荷，IJEPES）、2603.14845（天气基础模型+卫星辐照度）、2312.11966（SHADECast 扩散辐照度临近预报）、2503.21966（天空图像基准，Solar Energy）、2606.12097（风电 SDE 一个月前瞻）、2608.05018（德国输电网 41 天实时挑战）、2412.06112（PowerMamba，TPWRS）、2504.16100（法国风光数据集，EDS）、2501.05000（户级/能源社区负荷）、2601.13476（EV 充电数据插补，TSG）、2501.07276（电表插补基准）、2404.03011（风机异常检测迁移，Energy and AI）、2408.16202（深度学习短期负荷综述）、2409.15794（天然气基础模型）、2610.18280（物理约束图网络光伏）、2503.24019（在线 GAM 自动选择）。这些候选的完整注释都在本 agent 的草稿里，需要时可以补入。

异常检测、插补与分类：主清单中没有异常检测或插补论文，只有 1 篇“预警”（rank 44，光伏爬坡事件）。备选中有 1 篇异常检测（rank 63）。限量要求满足。

## 3. 子方向覆盖表（子方向 -> 排名）

| 子方向 | 主清单 rank | 备选 rank |
|---|---|---|
| 综述/评测基础 | 2, 22, 38 | 60 |
| 竞赛/基准/数据集 | 1, 14, 15, 16, 17, 22, 23 | 62 |
| 系统/区域级短期负荷 | 3, 5, 19, 26, 27 | 57, 65 |
| 中长期负荷（月-多年） | 4, 24, 25 | 52, 64 |
| 配电网/低压/净负荷 | 29, 30, 32 | 63 |
| 户级/建筑能耗 | 23, 31, 47 | 51, 56 |
| 极端天气下的负荷 | 28 | 52 |
| 日前电价 | 6, 8, 18, 22, 33, 37 | 53 |
| 日内/平衡市场电价 | 34, 35 | 54 |
| 中长期电价 | 36 | — |
| 风电/风速（超短期至次季节） | 9, 10, 16, 39, 40, 41, 42 | 61 |
| 光伏/辐照度（卫星、天空图像、NWP 替代） | 11, 12, 13, 17, 43, 44 | — |
| 热需求/区域供热 | 31, 45 | 55 |
| 天然气需求 | 46 | — |
| 电动汽车充电需求 | 20, 48, 49 | 58 |
| 层级/调和预测 | 49, 50 | 59 |
| 基础模型（能源中的应用） | 7, 10, 14, 18, 19, 21, 29, 30, 45, 47 | 51, 57, 60 |
| 统计方法（GAM/分位数回归/状态空间/计量/copula/INLA） | 3, 4, 8, 20, 25, 33, 34, 36, 37, 40, 49, 50 | 53, 59 |
| 物理-数据融合 | —（主清单暂无；rank 21 为天气基础模型微调） | 56, 61 |
| 天气/气象输入（交叉气象与气候） | 9, 11, 12, 13, 17, 21, 28, 42, 44 | 52 |

明显缺口：
- 没有覆盖 Copernicus WES、Solar Energy 等期刊中仅有期刊版本（无 arXiv）的论文，原因是 OpenAlex 检索被限流（429）。
- 天然气需求只有 1 篇，城市级燃气或管网负荷较少。
- 中国电网与中国学者的大型系统级负荷/电价研究以期刊为主（多为 IEEE TPWRS/TSG、付费），本清单覆盖较少。
- 数据中心负荷与新型大负荷（如北弗吉尼亚，2609.34140）的长期预测只在检索中出现，没有收录。
- 水电与入流预测属于“水文与水资源”，没有收录。
- 电池/储能 SOC、电网频率等时序预测不在本类别范围内。

## 4. 优先阅读 10 篇

1. rank 1：The Hybrid Renewable Energy Forecasting and Trading Competition 2024。IJF 正式竞赛报告，真实前向评测，同时讨论预测技巧与交易价值。
2. rank 2：Energy Forecasting: A Review and Outlook（2020）。领域权威综述，给出可复现研究规范与开放数据源。
3. rank 3：Combining Weather Forecast Aggregation and State-Space Models…。GAM + 状态空间在线自适应，并聚合多家气象预报，统计路线的代表。
4. rank 4：Efficient mid-term forecasting of hourly electricity load using GAMs。中期小时负荷，气温、节假日、经济变量处理细致，可解释。
5. rank 6：The role of probabilistic load and renewable prediction in enhancing day-ahead electricity price forecasts。把负荷与风光预测的不确定性传递到电价预测。
6. rank 8：Day-Ahead Electricity Price Forecasting Using Merit-Order Curves Time Series。从供需曲线（市场机制）出发的结构化电价预测。
7. rank 9：Seamless short- to mid-term probabilistic wind power forecasting。拆分天气不确定性与功率转换不确定性，6-162 小时一个模型覆盖。
8. rank 11：Intraday spatiotemporal PV power prediction at national scale…。全国 6434 个站点的卫星光伏时空预测评估。
9. rank 14：FETS Benchmark。覆盖 54 个能源数据集的基础模型与专用模型对比。
10. rank 18：Foundation models for electricity price forecasting and battery arbitrage。同时给出统计与经济评价，结论审慎（基础模型不能普遍取代专用模型）。

## 5. 扩展领域建议

- **气象预报后处理与次季节预报（服务能源）**：如 2411.19077、2509.25268、2412.13957（温度/风速后处理 Transformer）、2503.23893（DiffScale 次季节风速降尺度）。可以在“气象与气候”类中单独收集“面向能源的气象预报”。
- **能源市场交易与决策价值导向预测**（value-oriented forecasting、预测-优化一体化）：2501.16086、2510.12382 等，可与“金融”合作收集。
- **多模态/文本增强的能源预测**（LLM、VLM、运行文本）：2610.02256、2604.04145、2506.03728、2506.11050（NSW-EPNews）。数量增长很快，可以单独成为一个子主题。
- **电网资产与运维时序**（变压器动态热定值、覆冰、风机 SCADA 异常）：2603.11905、2509.25268、2404.03011，可以归入“工业与设备”。
- **天然气与商品价格预测**（2604.24788 天然气现货价格等）：可以归入“金融/商品”。

## 6. 无法核实或存疑的条目说明

- rank 2（Hong 2020）：OpenAlex 的 publication_date 是 2020-01-01，只能确认年份。JSON 中填的 2020-01-01 是 OpenAlex 的值，不代表真实上线日。属于 old 条目，不影响窗口判断。
- rank 56（2508.09161）：arXiv v1 是 2025-08-05，但 arXiv 注释称已在 Energy and AI 发表，所给卷号（Volume 15）与 DOI 序号（100538）的时间对不上。期刊上线日可能早于 arXiv v1，不过即使如此也在窗口内。卷期请以 DOI 为准核实。
- 检索中见到个别 arXiv ID 的月份与 v1 日期不一致（入选条目未受影响），例如 2610.35885 的 v1 是 2026-09-05，2610.06881 的 v1 是 2026-09-19。入选条目都以 helper 返回的 v1 日期为准。
- 摘要被截断的条目（helper 返回的摘要很完整，但本 agent 只阅读了每条前约 1100 个字符）：rank 18、19、20、21、28、29、30 等条目的数值结论只引用了已读到的部分，其余字段标为“待全文核实”。
- 已发表信息全部来自 arXiv 的 journal_ref/DOI/comment 字段，没有逐一到出版社核实。“已接收”类条目（如 TSTE、TPWRS、ICDE 2027、Grid Edge 2027）的最终出版状态待核实。
- 交叉分类“金融”只用于摘要明确涉及交易、报价、利润或市场微观结构的条目（rank 1、18、33、35、36，备选 54、59）。按 brief 要求，交易收益不作为预测有效性的证据，相关 summary 中已注明。
