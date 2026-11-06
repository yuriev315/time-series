# 时间序列分析与预测：系统阅读指南

**使用说明（请先读）**
- 本指南只引用已下载并核验通过的资料。论文见各分类的 `domains/<分类>/reading_map_cn.md`，讲义见 [university_materials/catalog_cn.csv](university_materials/catalog_cn.csv)，书籍见 [books/catalog_cn.csv](books/catalog_cn.csv)。
- “已核验”只表示检查过文件完整性、目录，以及标题与作者是否一致。**本库没有精读任何资料**，下文的章节推荐都依据已检查的目录（PDF 书签、正文 Contents 页、讲义包文件标签或 HTML 章节页）。凡是目录无法提取的资料，只推荐整体阅读，不编造章节号。
- 难度标注（入门/进阶/高级）来自检索阶段对官方页面描述的判断，仅供参考。

---

## 1. 入门路线：统计基础 → 经典时间序列 → 预测评测

| 步骤 | 资料 | 建议内容（依据已检查目录） |
|---|---|---|
| 1 统计与概率底子 | BK034 Deisenroth 等《Mathematics for Machine Learning》[PDF](books/files/Deisenroth_MathematicsMachineLearning_1stedition_2020_en.pdf)；BK032 Durrett《Essentials of Stochastic Processes》[PDF](books/files/Durrett_EssentialsStochasticProcesses_3rdeditionPDFVersion39May2021_2021_en.pdf) | 线性代数、概率与马尔可夫链基础；已有统计基础可跳过 |
| 2 应用时间序列入门 | UM058 ETH Dettling《Applied Time Series Analysis》讲义（SS 2016）[PDF](university_materials/files/ETHZurichSeminarStat_AppliedTimeSeriesAna_2016_en.pdf) | 正文目录：第 4 章描述性分析、第 5 章平稳模型、第 6 章 SARIMA 与 GARCH、第 7 章时间序列回归、第 8 章预测、第 9 章多变量、第 10 章谱分析、第 11 章状态空间 |
| 3 预测实践主教材 | BK001 Hyndman & Athanasopoulos《Forecasting: Principles and Practice》第 3 版，官方 HTML 离线包 [zip](books/files/Hyndman_ForecastingPrinciplesPractice3rdEd_3rdeditionPythonForecastingPrinciplesandPracticethePythonicWay_2021_html_en.zip) | 已检查的章节页：graphics → decomposition → features → toolbox → regression → exponential-smoothing → arima → dynamic-regression → hierarchical-forecasting → advanced → practical |
| 4 配套课程 | UM003 Monash ETC3550/5550 讲义包 [目录](university_materials/files/MonashUniversity_ETC3550ETC5550_2026/)；UM002 Berkeley Stat 153（Tibshirani, Fall 2023）[目录](university_materials/files/UniversityCalifornia_Stat153_2023/) | Monash 课程与 FPP3 同步；Berkeley 课程补充回归、正则化与谱分析视角 |
| 5 预测评测 | BK001 的 toolbox 章（评估、时间序列交叉验证）；通用方法类论文 TS055（MASE）、TS056（正常评分规则）、TS057（时间序列交叉验证）、TS048、TS049（评测批评与泄漏）——见 [domains/01_general_methods/reading_map_cn.md](domains/01_general_methods/reading_map_cn.md) | 先掌握点预测指标与滚动原点评估，再读概率评分与泄漏问题 |
| 6 季节调整（官方统计实务） | BK025 Eurostat《Handbook on Seasonal Adjustment》2018 [PDF](books/files/Mazzi_HandbookSeasonalAdjustment2018Edition_2018edition_2018_en.pdf) | 书签目录：Pre-Treatment Methods、Seasonal Adjustment Methods、Improving End-Point Estimates、Seasonal Adjustment of High Frequency Data |

## 2. 理论路线：随机过程 → 谱分析 → 状态空间与多变量方法

| 步骤 | 资料 | 建议内容 |
|---|---|---|
| 1 平稳过程理论 | UM021 van der Vaart《Time Series》讲义（UvA 2010–11）[PDF](university_materials/files/UniversiteitVanAmste_ST410016_2010_en.pdf)；UM029 Oslo STK4060（Autumn 2025）[目录](university_materials/files/UniversityOslo_STK4060STK9060_2025/) | UM021 未提取到目录，建议整体阅读（据课程页描述，覆盖平稳性、预测、弱相依 CLT、谱理论、ARMA/GARCH、状态空间）；UM029 为近年同类课程 |
| 2 时间序列计量理论 | UM006 MIT 14.384（Mikusheva, Fall 2013）讲义包 [目录](university_materials/files/MassachusettsInstitu_14384_2013/) | 共 23 个讲义文件（Lecture 1–26）；据课程页，涵盖 HAC、谱估计、VAR/SVAR、因子模型、单位根与结构突变 |
| 3 谱分析 | BK011 Stoica & Moses《Spectral Analysis of Signals》[PDF](books/files/Stoica_SpectralAnalysisSignals_PDF2004_2005_en.pdf)；UM032 MIT 12.864 Wunsch 讲义 [目录](university_materials/files/MassachusettsInstitu_12864_2005/) | BK011 正文目录：第 2 章非参数方法、第 3 章有理谱参数方法、第 4 章线谱参数方法；UM032 偏地球物理应用 |
| 4 状态空间与 Kalman | BK002 Särkkä & Svensson《Bayesian Filtering and Smoothing》第 2 版 [PDF](books/files/Sarkka_BayesianFilteringSmoothing2ndEd_2ndedition_2023_en.pdf)；UM015 Colorado ECE5550 Applied Kalman Filtering [目录](university_materials/files/UniversityColoradoCo_ECE5550_NA/) | BK002 书签目录：第 5 章状态空间建模、第 6 章滤波方程与精确解（Kalman）、第 7–10 章非线性高斯滤波、第 11 章粒子滤波、第 12–15 章平滑、第 16 章参数估计 |
| 5 非线性与非平稳 | UM014 DTU 02427 Madsen & Holst 课程教材 [PDF](university_materials/files/TechnicalUniversityD_02427_2026_en.pdf)；UM061 Edinburgh ECNM11049（2026）[目录](university_materials/files/UniversityEdinburghS_ECNM11049_2026/) | UM014 正文目录：第 1 章非线性时间序列模型、第 2 章非参数方法、第 3 章识别（后续章节目录未完整提取）；UM061 覆盖门限、马尔可夫转换、时变参数 |
| 6 多变量与贝叶斯宏观 | BK023 Koop & Korobilis《Bayesian Multivariate Time Series Methods for Empirical Macroeconomics》[PDF](books/files/Koop_BayesianMultivariateTimeSeriesMethods_MPRAPaper20125_2010_en.pdf)；BK024 Blake & Mumtaz《Applied Bayesian econometrics for central bankers》[PDF](books/files/Blake_AppliedBayesianEconometricsCentralBanker_updated2017_2017_en.pdf) | BVAR、时变参数 VAR、动态因子模型 |
| 7 粒子方法进阶 | UM016 Linköping SMC 博士课程 [目录](university_materials/files/LinkopingUniversityI_PhDcourse6credits_2025/)；BK030 Naesseth 等《Elements of Sequential Monte Carlo》[PDF](books/files/Naesseth_ElementsSequentialMonteCarlo_arXivv3202412_2024_en.pdf) | BK030 书签目录：重要性抽样到 SMC、学习提议分布、嵌套 MC、条件 SMC |

## 3. 现代方法路线：机器学习 → 深度学习 → 基础模型与概率预测

| 步骤 | 资料 | 建议内容 |
|---|---|---|
| 1 统计学习与评估 | BK019 Hastie 等《The Elements of Statistical Learning》第 2 版 [PDF](books/files/Hastie_ElementsStatisticalLearning2ndEd_2ndedition12thprintingcorrectedJan2017_2009_en.pdf)；BK035 Hardt & Recht《Patterns, Predictions, and Actions》[PDF](books/files/Hardt_PatternsPredictionsActionsFoundationsMac_1steditionarXiv_2022_en.pdf) | 模型评估、交叉验证、集成方法；BK035 讨论数据集、基准与可复现性 |
| 2 时间序列机器学习 | UM012 ENS Paris-Saclay MVA《Machine Learning for Time Series》[目录](university_materials/files/ENSParisSaclayMaster_MachineLearningTimeS_2026/) | 特征提取、缺失值插补、变点与异常检测 |
| 3 深度学习基础 | BK016 Zhang 等《Dive into Deep Learning》[PDF](books/files/Zhang_DiveIntoDeepLearning_PyTorchPDF_2023_en.pdf)；BK017 Prince《Understanding Deep Learning》[PDF](books/files/Prince_UnderstandingDeepLearning_PDFv503GitHubrelease20260209_2023_en.pdf) | 循环网络、注意力与 Transformer 相关章节 |
| 4 深度时间序列预测 | UM011 Tavenard《Deep Learning for Time Series》[目录](university_materials/files/InstitutPolytechniqu_DeepLearningTimeSeri_NA/)；论文：通用方法类 D、E 两节（TS023 综述、TS031 线性基线、TS032/TS040 Chronos 系列、TS043 LLM 批评） | 先读 UM011 建立框架，再按 [通用方法阅读路线](domains/01_general_methods/reading_map_cn.md) 读论文 |
| 5 概率建模 | BK006 Murphy《Probabilistic Machine Learning: Advanced Topics》[PDF](books/files/Murphy_ProbabilisticMachineLearningAdvancedTopi_1steditionPDF20251210_2023_en.pdf) | 书签目录只有部分级（Fundamentals / Inference / Prediction / Generation / Discovery / Action），建议读 Inference 与 Prediction 两部分中状态空间与序列相关的章节（具体章号待全文核实） |
| 6 预测区间与校准 | BK008 Angelopoulos & Bates《A Gentle Introduction to Conformal Prediction》[PDF](books/files/Angelopoulos_GentleIntroductionConformalPredictionDis_arXivv620221207_2022_en.pdf)；UM010 Berkeley Stat 241B（Spring 2024）[目录](university_materials/files/UniversityCalifornia_Stat241BCS281B_2024/) | BK008 书签目录：第 1–3 章共形预测与评估、第 4 章扩展（含分布漂移）；再读论文 TS016、TS017（时间序列共形） |
| 7 在线学习与非平稳 | BK036 Orabona《Online Learning》[PDF](books/files/Orabona_OnlineLearningModernIntroductionConvex_arXivv1020260621_2026_en.pdf) | 遗憾界与在线预测，配合论文 TS004、TS005（非平稳） |
| 8 结构突变与异常 | UM013 Lancaster MATH337 变点检测 [PDF](university_materials/files/LancasterUniversity_MATH337_2024_en.pdf)；BK012 Castle & Hendry《Modelling our Changing World》[PDF](books/files/Castle_ModellingOurChangingWorld_1stedition_2019_en.pdf)；UM041 Bucharest 异常检测课程 [目录](university_materials/files/UniversityBucharestF_AnomalyDetection_2025/) | BK012 书签目录：第 4 章趋势与突变、第 5 章 Indicator Saturation、第 7 章预测 |

## 4. 应用路线（与已有论文关联）

| 领域 | 先读资料 | 再读论文 |
|---|---|---|
| 金融 | BK022 Sheppard《Financial Econometrics Notes》[PDF](books/files/Sheppard_FinancialEconometricsNotes_20202021_2021_en.pdf)（书签：单变量与多变量时间序列、单变量波动率、VaR/ES 与密度预测、多元波动率与 copula）；UM009 Oxford MFE 课程 [目录](university_materials/files/UniversityOxfordMScF_MFE_2021/) | [金融阅读路线](domains/02_finance/reading_map_cn.md)：HAR 与 ML 的公平比较、LLM 前视偏差 |
| 环境（空气质量、气象） | BK007 Wikle 等《Spatio-Temporal Statistics with R》[PDF](books/files/Wikle_SpatioTemporalStatisticsR_1stedition_2019_en.pdf)（正文目录：第 2 章探索性分析、第 3 章时空统计模型、第 4 章描述性时空模型）；UM040 KSU STAT 764 时空统计 [zip](university_materials/files/KansasStateUniversit_STAT764_2020_html_en.zip)；BK028 Evensen 等《Data Assimilation Fundamentals》[PDF](books/files/Evensen_DataAssimilationFundamentalsUnifiedFormu_1stedition_2022_en.pdf) | [空气质量](domains/03_air_quality/reading_map_cn.md)、[气象与气候](domains/05_weather_climate/reading_map_cn.md) |
| 水质 | BK027 USGS《Statistical Methods in Water Resources》[PDF](books/files/Helsel_StatisticalMethodsWaterResourcesUSGS_2020editionTWRI4A3v112002_2020_en.pdf)；BK044 USGS EGRET/WRTDS 用户指南 [PDF](books/files/Hirsch_UserGuideExplorationGraphicsRivEr_2015_2015_en.pdf) | [水质阅读路线](domains/04_water_quality/reading_map_cn.md) |
| 水文 | BK042 WMO《Manual on Flood Forecasting and Warning》[PDF](books/files/Organization_ManualFloodForecastingWarningWMO_2011edition_2011_en.pdf)；BK028 数据同化 | [水文与水资源阅读路线](domains/07_hydrology/reading_map_cn.md) |
| 能源 | BK026 Haben 等《Core Concepts and Methods in Load Forecasting》[PDF](books/files/Haben_CoreConceptsMethodsLoadForecasting_1stedition_2023_en.pdf)（书签：第 5 章核心概念、第 7 章评估、第 9–11 章基准/ML/概率方法、第 14 章低压负荷案例）；UM060 DTU 31761 Pinson [目录](university_materials/files/TechnicalUniversityD_31761_2018/) | [能源与电力阅读路线](domains/06_energy_power/reading_map_cn.md) |
| 工业 | UM063 林雪平预测性维护课程（RUL 与退化建模）；UM016 粒子方法与 BK002 状态空间；UM041 异常检测 | [工业与设备阅读路线](domains/09_industrial/reading_map_cn.md)：先读数据切分与泄漏批评论文 |
| 交通、医疗 | BK007 时空统计；UM001 Michigan STATS 531（POMP 与流行病案例）[目录](university_materials/files/UniversityMichigan_DATASCISTATS531631_2025/) | [交通](domains/08_transport/reading_map_cn.md)、[医疗与公共卫生](domains/10_health/reading_map_cn.md) |

## 5. 核心书单（优先 14 项）

章节建议都依据已检查的目录，内容未精读。

| # | 资料 | 用途 | 章节建议 |
|---|---|---|---|
| 1 | BK001 FPP3（HTML 离线包） | 预测实践总纲 | 全书；评测看 toolbox、层级看 hierarchical-forecasting |
| 2 | UM058 ETH Dettling 讲义 | 应用时间序列一站式入门 | 第 4–8 章，后续第 10、11 章 |
| 3 | UM003 Monash ETC3550 | 与 FPP3 配套的课程节奏 | 全部讲义 |
| 4 | UM021 van der Vaart 讲义 | 平稳过程与渐近理论 | 整体阅读（目录未提取） |
| 5 | BK011 Stoica & Moses | 谱估计 | 第 2–4 章 |
| 6 | BK002 Särkkä & Svensson | 状态空间、Kalman 与粒子滤波 | 第 5–8、11–12、16 章 |
| 7 | UM014 Madsen & Holst（DTU 02427） | 非线性、非平稳与自适应估计 | 第 1–3 章起 |
| 8 | UM006 MIT 14.384 | 时间序列计量（HAC、VAR、单位根、突变） | 按讲次顺序 |
| 9 | BK022 Sheppard 金融计量笔记 | 波动率与风险预测 | “Analysis of a Single Time Series”“Univariate Volatility Modeling”“Value-at-Risk, ES and Density Forecasting” |
| 10 | BK007 Wikle 等 | 时空统计 | 第 2–4 章 |
| 11 | BK008 Angelopoulos & Bates | 预测区间与校准 | 第 1–4 章 |
| 12 | UM011 Tavenard 深度学习时间序列 | 深度预测与基础模型概览 | 全部幻灯片 |
| 13 | BK026 Haben 等 负荷预测 | 领域实践与评测流程 | 第 5、7、9–11 章 |
| 14 | BK012 Castle & Hendry | 非平稳与结构突变的直观理解 | 第 3–5、7 章 |

## 6. 已知缺口（资料层面）

- **时间序列基础模型**：没有合法公开的书本长度资料，只能依赖论文和 UM011 等课程幻灯片。
- **层级预测、预测组合**：只有 FPP3 相关章节和少量课程内容。
- **面板时间序列**：没有找到公开且完整的课程。
- **数据泄漏与可复现性**：没有专书，主要依靠通用方法类的评测论文与 BK035。
- **空气质量、工业 RUL**：没有合格的公开书籍。工业 RUL 方向可用课程 UM063（林雪平《Prognostics and Statistical Predictive Maintenance》博士课程，2025 年春）[目录](university_materials/files/LinkopingUniversityD_PrognosticsStatistic_2025/)；水文随机方法另有课程 UM062（哥伦比亚国立大学，2025-II）。
- **年份**：部分经典讲义的学期或版本年份待核实，已在目录中标注。
