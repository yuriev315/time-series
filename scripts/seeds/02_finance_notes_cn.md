# 02_finance（金融）检索笔记

检索日期：2026-10-29；收录窗口：首次公开日期 2023-10-29 .. 2026-10-29（有 arXiv 版本的以 arXiv v1 为准）。
产出：`scripts/seeds/02_finance_seed_cn.json`，共 65 条：rank 1-50 为主列表，51-65 为备选。
主列表中近期文献 48 篇（96%），旧文 2 篇（2308.01915 LOBCAST、2601.13014 Christensen 等）；备选 15 篇全部是近期文献。
65 条都有 arXiv 版本，PDF 路线统一为 `https://arxiv.org/pdf/<id>`（合法、公开）。
所有字段只依据 arXiv API 返回的摘要与元数据（comment、journal_ref、DOI）填写，摘要里没有的信息标为“待全文核实”。

## 1. 检索词与平台（实际执行过的查询）

平台：arXiv API（经 `scripts/search_candidates_en.py`，自动限定日期窗口）。OpenAlex 也尝试过，但本轮所有 OpenAlex 搜索都返回 HTTP 429（共享配额已用尽），没有拿到结果。为此只用一次 OpenAlex `abs` 查询核对了 Christensen 文的 DOI 日期。本轮没有使用 WebSearch。

arXiv 查询：
1. `abs:"realized volatility" AND (abs:forecasting OR abs:forecast)`
2. `abs:"foundation model" AND (abs:financial OR abs:stock) AND abs:forecasting`
3. `abs:"large language model" AND abs:"stock" AND (abs:forecast OR abs:prediction) AND abs:"look-ahead"`
4. `ti:volatility AND (ti:"machine learning" OR ti:"deep learning" OR ti:neural OR ti:transformer)`
5. `abs:"implied volatility" AND (ti:forecasting OR ti:predicting)`
6. `abs:"value-at-risk" AND abs:"expected shortfall" AND abs:forecasting AND (cat:q-fin.RM OR cat:econ.EM OR cat:q-fin.ST)`
7. `abs:"limit order book" AND (abs:forecasting OR abs:"price movement" OR abs:prediction) AND abs:benchmark`
8. `(ti:"exchange rate" OR ti:"exchange rates" OR ti:FX OR ti:currency) AND (ti:forecasting OR ti:forecast OR ti:predictability)`
9. `(ti:"yield curve" OR ti:"term structure" OR ti:"interest rate" OR ti:"bond yields") AND (ti:forecasting OR ti:forecast OR ti:predicting)`
10. `(ti:bitcoin OR ti:cryptocurrency OR ti:crypto) AND (ti:forecasting OR ti:prediction) AND (cat:q-fin.ST OR cat:q-fin.CP OR cat:cs.LG OR cat:econ.EM)`
11. `(abs:"look-ahead bias" OR abs:"lookahead bias" OR abs:"data leakage" OR abs:"memorization") AND (abs:financial OR abs:stock) AND (abs:LLM OR abs:"language model")`
12. `(abs:"cross-section of stock returns" OR abs:"cross-sectional return" OR abs:"return predictability") AND (abs:"machine learning" OR abs:"neural network" OR abs:transformer) AND (cat:q-fin.ST OR cat:q-fin.PM OR cat:econ.EM OR cat:q-fin.GN)`
13. `(ti:"stock movement" OR ti:"stock price movement" OR ti:"stock trend") AND (ti:prediction OR ti:forecasting)`
14. `(ti:covariance OR ti:correlation OR ti:"multivariate volatility") AND (ti:forecasting OR ti:forecast) AND (cat:q-fin.ST OR cat:econ.EM OR cat:q-fin.RM OR cat:q-fin.PM)`
15. `(ti:crash OR ti:crisis OR ti:"early warning" OR ti:"systemic risk" OR ti:bubble OR ti:drawdown) AND (ti:predict OR ti:prediction OR ti:forecasting OR ti:"early warning") AND (cat:q-fin.ST OR cat:q-fin.RM OR cat:econ.EM OR cat:q-fin.GN)`（第一次 429，重试后成功）
16. `(abs:"data snooping" OR abs:"backtest overfitting" OR abs:"multiple testing" OR abs:"look-ahead bias") AND (abs:forecast OR abs:predictability OR abs:prediction) AND (cat:q-fin.*  …)`
17. `(abs:"equity premium" OR abs:"stock market return") AND (ti:forecasting OR ti:predictability OR ti:predicting OR ti:forecasts)`
18. `(abs:"multi-asset" OR abs:"cross-asset" OR abs:"asset classes") AND (ti:forecasting OR ti:prediction OR ti:predictability) AND (…)`
19. `(ti:commodity OR ti:"crude oil" OR ti:gold OR ti:futures) AND (ti:forecasting OR ti:forecast) AND (…)`
20. `(ti:intraday OR ti:"high-frequency") AND (ti:volume OR ti:returns OR ti:"price") AND (ti:forecasting OR ti:prediction OR ti:predicting)`
21. `(ti:survey OR ti:review) AND (ti:financial OR ti:stock) AND (ti:forecasting OR ti:prediction) AND (abs:"time series" OR abs:"deep learning")`
22. `(abs:"anomaly detection" OR abs:"manipulation detection") AND (abs:"stock" OR abs:"financial market" OR abs:cryptocurrency) AND (abs:"time series")`
23. `(abs:"density forecast" OR abs:"probabilistic forecast" OR abs:"conformal") AND (abs:"stock returns" OR abs:"asset returns" OR abs:"financial returns")`
24. `(abs:"stock" OR abs:"financial") AND abs:"time series" AND abs:benchmark AND (abs:forecasting) AND (abs:leakage OR abs:"realistic" OR abs:"non-stationary")`
25. 用 `abs <id1,id2,…>` 批量取 96 个候选的完整摘要和元数据（arXiv id_list）

OpenAlex 查询（都因 429 失败，没有结果）："stock market crash early warning prediction machine learning"、"data snooping out-of-sample stock return predictability machine learning"、"equity premium forecasting out-of-sample machine learning"、"exchange rate forecasting random walk machine learning out-of-sample"、"realized volatility forecasting HAR machine learning"、"cryptocurrency return forecasting out-of-sample machine learning"。

## 2. 纳入 / 排除原则与主要排除记录

纳入原则：
- 核心任务必须有时间依赖，预测优先，并且 target 必须写明（收益、方向、RV、VaR/ES、曲面、收益率曲线等）。
- 优先收录有明确基准（HAR、随机游走、AR(1)、GARCH）、样本外或滚动设计、正式检验（DM、MCS、GW、多重检验校正）的研究。
- 金融特有的评估问题（前视偏差、记忆、回测过拟合、基准公平性、体制变化）单独作为一个子方向收录。
- 只靠回测利润或 Sharpe 支撑结论的论文，在 summary 中注明“证据以策略收益为主，不作为预测有效性证据”。

主要排除记录：
- 窗口之前的经典文献（未收录或只在笔记中提及）：Corsi HAR（2009）、Meese-Rogoff（1983）、DeepLOB（Zhang et al. 2019）、FI-2010 数据集（2017）、Gu-Kelly-Xiu “Empirical Asset Pricing via ML”（2020，无 arXiv/OA 稳定路线）、Kelly 等 “Virtue of Complexity”（SSRN）。旧文只保留 2 篇：LOBCAST 基准（2308.01915，v1 为 2023-07-05）和 Christensen 等 HAR vs ML（期刊 2022 年，arXiv 2026 年才上传）。
- 质量弱或同质化的价格预测论文：2405.08089、2508.01419、2506.22055、2407.17930（LSTM/GRU 预测比特币价格）；2506.09851（USD/BDT）、2411.04259（USD/TL）、2404.04461（外汇算法比较）；2512.21804（CNN S&P500，原稿为 2020 年）；2412.07223（BPNN+GA 波动率，会议质量弱）；2505.05646（课程报告级 VaR 比较）；2401.05441（ANFIS，IJCSIT）。
- 已撤稿：2510.07568（碳排放期货 ARIMA-TX-GARCH，作者已撤回）。
- 归属其他领域：电力日内市场的 LOB/价格预测（2509.04452、2502.06830、2609.23598、2403.05441）交给“能源与电力”；农产品价格 TSFM（2601.06371）、孟加拉农产品价格基准（2604.06227）不属于金融市场核心。
- 主要是交易系统或回测收益、预测评估很弱的：2511.08571（黄金期货 alpha）、2510.22348、2508.14784（外汇统计套利，以信息比率为主）、CS 方向的股票涨跌 GNN/LLM 论文（FinMamba 2502.06707、DGDNN 2401.01846、CSPO 2503.22740 等，同质化严重，且多以回测利润作证据），以及 LLM 情绪+涨跌预测类（2510.03633、2602.00086 等）。
- 非时间序列预测：2311.10685 High-Throughput Asset Pricing（策略挖掘与经验贝叶斯，评估价值高，但核心不是时间序列预测；已在笔记中记录，可作为数据窥探的扩展阅读）；2511.16375 破产预测（截面分类）；2608.11327 财报预测（另成方向，见第 5 节）。
- 相似主题择优：全球波动溢出只保留 GSP-HAR（2410.22706），没有收 2409.15320（同一作者的 STGNN 版本）；加密资产波动率保留概率预测 2508.15922，LGBM 版本 2511.20105 落选；TSFM 金融适配保留 Kronos 和若干批判性评测，FinCast 与 TimesFM 微调放入备选。
- 摘要中考察过但未选的：2603.16886（918 个实验的架构对比，单一作者，结论“方向准确率约 50%”有参考价值）、2605.09842（收益率曲线 ML vs 计量，期刊早于 arXiv，未入选）、2412.10540、2606.24062 等。

## 3. 子方向覆盖表（主列表 rank）

| 子方向 | rank |
|---|---|
| 已实现波动率（HAR vs ML、粗糙波动、期权信息、文本、体制） | 1, 2, 10, 14, 22, 23, 24, 25, 47, 50 |
| 协方差 / 多元波动 | 20, 21 |
| 隐含波动率曲面 | 26 |
| 尾部风险 VaR/ES（建模、组合、评价、窗口选择） | 11, 12, 15, 16, 17, 18, 19 |
| 股票收益 / 方向（日度、横截面、日内、LLM 智能体） | 3, 9, 39, 40, 43, 47 |
| 外汇 | 27, 28, 29（另有 2 号涵盖外汇资产） |
| 利率 / 收益率曲线 | 30, 31, 32, 33 |
| 加密资产 | 34, 35, 36（13 号含比特币 LOB 数据） |
| 高频 / LOB / 成交量 | 13, 37, 38, 39, 48, 49 |
| 金融时间序列基础模型 | 2, 4, 7, 8, 9, 33 |
| LLM 预测与前视偏差 / 记忆批判 | 5, 6, 25, 29, 43, 44 |
| 金融评估方法（基准公平、回测过拟合、检验功效） | 1, 3, 12, 36, 45 |
| 预警 / 崩盘风险 | 41, 42 |
| 跨资产 / 多资产 | 2, 3, 33, 46 |
| 异常检测（限量） | 48 |

明显缺口：
- 商品期货（原油、金属）专门的预测研究不足，主列表只通过 3 号与 46 号间接覆盖。铜期货波动率（2409.08356）因为属于 HAR vs RNN 的同质比较而没有收录。
- 信用 / CDS / 公司债利差的时间序列预测，以及系统性风险预警（如 CoVaR）偏少，后者只有备选 59 号。
- A 股的深度学习因子 / alpha 预测（Qlib 一类）没有覆盖，原因是候选多以回测收益为证据。
- 宏观-金融混频（MIDAS）类收益预测没有专门收录。

## 4. 优先阅读 10 篇

1. rank 1 — *HARd to Beat: The Overlooked Impact of Rolling Windows in the Era of Machine Learning*：HAR 拟合方案设定合理时，ML 无法胜出，是检验基准公平性的范例。
2. rank 2 — *Forecasting Realized Volatility with Time Series Foundation Models: A Comparison with Econometric Benchmarks*：用 MCS 和 MZ 回归拆解 TSFM 的“优势”来自哪里。
3. rank 3 — *How do standard time series forecasting benchmarks translate to finance?*：通用 SOTA 架构不如 AR(1)，说明通用基准的排名不能迁移到金融。
4. rank 4 — *Re(Visiting) Time Series Foundation Models in Finance*：现成 TSFM 在全球收益上效果差，需要在金融数据上从头预训练。
5. rank 5 — *The Memorization Problem: Can We Trust LLMs' Economic Forecasts?*：LLM 在训练覆盖期内的预测不可识别。
6. rank 6 — *Detecting Lookahead Bias in LLM Forecasts*：提出可操作的前视偏差检验（LAP）。
7. rank 7 — *FinVerse*：金融专用的 TSFM 基准，与 GIFT-Eval 的排名只中等相关。
8. rank 12 — *Evaluating financial tail risk forecasts: Testing Equal Predictive Ability*：DM/MCS 在 VaR/ES 上检验力不足。
9. rank 13 — *TLOB*：LOB 预测的最新代表，讨论可预测性衰减和价差成本。
10. rank 11 — *Combining a Large Pool of Forecasts of Value-at-Risk and Expected Shortfall*：尾部风险预测组合的系统研究。

## 5. 扩展领域建议

- 预测市场（Kalshi/Polymarket）的概率预测与基准：检索中出现较多，如 2604.01431、2604.14199、2602.00133、2602.21229，可独立收集，与“事件预测/LLM 预测评测”交叉。
- 宏观经济与通胀预测、现时预测（nowcasting）：econ.EM 中数量多。本领域只收金融市场变量，宏观部分建议单列。
- 公司财务报表 / 基本面长期预测：如 2608.11327 Forma 与 ProForma-20Q 基准，属面板预测，适合单列。
- 农产品与大宗商品价格：如 2601.06371 TSFM 农产品价格，可与“能源与电力”或单独的“商品”类合并。
- DeFi / 链上风险：如 2602.03981 DeXposure-FM、2602.03874 ASRI，属图与时间序列结合的风险监测。

## 6. 无法核实或存疑的条目说明

- 日期异常：arXiv API 的 `published`（v1）字段与编号前缀不一致的条目有 2608.26115（v1=2026-06-10）、2608.07536（v1=2026-07-28）、2606.00071（v1=2026-05-20）、2603.16886（v1=2026-02-27）等。JSON 中按 API 所示的 v1 日期记录，均在窗口内，建议协调人下载时再核对 arXiv 页面。
- rank 18（2603.02357）：arXiv v1 是 2026-03-02，但其 IJF DOI（10.1016/j.ijforecast.2025.12.002）显示期刊版可能更早上线（约 2025-12）。两者都在窗口内，JSON 用 arXiv v1。
- rank 50（2601.13014，旧文）：arXiv 元数据给出的 DOI 10.1093/jjfinec/nbac032 在 OpenAlex 中对应的是 2022-08-24 的“更正说明”（Correction），原论文上线更早，确切日期待全文核实。无论哪个日期都早于窗口，因此标为 old。期刊版本为 closed access，PDF 只走 arXiv。
- rank 49（2308.01915）：v1=2023-07-05，早于窗口，标为 old。
- 证据性质需要注意的：rank 29（AI 与汇率可预测性）、rank 43（LLM 智能体选股）、rank 44（ChronoGPT）、rank 46（多资产体制）的主要证据是策略收益或 Sharpe，summary 中已注明不能作为预测有效性证据。rank 3、7 的部分指标也是组合回测。
- 同行评审状态：大部分 2026 年条目只是 arXiv 预印本（未见 journal_ref）。已确认的期刊或会议条目有：rank 3（J. Forecasting）、10（AAAI'24）、14（JBES）、18（IJF）、25（ICAIF 2025）、32（ASTIN Bull.）、34（DSAA'25）、42（Emerging Markets Review）。
- 由于 OpenAlex 配额耗尽，没有补充 OA 期刊（非 arXiv）来源的金融文献。如需提高同行评审比例，可在配额恢复后用 OpenAlex 检索 IJF、JFEc、Quantitative Finance 的 OA 论文，替换部分备选。
