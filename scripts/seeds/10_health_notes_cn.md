# 10_health 医疗与公共卫生：检索与筛选说明

检索日期：2026-10-29。时间窗：首次公开日期在 2023-10-29 至 2026-10-29 之间。有 arXiv 版本的用 arXiv v1 日期；只有 medRxiv/期刊版本的，用 OpenAlex 记录中最早的公开日期（preprint 或期刊），并在 `date_source` 中注明。
产出：`scripts/seeds/10_health_seed_cn.json`，共 65 条：主列表 1–50，备选 51–65。主列表中近期文献 48 条，旧文 2 条（rank 49、50）。

## 1. 检索词与平台（实际使用）

所有检索都通过 `scripts/search_candidates_en.py`（arXiv API / OpenAlex，带共享限速）完成；WebSearch 只用过 1 次，用于发现文献。

**arXiv（`arxiv` 命令，日期自动过滤）**
- `abs:"glucose" AND (abs:forecast* OR abs:prediction) AND abs:"continuous glucose"`
- `abs:sepsis AND abs:"early prediction" AND abs:ICU`
- `abs:"influenza" AND abs:forecast* AND (abs:FluSight OR abs:ensemble)`
- `abs:sepsis AND (abs:prediction OR abs:"early warning") AND (abs:"time series" OR abs:temporal)`
- `abs:"acute kidney injury" AND abs:predict* AND (abs:ICU OR abs:EHR)`
- `abs:"clinical deterioration" AND (abs:"early warning" OR abs:forecast*)`
- `abs:"COVID-19 Forecast Hub" OR abs:"COVID-19 forecasting hub" OR abs:"Forecast Hub"`
- `abs:dengue AND abs:forecast*`
- `abs:"emergency department" AND (abs:forecast* OR abs:"visits") AND abs:"time series"`
- `abs:"hospital" AND (abs:"bed occupancy" OR abs:admissions) AND abs:forecast*`
- `abs:"blood pressure" AND abs:forecast* AND (abs:wearable OR abs:"time series")`
- `abs:"heart rate" AND abs:forecast* AND abs:wearable`
- `abs:"foundation model" AND (abs:ICU OR abs:"electronic health records" OR abs:wearable) AND abs:"time series"`
- `abs:"irregularly sampled" AND (abs:clinical OR abs:ICU OR abs:MIMIC) AND (abs:forecast* OR abs:prediction)`
- `abs:leakage AND (abs:sepsis OR abs:ICU OR abs:EHR) AND abs:prediction`
- `ti:"vital sign" AND abs:forecast*`（无结果）
- `abs:"early warning signals" AND (abs:epidemic OR abs:disease OR abs:outbreak)`（无结果）
- `abs:epidemic AND abs:"foundation model" AND abs:forecast*`
- `abs:hypoglycemia AND abs:predict* AND (abs:nocturnal OR abs:"prediction horizon")`
- `abs:benchmark AND abs:ICU AND abs:"time series" AND (abs:prediction OR abs:forecast*)`
- `abs:sepsis AND (abs:"label" OR abs:onset) AND (abs:evaluation OR abs:bias) AND abs:"early"`
- `abs:"large language model" AND abs:epidemic AND abs:forecast*`
- `abs:mood AND abs:forecast* AND (abs:wearable OR abs:smartphone OR abs:"ecological momentary")`
- `abs:"COVID-19" AND abs:hospitalization AND abs:forecast* AND abs:probabilistic`
- `abs:"atrial fibrillation" AND abs:forecast* AND abs:onset`
- `ti:"foundation models" AND ti:"vital sign"`
- `abs:"critical slowing down" AND (abs:epidemic OR abs:infectious OR abs:disease)`
- `ti:"time series foundation models" AND (abs:clinical OR abs:health OR abs:medical)`
- `abs:"wastewater" AND abs:forecast* AND abs:hospital*`（无结果）
- `abs:"respiratory" AND abs:"hub" AND abs:forecast*`

**OpenAlex（`openalex` 命令，均加 `--oa`；带 `[T]` 的用了 `--title`）**
- FluSight influenza hospitalization forecasts evaluation 2023-24
- COVID-19 Forecast Hub ensemble hospitalization forecasts evaluation
- dengue forecasting climate machine learning
- [T] emergency department visits forecasting
- [T] hospital bed occupancy forecasting
- wastewater surveillance forecasting COVID-19 hospital admissions
- sepsis early prediction machine learning external validation
- [T] acute kidney injury prediction continuous
- [T] seizure forecasting wearable
- disease progression forecasting longitudinal electronic health records deep learning
- Alzheimer disease progression forecasting multimodal longitudinal
- malaria incidence forecasting climate
- respiratory syncytial virus RSV forecasting
- nowcasting hospitalizations reporting delays Bayesian
- intraoperative hypotension prediction deep learning arterial waveform
- [T] mortality forecasting excess deaths time series（无结果）
- in-hospital cardiac arrest prediction early warning deep learning vital signs
- heat wave hospital admissions forecasting temperature
- [T] Learning the natural history of human disease with generative transformers
- time series foundation models vital sign forecasting
- seasonal influenza forecasting large language model
- COVID-19 Scenario Modeling Hub projections evaluation
- [T] hand foot mouth disease forecasting
- measles outbreak forecasting
- early warning outbreak detection syndromic surveillance forecasting
- [T] ambulance demand forecasting
- 按标题核对：Are Time Series Foundation Models Ready for Vital Sign Forecasting（OpenAlex 无记录）、GluFormer（无记录）、Zero shot health trajectory prediction using transformer、Scaling wearable foundation models、Forecasting seasonal influenza epidemics with PINN、Flusion、Dengue Forecasting Sprint Brazil、Post-processing and weighted combination of nowcasts、Fine-tuned LLMs enhance influenza forecasting、Can one model fit all（临床 TSFM）
- sepsis prediction data leakage；temporal dataset shift clinical prediction（均无结果）
- 以下 6 条遇到 OpenAlex 429 限流，未得到结果：forecasting hospital admissions ML temporal validation、Delphi epidemic nowcasting auxiliary indicators、[T] ICU occupancy forecasting、patient deterioration early warning ward vital signs、CGM forecasting foundation model、CKD eGFR trajectory prediction

**WebSearch（1 次）**：`"Are Time Series Foundation Models Ready for Vital Sign Forecasting in Healthcare" arXiv`，找到 PMLR v259 页面，并用 WebFetch 读取该页面的摘要和 PDF 链接。

**元数据核实**：候选文献逐条用 `abs`（arXiv id 或 DOI）取得完整摘要和全部 OA 位置。arXiv API 当时频繁返回 429，部分 arXiv 文献的摘要改从 OpenAlex 取（DOI 10.48550/arXiv.<id>）。这些文献的 v1 日期来自同一会话中 arXiv 检索的列表输出，或单独调用 `abs` 核实。

## 2. 纳入/排除原则与主要排除记录

**纳入原则**
- 核心任务必须有时间维度：优先预测（生理信号、ICU 轨迹、疾病进展、传染病、医疗资源需求），其次是预警（脓毒症、AKI、术中低血压、心搏骤停、癫痫、房颤）。
- 评测/泄漏/非平稳性类文献单独保留：WIS、分配评分、风险轨迹稳定性、部署式连续监测评测、预测因子关系的时间异质性。
- 不同目标、数据类型（可穿戴、ICU、EHR、监测）、跨度（分钟到 20 年）和方法（统计、ML、DL、基础模型、机理混合、扩散、LLM）尽量各取代表，不堆同质应用。
- 每条至少有 1 个合法 OA PDF 途径：arXiv、PMC、medRxiv、publisher OA 或机构库。

**主要排除记录**
- 早于时间窗的知名文献（未纳入，或仅作旧文）：
  - Cramer et al. 2022 PNAS（美国 COVID-19 Forecast Hub 集合评估）：2021 年预印本。
  - Sherratt et al. 2023 eLife（欧洲 COVID-19 Forecast Hub）：2023 年 4 月。
  - Reyna et al. PhysioNet 2019 脓毒症挑战。
  - Lopez et al. "Challenges of COVID-19 Case Forecasting in the US, 2020–2021"（PLoS CB 2024 期刊版）：预印本很可能早于窗口，未核实，故排除。
  - Howerton et al. Scenario Modeling Hub 评估（Nature Comms 2023-11-20）：在窗口内，但它是情景投影而非预测，且主列表名额已满，未纳入。
  - Reich et al. "COVID-19 case reports as leading indicator"（Epidemics 2023-11-07）：OpenAlex 上 Elsevier OA 未给 PDF 链接，未纳入。
- 只有摘要页、找不到 PDF 途径的：
  - Pucher et al. 2026 "Can one model fit all? …foundation models … clinical medicine"（AIIM，hybrid，OpenAlex 无 PDF）。主题高度相关，建议协调者另行查找作者稿。
  - Wolffram et al. 2026 SARI nowcast 集合（KIT 仓库有 PDF，但 OpenAlex 无摘要，无法写注释）。
  - Johnson et al. 2026 污水贝叶斯生成模型（medRxiv，OpenAlex 未给 PDF）。
- 方法过于平凡或来源存疑：大量 "LSTM/ARIMA 预测某地登革热/疟疾/手足口病" 类小刊论文（如 Kalutara、Bahir Dar、Chanthaburi、Qingdao CNN-BiLSTM 等），各病种只保留 1–2 篇代表。Zenodo/Figshare 上的非正式稿件和掠夺性期刊（IJAIRI、ShodhKosh、GSC 等）一律排除。
- 静态风险模型（入 ICU 时一次性预测死亡/并发症，无时间序列成分）大量排除，如多数 "sepsis-induced coagulopathy ML" 论文。
- 纯分类/异常检测（心律失常识别、PPG 血压估计、活动识别基础模型等）基本不纳入。主备两表中只有 1 条标为"分类"（rank 65，夜间低血糖）。

## 3. 子方向覆盖表

| 子方向 | 排名 |
|---|---|
| 血糖/CGM 预测（基准、基础模型、机理融合、LLM、联邦） | 2, 9, 27, 46；备选 58, 59, 60, 65 |
| 可穿戴生理信号（心率/HRV、血压、房颤、癫痫） | 8, 16, 34, 35, 36 |
| ICU 生命体征预测与基础模型 | 5, 11, 18, 32, 33；备选 61, 62 |
| ICU/住院恶化预警（脓毒症、AKI、低血压、心搏骤停、综合恶化） | 6, 22, 29, 37, 39；备选 57, 63 |
| 疾病进展建模（纵向 EHR、AD、化验预测） | 3, 23, 40, 41 |
| 传染病预测中心/集合评测（FluSight、Influcast、登革热 Sprint） | 1, 7, 21, 26 |
| 流感/呼吸道预测方法（ML 集合、扩散、PINN、ARIMAX、LLM、基础模型） | 4, 10, 12, 24, 42, 43, 44 |
| 即时预测（nowcasting，报告延迟） | 13, 30 |
| 污水监测与领先指标 | 20, 31；备选 53 |
| 其他传染病（登革热、疟疾、手足口病） | 7, 47, 48；备选 52 |
| 医疗资源需求（住院、床位、急诊） | 15, 19, 28, 45；备选 51, 54, 55, 56 |
| 评测、泄漏、可复现性与基准 | 14, 17, 20, 25, 38, 49, 50（另见 6 的部署式评测） |
| 综述 | 备选 64 |

**明显缺口**
- 中文/中国医疗资源需求预测（门诊量等）几乎没有收录：OpenAlex 中可核实 OA 全文的较少。
- RSV 单病原预测、超额死亡预测、救护车需求未找到合格候选。
- 明确讨论"标签泄漏/时间泄漏"的脓毒症文献未检到：arXiv 与 OpenAlex 的 leakage 检索均无合格结果。目前用 6、14、20、50 部分替代。
- 心理健康/情绪的可穿戴预测，以及 CKD/eGFR 轨迹预测，因限流未完成检索。
- 不规则采样方法只收了面向预测的 18、32、33。纯表示学习/分类的（如 TrajGPT、Set Transformer）未收。

## 4. 优先阅读 10 篇

1. rank 1 — Evaluation of FluSight influenza forecasting …：流感住院新目标下集合预报的权威前瞻评测，WIS/覆盖率评估范式。
2. rank 2 — GlucoBench：CGM 血糖预测的标准化数据集与基准。
3. rank 3 — Learning the natural history of human disease with generative transformers (Delphi-2M)：纵向 EHR 疾病进展生成式预测，有跨国外部验证。
4. rank 5 — Are Time Series Foundation Models Ready for Vital Sign Forecasting in Healthcare?：对 TSFM 用于生命体征预测给出审慎证据。
5. rank 6 — Deep learning models for AKI prediction … simulated continuous monitoring：揭示单点 AUROC 与连续部署表现的背离。
6. rank 10 — Generative diffusion models for spatiotemporal influenza forecasting (Influpaint)：扩散模型做时空流行病预测，有实时检验。
7. rank 12 — Mantis：仅用机理模拟预训练的传染病预测基础模型，以 Forecast Hub 为对照。
8. rank 14 — Stable Prediction of Adverse Events in Medical Time-Series Data (CAREBench)：把风险轨迹稳定性纳入预警评测。
9. rank 17 — Evaluating infectious disease forecasts with allocation scoring rules：评测与资源分配决策挂钩。
10. rank 20 — Rethinking respiratory disease forecasting: temporal heterogeneity …：监测预测因子与结局关系的非平稳性导致预测不稳定。

## 5. 扩展领域建议

- **气候-健康交叉**（登革热/疟疾/热浪住院）：候选很多但质量参差，可作为"气象与气候"与"医疗"的交叉子集单独收集。热浪与住院相关的文献多为关联分析而非预测，本次未纳入。
- **可穿戴/传感器基础模型**（LSM、PPG/ECG 基础模型）：数量增长很快，但多数以分类/表征为主，适合单独建"生理信号表征学习"子库。
- **EHR 生成式基础模型**（Delphi-2M、ETHOS、CEHR-GPT 类）：可单独追踪，重点看时间外推与校准。
- **预测中心生态**（FluSight、COVID/RSV Hub、欧洲 Respicast、德国 Nowcast Hub、Scenario Modeling Hub）：建议单独做"集合预报与评测"子集，兼顾情景投影。
- **污水流行病学预测**：方法正在从相关性分析走向时变因果建模，值得持续跟踪。

## 6. 无法核实或存疑条目说明

- rank 5（Gu, PMLR v259）：没有找到 arXiv 版。首次公开日期取 PMLR 卷页面信息（年份 2025、编辑链接日期 2025-02-17），会议日期为 2024-12-15/16，两者都在窗口内。摘要来自 PMLR 页面（经 WebFetch 转述），`field_basis` 已注明。PDF 有两条 PMLR 路径，需协调者核验。
- rank 23（ETHOS）：arXiv 2407.21124 的 v1 精确日期因 arXiv API 限流未取到（编号对应 2024-07）。目前填的是 medRxiv 预印本日期 2024-02-29（OpenAlex 位置记录）。两者都在窗口内，但严格按规则应改用 arXiv v1 日期，待核实。
- rank 3（Delphi-2M）：OpenAlex 未给直接 PDF。pdf_candidates 中的 nature.com `.pdf` 和 medRxiv `v1.full.pdf` 是按出版社/medRxiv 标准路径构造的；另有 Europe PMC 稿（PMC12589094）可作后备。
- rank 19（Tobin）：medRxiv 预印本日期是按 DOI（2024.10.13）推断的。期刊版 2025-08-12 也在窗口内。
- rank 44（Li, Cell Reports Methods）：期刊版日期为 2026-07-23；medRxiv 预印本（10.1101/2025.03.27.25324747）的确切日期未核实，两者都在窗口内。PDF 用 PMC 版。
- rank 28（Guo）：arXiv 题名（High-dimensional point forecast combinations…）与期刊题名（Ascertaining cause-specific ED demand using forecast combinations）不同。条目沿用 arXiv 题名，venue 字段注明了期刊题名。
- rank 49（Bracher, PLoS CB 链接）和 rank 55（Crisafulli, PLoS ONE 链接）中的 PLOS PDF 是按 PLOS 标准 printable 路径构造的，arXiv 为主路径。
- 部分摘要在 OpenAlex/arXiv 返回中被截断：rank 11、53、57、64 等的具体指标标为"待全文核实"。Flusion（rank 4）摘要后半段被截断，其在 FluSight 中的表现需全文确认。
- rank 50（YAIB）：OpenAlex arXiv 记录日期为 2023-06-08，是否为 ICLR 2024 正式论文待核实。
