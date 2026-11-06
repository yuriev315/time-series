# 检索日志（初步范围检索）

- 检索执行日期：2026-10-29（UTC）
- 时间窗口：以“首次公开日期”判断，2023-10-29 至 2026-10-29（检索日向前滚动三年）
- 最新覆盖：本库收录文献中首次公开日期最晚为 2026-09-11（TS014）；arXiv 检索结果最晚见到 2026-10 下旬提交的条目，但未纳入（理由见下文“排除记录”）
- 性质：初步范围检索，不是系统综述，不宣称穷尽。

## 1. 使用的平台与用途

| 平台 | 用途 | 是否作为最终元数据来源 |
|---|---|---|
| 通用网页搜索（WebSearch） | 发现候选、了解近期热点与评测争议 | 否，仅用于发现 |
| arXiv API（export.arxiv.org/api/query） | 带日期过滤的标题检索；批量获取标题、作者、v1 提交日、最新版本号与日期、comments、journal_ref、DOI、摘要 | 是 |
| Crossref REST API | 有 DOI 文献的标题、作者、期刊、卷期页、出版年 | 是 |
| OpenAlex API | 查询旧文献的开放获取位置（仓储、作者主页） | 仅定位 PDF |
| 官方论文集索引页 | 会议渠道核验：PMLR v235（ICML 2024）、v267（ICML 2025）、v258（AISTATS 2025），NeurIPS 2024/2025、ICLR 2024/2025 论文集，PVLDB vol 17 | 是（渠道） |
| NeurIPS 2025 单篇官方页面 | TiRex 渠道核验（NeurIPS 2025 索引页当时内容不完整） | 是（渠道） |
| DBLP 搜索 API | 计划用于渠道核验；实际返回 HTTP 429/202（限流），未使用其结果 | 否 |
| OpenReview API | 尝试核验 TMLR 渠道，未返回可用结果 | 否 |
| 作者主页 / 期刊官网 | 旧文献 PDF（robjhyndman.com、华盛顿大学 Raftery 主页、jstatsoft.org） | 是（PDF 与版本） |

## 2. 检索词

### 2.1 网页搜索（用于发现）
- `arXiv 2025 time series foundation model zero-shot forecasting Chronos-2 TiRex Toto Sundial`
- `fev-bench realistic benchmark time series forecasting arXiv 2025`
- `"no champions" long-term time series forecasting position paper benchmarking arXiv`
- `time series foundation models evaluation data leakage pretraining test overlap arXiv 2025`
- `2026 arXiv time series forecasting foundation model benchmark survey evaluation`
- `TiRex xLSTM zero-shot forecasting arXiv; Toto ... observability arXiv; Moirai 2.0 arXiv`
- `arXiv 2024 2025 seasonal-trend decomposition time series new method`
- `change point detection structural break time series review 2024 2025 arXiv`
- `non-stationary time series forecasting normalization 2024 2025 arXiv frequency adaptive normalization test-time adaptation`
- `frequency domain time series forecasting survey 2024 2025 arXiv spectral`
- `conformal prediction time series forecasting intervals 2024 2025 arXiv`
- `evaluating probabilistic multivariate time series forecasts scoring rules CRPS energy score calibration arXiv 2024 2025`
- `exponential smoothing ARIMA statistical forecasting new method 2024 2025 International Journal of Forecasting arXiv`
- `gradient boosted trees versus deep learning time series forecasting benchmark 2024 2025 arXiv global models`
- `time series forecasting evaluation cross-validation rolling origin data leakage look-ahead bias 2024 2025 arXiv`
- `fine-tuning adaptation time series foundation models in-context fine-tuning covariates ChronosX arXiv 2024 2025`
- `vector autoregression forecasting large Bayesian VAR 2024 2025 arXiv`
- `Kalman filter state space model forecasting deep learning 2024 2025 arXiv Mamba time series forecasting effective`

### 2.2 arXiv API 检索（均附加 `submittedDate:[202310290000 TO 202610292359]`，按相关度取前 25 条）
- `ti:"exponential smoothing"`
- `ti:ARIMA AND abs:forecast`
- `ti:"structural break" AND abs:"time series"`
- `ti:"change point" AND (ti:review OR ti:survey OR ti:benchmark)`（0 条）
- `(ti:"change point" OR ti:changepoint OR ti:"change-point") AND (abs:review OR abs:survey)`
- `ti:"state space" AND ti:forecasting`
- `ti:"unit root" OR ti:stationarity AND abs:"time series"`
- `ti:conformal AND ti:"time series"`
- `ti:"cross-validation" AND abs:"time series"`
- `ti:"gradient boosting" AND ti:forecasting`
- `ti:"time series" AND ti:features AND abs:forecasting`
- `ti:"scoring rules" AND abs:forecast`
- `ti:calibration AND ti:forecast AND abs:"time series"`
- `ti:decomposition AND ti:seasonal`
- `ti:"vector autoregress" AND abs:forecast`
- `ti:global AND ti:forecasting AND abs:local`
- `ti:"time series" AND ti:forecasting AND ti:survey`
- `ti:"foundation model" AND ti:"time series" AND (ti:"fine-tuning" OR ti:adaptation OR ti:"in-context")`
- `(ti:LSTM OR ti:recurrent OR ti:xLSTM) AND ti:"time series forecasting"`
- `ti:linear AND ti:"time series forecasting" AND abs:baseline`

前向/后向引用：未系统执行引用链检索（无可用的引用 API 配额）；部分候选来自已知核心文献的“相关工作”关系（如 DLinear → CATS/SparseTSF/Toner；GIFT-Eval/fev-bench → Chronos-2/TiRex/TabPFN-TS；TSFM 泄漏 → TempusBench）。这是本轮的方法局限。

## 3. 纳入原则
1. 直接研究时间序列分析、预测、基础模型或预测评测；通用 ML 论文本轮未纳入。
2. 首次公开日期（arXiv v1 提交日或正式出版日）在窗口内；旧论文近期更新的版本不算新研究。
3. 每个主题既有方法论文也有评测/批评，避免只收最新模型。
4. 优先原始研究，辅以少量综述（本库综述/教程 8 篇：TS003、TS012、TS013、TS014、TS016、TS023、TS044，以及指南性质的 TS009）。
5. 元数据可在原始来源（arXiv / Crossref / 官方论文集）核验。
6. 三年前文献最多 5 篇，仅限基础方法、评测依据或经典基线，逐篇写明保留理由（见 catalog 的“三年前保留理由”列）。

## 4. 排除记录（主要）
| 文献 | 排除原因 |
|---|---|
| TimesFM（arXiv 2310.10688，v1 2023-10-14） | 首次公开早于窗口起点 15 天；旧文献名额已用于评测依据与基线 |
| iTransformer（2310.06625，2023-10-10）、Time-LLM（2310.01728，2023-10-03）、LLMTime（2310.07820，2023-10-11）、Lag-Llama（2310.08278，2023-10-12）、TimeGPT（2310.03589，2023-10-05） | 同上，首次公开在窗口前 |
| PatchTST（2211.14730）、N-BEATS、N-HiTS、DeepAR、TFT、Informer、Autoformer、TimesNet、TCN | 早于窗口；概念在近三年文献中均有回顾（TS023、TS044） |
| STL（1990）、MSTL（arXiv 2021，期刊 2025）、ADF/KPSS、Kalman、Bai-Perron、Prophet、M4/M5 竞赛总结、Gneiting 校准与锐度（2007）等经典文献 | 窗口外；旧文献名额限制为 5 篇。MSTL 的期刊版虽为 2025 年，但首次公开为 2021 年（arXiv），按规则不算新研究 |
| Hyndman & Athanasopoulos《Forecasting: Principles and Practice》 | 在线教材，非窗口内论文；可作背景读物，未纳入目录 |
| Moirai 2.0（2511.11698）、MOMENT（2402.03885）、Mamba4Cast（2410.09385） | 相关但与已收录模型重复度高，控制总数 |
| MultiDimSPCI（2403.03850）、Bellman 共形（2402.05203）等共形方法 | 已有综述 TS016 与统计方向 TS017 覆盖，控制总数 |
| Chan 等大型贝叶斯 VAR 条件预测（2407.02262） | VAR 已有 TS012、TS013 覆盖，控制总数 |
| FoundTS（2410.11802） | 与 GIFT-Eval/TFB/fev-bench 功能重叠 |
| “Deep Time-Series Forecasting in 10 Years: A Survey”（2603.19899） | 与 TS023 重叠，择一 |
| MetaARIMA（2610.34171，2026-10-25 提交） | 提交仅数日、尚无独立评价，暂不纳入 |
| 大量 ARIMA 应用案例论文（股价、疫情等） | 方法贡献弱，属应用 |
| 变点检测深度学习综述（Frontiers of Engineering Management 2025）、Annual Review 变点综述（2025） | 未在原始来源核验到可合法下载的 PDF 与完整元数据，本轮未纳入，列为后续核实对象 |

## 5. 候选名单调整记录
- 第一版候选（62 篇，兼顾经典）在下载前按用户更新的时间窗口规则整体替换，**未下载任何旧版候选**。
- 第二版（最终）：53 篇近三年 + 5 篇三年前 = 58 篇。

## 6. 下载规则执行情况
- arXiv PDF 请求间隔 ≥4 秒，其他主机 ≥3 秒；每个 URL 最多 3 次尝试；401/402/403/404/451 立即停止不重试。
- 未尝试任何需要登录、付费或验证码的页面；OpenAlex 标为“非开放”的出版社链接未请求。
- 每个文件下载到独立的空暂存目录，核验通过后才移入 pdfs/。
