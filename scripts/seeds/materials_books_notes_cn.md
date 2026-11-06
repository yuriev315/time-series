# materials_books（书籍类学习资料）检索笔记

日期：2026-10-29。种子文件：`scripts/seeds/materials_books_seed_cn.json`，共 60 条：主表 1–50，备选 51–60。
本轮未下载任何资料，只用 WebFetch/WebSearch 读了官方页面，另用 curl 对部分 PDF 做了 HEAD 可达性检查（不下载正文）。摘要依据官方页面描述与目录，未精读正文。

## 1. 检索方式与来源

- **WebSearch**：用到的检索词包括书名加 "pdf"、"open access"、作者主页、"WMO-No."、"GAW report"、"CCBS handbook"、"Eurostat handbook"、"USGS Techniques and Methods"、"Springer open access time series / load forecasting / prognostics" 等。
- **WebFetch 核对的官方页面**：
  - 出版方与作者页：otexts.com（fpp3、fpppy、weird）、openforecast.org/adam、users.aalto.fi/~ssarkka、gaussianprocess.org、probml.github.io、hastie.su.domains（ESL、ISLP、SLS、CASI）、statlearning.com、sites.stat.columbia.edu/gelman、spacetimewithr.org、d2l.ai、mml-book.github.io、mlstory.org、sites.math.duke.edu/~rtd、user.it.uu.se/~ps。
  - GitHub 仓库：rlabbe、udlbook（经 GitHub API 取 latest release）。
  - arXiv 摘要页（6 个）。
  - 机构与政府：bashtage.github.io（Sheppard 讲义）、MPRA、bankofengland.co.uk、ec.europa.eu/eurostat、imf.org、pubs.usgs.gov、old.wmo.int、census.gov、python.quantecon.org、miguelhernan.org、chance.dartmouth.edu。
- **Springer 开放获取书**：link.springer.com 对直接请求返回 cookie 跳转（curl 得到 "Client Challenge"）。改为先请求 idp.springer.com/authorize，再带 code 访问书页，共核对 7 本，均确认标注 Open Access 且页面给出 `/content/pdf/<doi>.pdf`。
- **不可达的站点**：OAPEN、DOAB、direct.mit.edu、MIT Press 书页对本机一律返回 403 或 ECONNRESET，所以没能按计划在 OAPEN/DOAB 上做系统检索（见第 6 节）。
- 未使用 OpenAlex。

## 2. 主要纳入与排除决定

**合并（同一作品只计一项）**
- FPP3 与其 Python 版 "the Pythonic Way" 合为第 1 项，两个 HTML 目录都列出。
- ISL 只保留 Python 版 ISLP（2023），ISLR2 不另列。
- BFS 只保留第 2 版（2023），第 1 版不另列。
- Diebold 只取 Edition 2024，不收旧作 Elements of Forecasting。

**排除：没有合法全文，或无法在官方页面核实**

| 书 | 排除原因 |
|---|---|
| Hansen《Econometrics》 | 作者页现只链接出版社与零售商，无 PDF；《Probability and Statistics for Economists》同样 |
| Subba Rao《A course in Time Series Analysis》 | TAMU 旧链接已 301 跳到系主页，官方副本不存在；只剩 SlideShare/Scribd 等第三方副本，按规则不收 |
| Brunton & Kutz《Data-Driven Science and Engineering》 | databookuw.com 只提供代码和数据，无全书 PDF |
| Shumway & Stoffer（TSA4/TSA5/TSDA） | 未找到合法免费版，检索结果只有 Springer 付费页和可疑站点 |
| Yang & Kleissl《Solar Irradiance and PV Power Forecasting》 | Routledge 商业书，非 OA |
| Blitzstein & Hwang《Introduction to Probability》 | stat110 站点对本机 403，未找到官方 PDF |
| Barber《BRML》 | UCL 主页连接被拒，只找到第三方索引页 |
| Goulet《Probabilistic ML for Civil Engineers》 | 机构库称出版方 OA，但作者页连接被拒，无法核对文件 |
| Anderson & Moore《Optimal Filtering》 | 作者发表列表页链接到 hidden/ 目录下的 PDF，请求返回 502，授权状态不明 |
| Stanley Chan《Introduction to Probability for Data Science》 | 下载需填 Google 表单 |
| MacKay《ITILA》 | 官方页链接的 cs.toronto.edu PDF 返回 404，且与时间序列关联弱 |
| Doornik & Hendry《Empirical Model Discovery》 | OA 状态不明 |
| Goebel 等《Prognostics: The Science of Making Predictions》 | 无官方免费版 |

**付费经典（无合法全文，未收）**：Hamilton、Brockwell & Davis、Durbin & Koopman、Harvey、Tsay、Lütkepohl、Box-Jenkins、Percival & Walden、Kantz & Schreiber、Fan & Yao、Wilks、Jolliffe & Stephenson、Hyndman 等《Forecasting with Exponential Smoothing》、Prado-Ferreira-West、Aggarwal《Outlier Analysis》、Little & Rubin。

**因其他原因不收**
- HTML 名额已满（每表上限 5 本）：Bifet 等《Machine Learning for Data Streams》（仅 HTML，MIT Press OA）、Goodfellow《Deep Learning》（仅 HTML）、《Introduction to Econometrics with R》、NIST/SEMATECH e-Handbook。
- Bishop《Deep Learning: Foundations and Concepts》：只有在线阅读器，没有可下载文件。
- The Turing Way：没有书本 PDF。
- 篇幅或可得性不足：
  - EPA/AirNow 空气质量预报指南：官方 PDF 只有 26 页，不到书本长度。
  - WMO-No.1364《Guidelines on the Verification of Hydrological Forecasts》（2025）：library.wmo.int 为 JS 渲染，拿不到 PDF 地址。这是很好的候选，**建议协调者手工获取**。

**通用 ML/统计书收入的理由**
- ESL、ISLP：ML 预测器以及模型评估/交叉验证的标准来源。
- BDA3：层级模型与后验预测检验，是层级/面板预测和概率预测的方法论基础。
- PRML：序列数据一章（HMM、LDS）。
- CASI：预测误差估计与 bootstrap。
- MML、PML1：数学与概率机器学习基础。

这些书都在 reason 字段里写了理由，排位靠后，优先级 2–3。

## 3. 覆盖表（主题 → rank）

| 主题 | rank |
|---|---|
| 数学、概率统计、随机过程基础 | 35, 33, 32, 50, 19（备选 60, 56, 53） |
| 平稳性、自相关、谱分析、趋势季节分解 | 1, 6, 12, 26, 47（备选 52, 55） |
| ARIMA、指数平滑、动态回归、预测组合 | 1, 3, 4, 5, 6 |
| 状态空间、卡尔曼滤波、贝叶斯方法 | 2, 16, 7, 31, 29, 30, 25, 24, 34, 40, 48, 22, 32 |
| 多元、高维、非线性、波动率 | 24, 25, 6, 23, 49, 11, 31, 38（备选 53） |
| 机器学习、深度学习 | 17, 18, 19, 20, 21, 39, 38, 7（备选 59） |
| 概率预测、预测区间、校准、不确定性 | 9, 10, 11, 3, 27, 44, 5, 7（备选 59） |
| 非平稳、结构突变 | 13, 37（备选 54） |
| 异常检测 | 14 |
| 缺失数据、不规则采样 | 15, 38 |
| 时空分析 | 8 |
| 层级预测 | 1（第 11 章） |
| 层级/面板模型 | 22, 24（备选 58 纵向因果） |
| 滚动评估、时间切分、泄漏、可复现性 | 1（时间序列交叉验证）, 27, 36, 50, 5 |
| 季节调整、现时预测（官方手册） | 26, 46, 47（备选 55） |
| 金融、宏观 | 23, 4, 6, 41, 24, 25, 13, 46, 47 |
| 能源 | 27, 42 |
| 水文 | 28, 43, 45, 29（备选 51） |
| 水质 | 28, 45（备选 51） |
| 气象、数据同化 | 44, 29, 30 |

**缺口**
1. **时间序列基础模型**：没有合法免费的书本长度资料。现有的只是 UDL、Alice、PML2 中的 Transformer/SSM 骨干章节，建议由论文类目补齐。
2. **空气质量预报**：没有合格书籍；只有第 8 本时空统计作方法支撑。
3. **工业预测性维护 / RUL**：没有找到 OA 书。
4. **非线性时间序列与变点检测**：没有专著，相关经典均付费。
5. **层级预测**：只有 FPP3 一章加第 5 本综述的条目。
6. **数据泄漏、时间切分**：只散见于 FPP3、第 27 本和第 36 本，没有专书。

## 4. 建议的 Top 15（按阅读顺序）

1. **#35 MML**：数学基础（线代、概率、优化）。
2. **#1 FPP3**：预测入门主线，含分解、ETS、ARIMA、层级预测和时间序列交叉验证。
3. **#4 Diebold**：经济金融视角的预测与评估、预测组合。
4. **#6 Cochrane**：线性时序理论的速成，包括 ARMA、VAR、谱、单位根。
5. **#3 ADAM**：状态空间 ETS/ARIMA 进阶，以及不确定性与间歇需求。
6. **#16 Labbe**：用代码入门卡尔曼与粒子滤波。
7. **#2 Särkkä & Svensson**：贝叶斯滤波与平滑的权威教材。
8. **#13 Castle & Hendry**：非平稳、结构突变、指标饱和。
9. **#9 Gentle Conformal**：预测区间与校准入门。
10. **#8 Wikle 等**：时空统计。
11. **#14 Weird**：异常检测。
12. **#15 FIMD**：缺失数据与插补。
13. **#17 D2L**：深度序列模型实践。
14. **#7 PML2**：高级概率建模总参考（状态空间、SMC、GP、生成模型）。
15. **#27 Haben 等**：能源负荷预测完整流程与评估（应用范例）。

## 5. 年份分布（主表 50 本，按 version_year）

| 年份段 | 数量 |
|---|---|
| 2024–2026 | 5（2024：2，2025：1，2026：2） |
| 2023 | 7 |
| 2019–2022 | 17 |
| 2009–2018 | 14 |
| 2005–2006 | 4 |
| 待核实 | 3 |

- 合计 12 + 17 + 14 + 4 + 3 = 50；近三年（2023 年及以后）共 12 本。
- 2009–2018 的 14 本：2018：2，2017：3，2016：1，2015：3，2013：1，2012：1，2011：1，2010：1，2009：1。
- 2005–2006 的 4 本：Cochrane（version_year 写为 "2005（待核实）"）、Stoica & Moses、GPML、PRML。
- 待核实 3 本：Weird、Labbe、QuantEcon（version_year 写为 "待核实"）。
- 早于 2023 年且年份已知的版本都填了 classic_reason。

## 6. 存疑条目与下载风险（供协调者参考）

**站点可达性**

| rank | 书 | 风险 |
|---|---|---|
| #4 | Diebold | sas.upenn.edu 对本机（WebFetch 与 curl）返回 403，文件 URL 来自搜索引擎索引，官方页面未能直接核对；下载可能失败，失败时改用备选 |
| #34 | PRML | 微软站点对 curl 的 HEAD 请求返回 403（反爬），WebFetch 读取页面正常 |
| #47 | IMF QNA | 带浏览器 UA 的 HEAD 返回 403，不带 UA 返回 200 |
| #13, 27, 29, 41, 42, 51, 59 | Springer OA 共 7 本 | curl 直连得到 "Client Challenge"，可能需要浏览器 UA 或 cookie；7 本中只有 #13（CC BY 4.0）和 #51（CC BY-NC 4.0）在页面上显示了具体许可证 |
| #57 | Elements of Causal Inference | OAPEN、MIT Press 均返回 403，URL 来自检索结果 → 存疑 |

**Google Drive 文件**
- 涉及 #16、#20、#21、#49、#50。
- 后四本是官方 `.pdf.download.html` 页面用 meta-refresh 跳到 Drive，种子里直接给出了 Drive 地址。#16 的 Drive 链接取自 README 原文。
- 大文件下载时 Drive 可能先返回病毒扫描确认页。

**完整性与版本**
- #23 Sheppard：分章列表中第 6、9 章标为 TBD，"Complete" 全书 PDF 是否包含这两章待核实。
- #12 Stoica & Moses：作者主页提供的是出版前排版稿（约 2004 年），可能与 2005 年印刷版有差异。
- #6 Cochrane：原始年份 1997、版本年份 2005 都待核实（凭记忆，未打开 PDF）。
- #14 Weird、#16 Labbe、#48 QuantEcon：版本年份待核实，均为在线持续更新。

**性质与许可**
- #5 Petropoulos 等：期刊长综述，不是书，因百科式篇幅和导航价值破例收入。
- 仅限个人使用、不得再分发的条目：#2、#10、#18（CC BY-NC-ND）、#49、#50、#53。入库只作本地个人学习副本即可。

**cross_kind**：#1、#2、#4 的课程对应关系由记忆或目录名推断，均标"待核实"；#23 的课程名来自作者页面。
