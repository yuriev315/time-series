# 大学课程讲义补充清单（排名 61–72）说明

生成日期：2026-10-29。对应文件：`scripts/seeds/materials_courses_supp_cn.json`，共 12 条，kind 均为 "course"。

## 0. 背景与目标

原清单 `materials_courses_seed_cn.json` 有 60 条，下载核验后约 47 条成为完整讲义包。其余失败的原因有：文件 404、站点 403、PKU/PSU 的 TLS 证书错误、扫描件无文本。本批补充 12 条，有三个要求：

- 不与原 60 条重复（机构、课程、文件 URL 都比对过）；
- 不与书单 `materials_books_seed_cn.json` 重复；
- 优先补原清单覆盖不到的主题。

比对结果：本批 144 个文件 URL 和 12 个 homepage，与课程种子及书单都没有交集（脚本比对）。

## 1. 检索词与来源

主要用 WebSearch 发现候选，再回到官方页面用 curl/WebFetch 读取 HTML，从页面里逐个提取讲义链接。所有 URL 都取自页面上的实际链接，没有按命名规律推测。GitLab 仓库用官方 API 列出文件树，README 讲次表与之一致。HydroShare 也用官方 API 列出文件。

用过的检索词（节选）：

- 能源：renewable energy forecasting course lecture notes DTU Pinson
- 金融：financial econometrics lecture notes volatility GARCH course pdf；volatility modelling course slides realized volatility HAR；Andrew Patton / Brownlees / Lindström financial statistics slides
- 非线性：nonlinear time series course lecture notes threshold regime switching
- 面板：panel data econometrics lecture notes pdf；dynamic panel GMM cross-sectional dependence course；longitudinal data analysis lecture notes
- 层次预测与组合：hierarchical forecasting reconciliation course slides；forecast combination lecture notes Timmermann；forecast evaluation instabilities Rossi Giacomini
- 预后：prognostics remaining useful life course lecture notes
- 水文：stochastic hydrology lecture notes；statistical hydrology lecture notes；hydrological forecasting course slides
- 概率预测：probabilistic forecasting scoring rules course Gneiting；forecast evaluation CRPS PIT lecture notes
- 共形预测：conformal prediction course lecture notes 2024 time series
- 深度学习：deep learning time series forecasting course slides；sequence models lecture notes；time series foundation models course
- 时空与环境：spatio-temporal statistics course lecture notes；environmental statistics course lecture notes air pollution；extreme value statistics course lecture notes

由检索结果顺藤摸瓜找到的官方页：

- Pinson 个人站点课程页
- SGPE ECNM11049 课程页
- UNAL 课程 GitHub Pages
- LiU 静态课程页及 gitlab.liu.se 仓库
- UW STAT 591A 课程页
- HAL hal-04690218
- Goude 在 Paris-Saclay 的教学页（由 Zaffran 教学页指向）
- posit::conf 2023 工作坊站
- Mike West 的 JSM 2019 CE 页
- R. L. Smith 的 UNC 主页及 STOR 834 页
- Zivot 的 Econ 589 Syllabus 页
- Zaffran 教学页与 ENBIS Indico 页

## 2. HEAD 核验结果

逐个文件检查：`curl -sSI -A 'time_series_literature/1.0' <url>`。没有下载全文。另外做过少量 Range 请求，只读首尾不超过 600 KB，用来看 PDF 元数据、字体类型和首页文字，判断是否为文本 PDF、标题和作者能否匹配。

**最终结果：144/144 个文件 URL 返回 200，Content-Type 均为 application/pdf，合计约 228 MB。**

| 排名 | 主机 | 文件数 | HEAD 结果 | 文本性抽查 |
|---|---|---|---|---|
| 61 | pierrepinson.com | 46 | 46×200 pdf（HTTP/2） | beamer/pdfTeX，2018 年；抽查 8.3、9.1 两讲有文本 |
| 62 | nhauzenb.github.io | 7 | 7×200 pdf | pdfTeX；首页含课程名与讲师 Hauzenberger |
| 63 | lamhydro.github.io | 20 | 20×200 pdf | pdfTeX；首页含课程名与讲师 Morales，日期 2025-08/10 |
| 64 | gitlab.liu.se（raw） | 6 | 6×200 pdf（HTTP/1.1） | Type1C 字体；首页含课程名与 Erik Frisk |
| 65 | sites.stat.washington.edu | 12 | 12×200 pdf | PowerPoint 导出；首页含 Sampson、Guttorp |
| 66 | hal.science | 1 | 200 pdf | 首页含标题、作者与完整目录 |
| 67 | www.imo.universite-paris-saclay.fr | 9 | 9×200 pdf | beamer，作者元数据为 Yannig Goude（注 1） |
| 68 | posit-conf-2023.github.io | 11 | 11×200 pdf | pdfTeX，2023-09 |
| 69 | www2.stat.duke.edu | 3 | 3×200 pdf | 首页含三位讲师姓名 |
| 70 | rls.sites.oasis.unc.edu | 1 | 200 pdf | Type1 字体；首页标题与作者可读，目录 1–9 章 |
| 71 | faculty.washington.edu | 27 | 27×200 pdf | 首页含 “Amath546/Econ589 … Eric Zivot” |
| 72 | mzaffran.github.io | 1 | 200 pdf（必须用 https；http 会 301） | 首页含标题与作者 |

注 1：67 的旧域名 `www.math.u-psud.fr/~goude/` 先 301 到 `~goude/`，再 301 到 `~yannig.goude/`。JSON 里已直接写入最终的 200 地址。

下载脚本的核验条件也逐项对照过：

- 单 PDF 条目（66、70、72）：标题用的是 PDF 首页原文，以满足 title_match≥0.6；作者姓氏都出现在首页。
- 多文件条目：每条都至少有一个文件首页含讲师姓氏或课程名。

## 3. 纳入与排除决策

### 纳入（12 条）

- 61 Pinson：DTU 31761 开放课程
- 62 Edinburgh：SGPE ATSE 2026
- 63 UNAL：水资源随机方法 2025-II
- 64 LiU：预后与预测性维护博士课 2025
- 65 UW：STAT 591A 时空统计 2017
- 66 Da Veiga：ETICS 2024 共形预测讲义
- 67 Goude：Paris-Saclay ML & Forecasting 2025-26
- 68 Hyndman：posit::conf 2023 工作坊（取其层次预测部分）
- 69 Prado/West/Ferreira：JSM 2019 贝叶斯时间序列
- 70 R. L. Smith：极值统计讲义（STOR 834 2023 课程页所列）
- 71 Zivot：UW Econ 589 2013
- 72 Zaffran：ECAS-ENBIS 2023 共形预测

### 主要排除项

| 候选 | 排除原因 |
|---|---|
| Bierkens 等 “Introduction to Stochastic Hydrology”（Utrecht GEO4-4420，HydroShare 资源，含 2026-08 版电子书 PDF 和 9 章 PDF） | 内容很好，作者本人上传。但 HydroShare 对 HEAD 返回 405，GET 先 301/302 跳到临时签名的 Google Storage URL，最终 Content-Type 是 binary/octet-stream。SURFsharekit/edusources 链接的 HEAD 也只返回 text/html。不满足“HEAD 200 + PDF 类型”，暂不收。**可作备选**：HydroShare 的 GET 跳转实际可下载（206 Range 测试成功），需协调者决定 |
| R. L. Smith “Environmental Statistics Lecture Notes (2001)” envnotes.pdf（377 页） | HEAD 200 pdf，但 PDF 用 Ghostscript 6.51 生成，250 个 Type3 位图字体；首段流解压后是乱码，pypdf 抽不出文本，大概率被判为无文本。改收同作者的 SEMSTAT 极值讲义（70） |
| Smith STOR 834 “Extreme Values” 书稿（2023-04 版） | 目录显示 1.5–1.9 节都在第 26 页，是占位节，书稿不完整 |
| Anne Sabourin MVA 极值课程讲义（helios2.mi.parisdescartes.fr） | 站点 503 维护中 |
| ISF 2025 / ISF 工作坊深度学习预测幻灯片（isf.forecasters.org） | 403 |
| KIT Gneiting “Forecasting: Theory and Practice”（wwwalt.math.kit.edu） | TLS 证书链无法验证（unable to get local issuer certificate），且未见公开讲义 |
| Lund FMS161/MASM18 Financial Statistics（Lindström） | 官方课程页 404，只有 sambuz 等第三方镜像 |
| Aarhus CREATES 2016 高频金融计量博士课 | 只找到单讲 PDF，没有列出全部讲义的官方页 |
| UCR Agüero “Panel Data Econometrics”（2008 开普敦短课） | 太旧，只有 4 讲 |
| AGRODEP “Course Notes on Panel Data Econometrics”（2012） | 页面不给公开 PDF 链接（需登录），站点还夹杂代写广告链接 |
| NYCU 黄冠华 Longitudinal Data Analysis 2024 | 课程站点 /course/lda24/ 404 |
| UW FISH 507 ATSA 2025（Holmes/Ward/Scheuerell） | 讲义 PDF 与 HTML 混杂（HMM、GAM、时空等讲只有 HTML）；配套实验书只有 HTML |
| TU Delft CIEM42X0 概率设计 2025 | 主题为可靠性设计，非时间序列预测 |
| CMU 11-785 Introduction to Deep Learning（S25，30 份幻灯片） | 文件可用，但属通用深度学习，与原清单 Fleuret（35）、Tavenard（11）重叠，且体量大 |
| NEU（越南）时间序列课、TTU Eco 4306（Duras） | 入门 ARIMA 课，与原清单重复；后者讲师已离校 |
| NPTEL Stochastic Hydrology | 页面是 JS 应用，无法从页面核验文件清单 |
| UW Econ 589 页面上的教材章节 PDF（ch1/ch2/ch18 等）和他人论文 | 不是讲师讲义，合法性存疑，未纳入 71 |

## 4. 新增覆盖（主题 → 排名）

| 主题（用户列出的缺口） | 本批排名 | 说明 |
|---|---|---|
| 预测组合 / 层次预测 | 67（专家聚合）、68（第 10 份：预测调和） | 原清单无层次预测；组合只在书中零散出现 |
| 面板 / 时空统计 | 65（时空）；面板 **未补到** | 合格的公开面板课程讲义都失败了，见上表 |
| 状态空间与 Kalman 滤波 | 62（UC/状态空间/DFM）、69（贝叶斯 DLM/TVAR/DFM）、63（第 20 讲） | 原清单已较多，本批偏贝叶斯多元与宏观应用 |
| 金融计量 / 波动率 | 71（GARCH、DCC、VaR 回测）、70（金融时间序列极值）、62（随机波动率、时变参数） | 补回测与多元波动率；已实现波动率/HAR 未找到合格课程 |
| 非线性时间序列 | 62（结构突变、TAR、马尔可夫转换、TVP、神经网络） | |
| 概率预测 / 共形预测 | 61（模块 8 概率预测检验）、66、72（时间序列 ACI） | |
| 深度学习序列 / 预测 | 64（深度网络预后）、62（神经网络）；**无新增专门课程** | 原清单 11、35 已覆盖；ISF 资料 403 |
| 环境 / 水文 / 能源预测 | 61、67（能源）；63（水文）；65、70（环境监测、气候、极值） | |
| 预后 / 剩余寿命 | 64 | 原清单完全没有 |

## 5. 年份分布

以课程学期或版本年计：2026（62）；2025（63、64、67）；2024（66）；2023（68、72）；2019（69）；2018（61 幻灯片）；2017（65）；2013（71）；2003/2001（70）。

近三年（2023–2026）共 7 条，较早的 5 条都填写了 classic_reason。格式：multi_pdf 9 条，pdf 3 条，html 0 条。

## 6. 建议优先下载顺序

1. **61 Pinson**：能源预测与概率预测检验，46 讲完整开放课程。
2. **62 Edinburgh ATSE**：非线性、状态空间、因子与混频模型，2026 版。
3. **63 UNAL**：水文时间序列与极值，2025 年。
4. **64 LiU**：预后与剩余寿命，2025 年。
5. **70 Smith**：环境与金融极值的经典成文讲义。
6. **66 Da Veiga**：成文的共形预测讲义。
7. **65 UW 591A**：时空统计与环境监测。
8. **67 Goude**：GAM 负荷预测与专家聚合。
9. **71 Zivot**：GARCH、DCC 与 VaR 回测。
10. **68 Hyndman**：层次预测与预测调和。
11. **69 JSM 2019**：贝叶斯多元动态模型。
12. **72 Zaffran**：时间序列共形预测。

## 7. 存疑与注意事项

- **61**：学期不明。只能从 PDF 元数据推断幻灯片制作于 2018 年；页面称该课程在 DTU “讲授多年”，现由作者站点以开放课程形式发布。46 个文件中有 10 个是模块导言（x.0），页数少，但抽查均有文本，预计不会触发“>1/4 文件几乎无文本”。
- **65**：年份 2017 是根据页面日期（9/28 为周四、11/23 停课）推断的，页面本身没写年份。
- **67**：语言可能中英混合，部分讲义为法文，待核实。课程页同栏还有 3 个 HTML 讲（含 time_series.html 实操）未纳入，因此本包是“全部 PDF 讲义”，不是全部课程材料。intro2024.pdf 等讲义标注 2024，planning 文件为 2025–2026。
- **68**：不是大学学期课程，而是 posit::conf 官方工作坊，讲师为 Monash 的 Hyndman。与原清单 3（Monash ETC3550）在 ETS、ARIMA 等内容上重叠，新增价值主要在第 10 份（层次预测）。已设为 priority 3；若协调者认为重复，可只保留或剔除。
- **69**：一日课程，只有 3 份幻灯片，但每份都较长（1.4–5.6 MB）。课程说明 PDF 未纳入。
- **70**：讲义写于 2001 年，PDF 版本日期为 2003-03-12。它也是 Finkenstädt & Rootzén 编著书第 1 章的预印本（作者主页公开）。STOR 834 2023 课程页把它列为讲师讲义。
- **71**：2013 年课程，较旧。其中 13 份为 R 示例幻灯片（PowerPoint 导出），内容以输出图表为主，但都有标题文字。
- **66 与 72**：同属共形预测主题。66 是成文讲义，偏通用方法；72 是幻灯片，专讲时间序列。两者互补；若需去重，保留 66。
- **备选**：Bierkens HydroShare 电子书。若协调者接受“GET 可下载但 HEAD 405、类型为 octet-stream”，它可替换 72 或 68。
