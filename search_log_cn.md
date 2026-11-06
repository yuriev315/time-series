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

---

# 第二轮：多领域扩展（2026-10-29）

## 7. 任务与分工
- 范围扩展为 10 个分类（通用方法 + 9 个应用领域），每类目标约 50 篇“已核验全文”论文；新增大学课程讲义（目标约 50 套）与书籍（目标约 50 本），单独统计。
- 检索、筛选与摘要级标注由各分类独立的检索代理执行。它们按统一简报工作：时间窗口、相关性标准、合法全文路线、字段定义均一致。每类提交 50 篇主选 + 15 篇备选（水质另补 25 篇），并写检索笔记。
- 元数据核验、下载、全文核验、去重、计数和目录生成，由协调脚本统一完成；检索代理提供的元数据一律以 arXiv/Crossref/OpenAlex/出版方页面重新核实。

## 8. 各分类检索记录
每类的检索词、平台、纳入/排除记录、子方向覆盖、缺口与扩展建议，见对应笔记：

| 分类 | 检索笔记 |
|---|---|
| 金融 | [scripts/seeds/02_finance_notes_cn.md](scripts/seeds/02_finance_notes_cn.md) |
| 空气质量 | [scripts/seeds/03_air_quality_notes_cn.md](scripts/seeds/03_air_quality_notes_cn.md) |
| 水质 | [scripts/seeds/04_water_quality_notes_cn.md](scripts/seeds/04_water_quality_notes_cn.md)；补充检索 [04_water_quality_supp_notes_cn.md](scripts/seeds/04_water_quality_supp_notes_cn.md) |
| 气象与气候 | [scripts/seeds/05_weather_climate_notes_cn.md](scripts/seeds/05_weather_climate_notes_cn.md) |
| 能源与电力 | [scripts/seeds/06_energy_power_notes_cn.md](scripts/seeds/06_energy_power_notes_cn.md) |
| 水文与水资源 | [scripts/seeds/07_hydrology_notes_cn.md](scripts/seeds/07_hydrology_notes_cn.md) |
| 交通与出行 | [scripts/seeds/08_transport_notes_cn.md](scripts/seeds/08_transport_notes_cn.md) |
| 工业与设备 | [scripts/seeds/09_industrial_notes_cn.md](scripts/seeds/09_industrial_notes_cn.md) |
| 医疗与公共卫生 | [scripts/seeds/10_health_notes_cn.md](scripts/seeds/10_health_notes_cn.md) |
| 大学讲义 | [scripts/seeds/materials_courses_notes_cn.md](scripts/seeds/materials_courses_notes_cn.md) |
| 书籍 | [scripts/seeds/materials_books_notes_cn.md](scripts/seeds/materials_books_notes_cn.md) |

通用方法类沿用第一轮的 58 篇，新增字段（任务类型、预测目标、数据集等）依据摘要补充。

## 9. 检索受限情况（影响覆盖面）
- 多个检索代理并行工作期间，本机 IP 访问 arXiv API 与 OpenAlex 检索接口频繁返回 HTTP 429。交通、能源、水文、金融类的 OpenAlex 关键词检索几乎全部失败；单篇 DOI 查询多数可用。
- 后果：
  - 没有 arXiv 版本的期刊论文在这些类中偏少，例如交通的 TR-C/T-ITS、能源的 WES/Solar Energy、金融的 JFEC/IJF 开放获取文章。
  - 气象类的季节预测和湿度主题检索未能执行。
- 这些缺口已在各类笔记中列出；限流解除后可补检。

## 10. 时间资格核验
- 统一以首次公开日期判断：
  - arXiv v1；
  - Crossref 在线、印刷、posted、created 日期中最早者；
  - Crossref `has-preprint` 关系登记的预印本或讨论稿（如 EGUsphere、HESSD、ESSOAr、medRxiv、Research Square）。
- 日期选择规则：精确到日的日期优先；只有当月或年精度日期的整个区间都早于该日时，才取月/年精度日期。OpenAlex 日期仅在缺少其他来源时作为兜底（它会把月份补齐为 1 日）。
- 典型修正：
  - 金融 2601.13014 的 arXiv 元数据把 DOI 写成期刊更正声明，经 Crossref 检索改为原文 DOI 10.1093/jjfinec/nbac020，首次公开日期为 2022-06-21，按三年前文献计。
  - TS097、TS254 等期刊版改了题名，题名比对同时接受 arXiv 版与期刊版题名。
- 交通类 2 篇（2412.03307、2403.09969）的 arXiv v1 在窗口内，但 journal_ref 显示已在 ITSC 2023 正式发表，首次公开早于窗口，因此排除。

## 11. 执行中的问题与修复（如实记录）
1. **完整性检查误判**：下载脚本最初在文件句柄尚未关闭时比较文件大小与 Content-Length，导致约 50 篇实际完整的 PDF 被误判为“截断”。发现后停止运行、修复脚本，只对因此失败（以及因旧题名比对规则失败）的条目重新下载；其他失败条目不重复请求。
2. **作者核验**：PDF 中德语姓氏写作转写形式（Schlüter → Schlueter），已支持转写匹配。
3. **参考文献节识别**：增加单数形式 “Reference:”。
4. **错误文献**：TS156 的开放获取链接实际指向 CSIRO 2020 年项目报告，记为“下载错文献”失败并删除文件。
5. **不可用来源**：
   - 下列出版社对自动下载返回 403：Wiley/AGU、ACS、PNAS、RSC、AMS、Elsevier。
   - PMC 与 Europe PMC 返回网页或 Cloudflare 挑战页；ResearchSquare、ESSOAr 也不可用。
   - 以上均记为失败，未尝试绕过，并按排名用备选论文补位。水质类因此追加了一轮补充检索。

## 12. 学习资料检索
- 来源：
  - 官方课程主页（MIT OCW、各大学课程页）；
  - 作者主页；
  - 出版社开放获取页面；
  - 机构页面。
- OAPEN/DOAB 对本机返回 403，未能系统检索。
- Springer OA 书页面对直连返回机器人验证页（Client Challenge）；下载阶段只做普通请求，遇到验证页即记失败，不绕过。
- 协调人剔除的条目：
  - 1 条期刊长综述（不是书籍）；
  - 1 套主页上仅以 HTML 注释形式存在、未公开列出的讲义；
  - 1 套缺第 10 讲的不完整讲义。
