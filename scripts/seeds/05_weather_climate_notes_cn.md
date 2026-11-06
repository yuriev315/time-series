# 05_weather_climate（气象与气候）检索与筛选笔记

检索日期：2026-10-29。窗口：首次公开日期 2023-10-29 至 2026-10-29（有 arXiv 版本时一律取 arXiv v1 提交日）。
输出：`scripts/seeds/05_weather_climate_seed_cn.json`，共 65 条：1-50 为主列表，51-65 为备选。
主列表中近三年 48 篇（96%），三年前 2 篇（rank 14 GraphCast 2212.12794、rank 15 WeatherBench 2 2308.15560）。备选 15 篇全部在窗口内。
所有条目都有 arXiv 版本，即都有合法公开的全文 PDF 路径。另有 4 篇在 OpenAlex 中查到期刊 OA PDF 或机构库 PDF（Aurora、Aardvark、FuXi-S2S，已写入 pdf_candidates）。

## 1. 检索平台与实际使用的查询

均通过 `scripts/search_candidates_en.py` 执行（共享限速）。arXiv 查询的日期窗口由脚本自动添加。

arXiv（search_query）：
1. `abs:"weather forecasting" AND abs:"machine learning" AND (abs:global OR abs:medium-range) AND cat:physics.ao-ph`（-n 40）
2. `abs:nowcasting AND (abs:precipitation OR abs:radar OR abs:rainfall)`
3. `abs:"foundation model" AND (abs:weather OR abs:atmospheric) AND (cat:physics.ao-ph OR cat:cs.LG)`
4. `(abs:subseasonal OR abs:"sub-seasonal" OR abs:S2S) AND abs:forecast*`
5. `abs:ENSO AND abs:predict* AND (abs:"deep learning" OR abs:"machine learning" OR abs:neural OR abs:"linear inverse")`
6. `(abs:"tropical cyclone" OR abs:typhoon OR abs:hurricane) AND abs:forecast* AND (abs:"deep learning" OR abs:"machine learning" OR abs:"data-driven")`
7. `(abs:postprocessing OR abs:post-processing) AND abs:ensemble AND abs:forecast* AND (cat:stat.AP OR cat:physics.ao-ph OR cat:stat.ML)`
8. `(abs:heatwave OR abs:"heat wave" OR abs:"extreme heat" OR abs:heatwaves) AND abs:forecast*`
9. `(abs:"weather station" OR abs:"weather stations" OR abs:"station observations") AND abs:forecast* AND (abs:temperature OR abs:wind OR abs:precipitation)`
10. `(abs:"wind speed" OR abs:"wind gust") AND abs:forecast* AND (abs:"deep learning" OR abs:"neural network" OR abs:transformer)`
11. `(abs:"extreme precipitation" OR abs:"heavy rainfall" OR abs:"heavy precipitation") AND abs:forecast* AND (abs:learning OR abs:neural OR abs:diffusion)`
12. `(abs:WeatherBench OR abs:"verification") AND abs:"machine learning" AND abs:weather AND cat:physics.ao-ph`
13. `(abs:"limited area" OR abs:regional OR abs:"km-scale" OR abs:kilometer-scale) AND abs:"weather" AND abs:forecast* AND (abs:graph OR abs:diffusion OR abs:"machine learning")`
14. `abs:emulator AND abs:climate AND (abs:autoregressive OR abs:"long rollout" OR abs:"stable")`
15. `(abs:"seasonal forecast" OR abs:"seasonal prediction" OR abs:"seasonal forecasts") AND (abs:"machine learning" OR abs:"deep learning")`：**多次 HTTP 429 失败**（简化为 `ti:seasonal AND abs:forecast AND cat:physics.ao-ph` 后仍是 429）
16. `(abs:temperature OR abs:humidity) AND abs:forecast* AND abs:"time series" AND (abs:weather OR abs:meteorological)`：**HTTP 429 失败**

arXiv `abs`（id_list 批量取完整摘要和元数据，每批 10 个）：主列表与备选的全部 65 个 ID，另加 Prithvi WxC 2409.13598、LaDCast 2506.09193、Diffusion-LAM 2502.07532、ResoNet 2312.10429、PTSTnet 2503.21211、CESAR 2412.10578、Arctic 温度 2510.23976、AI 极端事件综述 2406.20080、基础模型综述 2312.03014、WP-MIP 2604.16643、热浪算法预报 2409.18305、Spherical DYffusion 2406.14798、SFNO 夏季 2023 热浪 2604.09754、Aurora 极端评估 2603.06516、FMAP 2504.03463、CNN 温度后处理 2507.18937、TCP-Diffusion 2410.13175、TIFNet 2509.21349、ZWD+Aurora 2607.05658、WxFM-XL 2610.10057、exPreCast 2602.05204。另尝试核实若干早于窗口的知名文献 ID，因 429 失败。

OpenAlex：
- 按 DOI 核实期刊版本（成功）：10.1038/s41586-024-08252-9（GenCast）、10.1038/s41586-025-09005-y（Aurora）、10.1038/s41586-025-08897-0（Aardvark）、10.1038/s41467-024-50714-1（FuXi-S2S）、10.1038/s41586-024-07534-6（XRO ENSO）。
- 自由文本检索（`--oa`）：`seasonal forecast machine learning precipitation temperature skill`、`ENSO prediction deep learning lead time` / `lead months`、`Aurora foundation model atmosphere`（--title）、`temperature forecasting weather station time series deep learning`、`air temperature forecasting meteorological station deep learning hourly`、`relative humidity forecasting neural network`、`Madden-Julian oscillation prediction machine learning`、`seasonal climate prediction deep learning hindcast`：**全部因 HTTP 429 失败**，因此没有得到 OpenAlex 检索结果。

WebSearch：未使用。

## 2. 纳入/排除原则与主要排除记录

纳入：核心任务有时间依赖（预报、预警或可预报性分析）；优先预报类论文；覆盖不同变量（温度、降水、风、湿度/可降水量、热指数、雷达反射率、ENSO/NAO/MJO 指数、TC 强度/路径）、不同尺度（站点、区域公里级、全球）、不同时效（分钟级临近预报到季节/年代际）和不同方法（统计后处理、ML、DL、扩散/流匹配生成模型、基础模型、物理-数据融合）。每条都写明空间信息的作用。
非预测类：基准/数据集 5 篇（WB2、RainfallBench、ChaosBench、TCBench、WEATHER-5K），预警 1 篇，综述 1 篇。没有异常检测、插补或分类论文。

主要排除记录：
- **早于窗口的知名文献**（未进主列表）：Pangu-Weather、FuXi（中期版）、FourCastNet（v1）、ClimaX、NowcastNet、MetNet-3、PreDiff、LDCast、Neural-LAM 早期版本、CorrDiff、ACE（v1）、EUPPBench。这些文献在检索结果中只作为被比较的基线出现，按已知首发年份（2022 年至 2023 年 10 月前）判定早于窗口。具体 arXiv ID 和 v1 日期本轮未能用工具重新核实（arXiv 返回 429），**待核实**。主列表只保留 GraphCast 与 WeatherBench 2 两篇旧文献（v1 日期已核实为 2022-12-24 与 2023-08-29），作为基线和评测基础。
- **XRO ENSO（Zhao et al., Nature 2024, 10.1038/s41586-024-07534-6）**：OpenAlex 显示 closed，没有 arXiv 版本，也没有找到 OA PDF，按规则排除。
- 两篇 Zeyi Niu 的 ML-物理融合台风论文（2503.00424、2504.20852）：arXiv comments 称作者因实验流程错误申请撤稿，排除。
- 2402.09846（雷达 QPE）：journal_ref 显示 2021 年已发表，属旧文，排除。
- 2510.21176：journal_ref 为 2023 年 Multimed Tools Appl，属旧文，排除。
- 量子 ML 天气预报类（2509.01422、2605.18333、2608.01626 等）、LLM/多模态问答类（WeatherQA、Zephyrus、Skew-T 推理）：方法新颖但预报证据弱或不属时间预测，排除。
- 太阳风/空间天气（2507.17298、2410.05068 等）：不属于地球大气气象，排除。
- 海洋（Samudra、NeuralOM、海洋热浪、风暴潮 Flo）：属海洋预测，建议单独收集，见第 5 节。
- 纯降尺度（AirCast-SR、PrecipCorrDiff、WGAN 降尺度等）：不涉及时间预测，按 scope 排除。FuXi-TC、CNN 温度集合后处理等“预报+降尺度”的论文保留或列入候选。
- 同类堆叠控制：临近预报候选很多（FusionCast、SimCast、MeTok、PA-Net、REE-TTT、QWRF-Net、VMU-Diff、FreCast 等），只保留方法类型不同的代表：级联、残差扩散、GPT token、卫星→雷达、业务全球、灰区统一生成、站点时序基准，另加三维灰箱与流匹配作为备选。

## 3. 子方向覆盖表

| 子方向 | 主列表 rank | 备选 rank |
|---|---|---|
| 全球中期确定性/集合预报（数据驱动） | 1, 3, 5, 6, 7, 9, 10, 11, 14 | 61 |
| 混合物理-ML / 端到端观测到预报 | 2, 4, 8 | — |
| 区域公里尺度 / 有限区模式 | 12, 13 | 52 |
| 降水临近预报（雷达/卫星/GNSS） | 16, 17, 18, 19, 20, 21, 22 | 51, 60 |
| 次季节 S2S / 季节 / 气候仿真 | 23, 24, 25, 26, 27, 28, 29 | 53, 55, 56, 57 |
| 气候模态（ENSO、NAO、MJO） | 30, 31, 32, 33（MJO 也见 23、25） | 57 |
| 热带气旋 | 34, 35, 36 | 54 |
| 极端天气 / 热浪 / 预警 | 37, 38, 39, 40 | 64 |
| 统计/ML 后处理与概率评估 | 41, 42, 43, 44, 45, 46 | 59, 65 |
| 站点预报（温度、风、多变量） | 44, 47, 48, 49 | 62, 63 |
| 评测基准 | 15, 22, 24, 34, 49 | 58 |
| 综述 | 50 | — |

变量覆盖：温度（38、44、47、49）、降水（16-22、43、46）、风速/阵风（41、42、48、55）、湿度/可降水量（22 PWV、39 热指数、62 PWV）、气候指数（30-33）、TC 强度与路径（34-36）。

明显缺口：
- **季节预测（3-6 个月）**的专门 ML 论文偏少。主列表只有 S2S 与 ENSO/NAO，DUNE（53）在备选。原因是专门检索季节预测的 arXiv/OpenAlex 查询均因 429 失败。建议协调者在限速恢复后补检 `seasonal forecast` 与 Copernicus/AMS 期刊中的 OA 论文。
- **湿度（相对湿度）**的直接预报论文缺失。目前只有 PWV 与热指数间接覆盖。
- **非 arXiv 的期刊 OA 论文**（Copernicus GMD/WCD/NPG、QJRMS OA、MDPI）偏少，因为 OpenAlex 检索全部 429。目前的期刊论文都通过 arXiv 版本收录（GPTCast 为 GMD，多篇为 AIES/MWR/QJRMS）。
- 闪电、能见度、雾等变量没有覆盖。

## 4. 优先阅读 10 篇

1. rank 1 GenCast：数据驱动概率集合预报的代表，几乎所有后续集合模型都与它比较。
2. rank 2 NeuralGCM：混合物理-ML 路线，同时覆盖天气与气候时间尺度。
3. rank 4 Aardvark Weather：端到端由观测到站点预报，改变 NWP 流程的范式。
4. rank 3 Aurora：基础模型 + 微调，覆盖天气、空气质量、海浪、TC。
5. rank 23 FuXi-S2S：ML 在次季节尺度首次超过业务模式，涉及 MJO。
6. rank 24 ChaosBench：说明中期模型外推到 S2S 会失效，是 S2S 评测基础。
7. rank 35 灰天鹅热带气旋：检验 AI 模型能否外推到训练集中缺失的极端事件。
8. rank 40 Do AI weather models miss extremes?：用站点观测检验尾部表现，校正笼统结论。
9. rank 45 PC 指标（Gneiting 等）：确定性 AI 与 NWP 公平比较的评估方法论。
10. rank 22 RainfallBench：通用时序模型在降水/湿度站点序列上的表现，与通用方法类别交叉。

## 5. 扩展领域建议

- **海洋预报**（海温、海浪、海冰、海洋热浪、风暴潮）：候选很多，如 Samudra、NeuralOM、Neptune、海洋热浪 DL、Flo 风暴潮、IceBench-S2S、北极海冰季节订正。建议单独设类或并入“水文与水资源”以外的海洋子类。
- **野火与干旱/土壤湿度预测**：如 DroughtSet、次季节土壤湿度与骤旱、野火预测评估。
- **空间天气**（太阳风、太阳耀斑、高能粒子）：arXiv 上有大量时间序列预测论文，可独立收集。
- **可再生能源气象**（风电/光伏的天气驱动预测）：与“能源与电力”交叉，例如 PING、法国风光数据集、S2S 风电预测。

## 6. 无法核实或存疑的条目

- rank 4 Aardvark：arXiv 第一作者为 Anna Vaughan，Nature 版（OpenAlex）第一作者为 Anna Allén，二者应为同一人更名。种子表按 arXiv 记为 Vaughan，期刊题名不同（End-to-end data-driven weather prediction）。
- rank 1 GenCast、rank 23 FuXi-S2S：期刊题名与 arXiv 题名不同，种子表 title 用 arXiv 题名，venue 字段注明期刊题名。
- rank 47 Local Off-Grid：venue 写为 JAMES，是根据 DOI 前缀 10.1029/…MS 推断的，**待核实**。
- rank 35 灰天鹅 TC：venue 写为 PNAS，依据是 arXiv DOI 字段 10.1073/pnas.2420914122，未查看出版页面。
- rank 20、41、48：venue 依据 arXiv comments 中的“已接收/将发表”，正式出版信息未核实。
- 多数条目的 frequency、horizon、split 摘要未给出，已标为“待全文核实”。
- GPTCast（rank 18）的 GMD 期刊 OA PDF 未在检索结果中直接看到，pdf_candidates 留空，协调者可使用 arXiv。
- 所有简介仅依据摘要；作者主张均未经全文核实。
