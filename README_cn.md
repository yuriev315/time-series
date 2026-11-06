# 时间序列分析与预测：初步文献库

本目录是“时间序列分析与预测”的**初步范围检索**结果，只收集文献，不含模型训练或论文实验。不宣称穷尽，也不是系统综述。

## 范围与日期
- 检索执行日期：2026-10-29（UTC）。
- 主要时间窗口：首次公开日期 2023-10-29 至 2026-10-29（检索日向前三年）。“首次公开”取 arXiv v1 提交日；无 arXiv 版本时取正式出版日期，并标注精度。
- 主题：A 基础分析、B 经典预测、C 机器学习、D 深度学习、E 时间序列基础模型、F 评测方法（每篇的主题与子主题见 catalog）。
- 规模：58 篇。53 篇在窗口内（91.4%），5 篇为三年前的补充/基础文献，逐篇写明保留理由。58 篇 PDF 全部下载并通过核验。
- 本库收录文献的最晚首次公开日期：2026-09-11。

## 目录说明
| 路径 | 内容 |
|---|---|
| [README_cn.md](README_cn.md) | 本说明 |
| [catalog_cn.csv](catalog_cn.csv) | 结构化目录（UTF-8 带 BOM，Excel 可直接打开）。表头、选入理由和简介为中文，标题、作者等元数据保留英文原文 |
| [reading_map_cn.md](reading_map_cn.md) | 按主题的阅读路线，以及最先阅读的 10 篇 |
| [search_log_cn.md](search_log_cn.md) | 检索平台、检索词、纳入与排除原则、排除记录 |
| [download_failures_cn.csv](download_failures_cn.csv) | 下载失败或仅有链接的文献（本轮为空表，只有表头） |
| [checksums_en.sha256](checksums_en.sha256) | 已下载 PDF 的 SHA256，可在本目录执行 `sha256sum -c` 校验 |
| [pdfs/](pdfs/) | 通过核验的 PDF，命名为 `首次公开年份_第一作者姓_短标题_en.pdf`（`_en` 表示正文为英文） |
| [scripts/](scripts/) | 本轮实际使用的脚本与中间数据（见下） |

### scripts/
| 文件 | 作用 |
|---|---|
| `seed_list_cn.json` | 候选名单：编号、主题、arXiv ID 或 DOI、优先级、选入理由、旧文献保留理由、经审核的非 arXiv PDF 地址 |
| `fetch_metadata_en.py` | 调用 arXiv API、Crossref、OpenAlex（及 DBLP，但本轮被限流）获取元数据，输出 `metadata_cache_en.json` |
| `verify_venues_en.py` | 用官方论文集索引页（PMLR、NeurIPS、ICLR、PVLDB）按标题核验会议渠道，输出 `venue_check_en.json` |
| `download_verify_en.py` | 下载 PDF，依次核验 HTTP 状态、`%PDF-` 文件头、pypdf 可解析性、首页标题匹配，再算 SHA256 并去重，输出 `download_results_en.json` |
| `annotations_cn.json` | 每篇两三句的中文简介（依据为摘要，未读全文） |
| `build_catalog_en.py` | 汇总以上文件，生成 `catalog_cn.csv`、`download_failures_cn.csv`、`checksums_en.sha256` |

## catalog_cn.csv 关键字段
- **时间窗口**：取值为“近三年”“三年前（补充/基础，不计入近三年）”或“待核实”（本轮没有待核实条目）。
- **首次公开日期 / 日期精度 / 正式发表日期 / 下载版本日期**：分开记录。旧论文近期更新的版本不算新研究。
- **渠道 / 渠道核验依据**，按可信度区分：
  - Crossref DOI 元数据；
  - 官方论文集索引页的标题匹配；
  - 官方单篇论文页面；
  - 只有 arXiv comments 中作者自述的接收信息（未核实）；
  - 未发现正式发表信息（标为“arXiv 预印本”，含义是“未核实是否已发表”）。
- **版本**：arXiv 文献下载的是最新版本号（例如 v3）。重大修订记录在“版本说明”列。
- **核验状态**：写明 HTTP 状态、文件头、页数和首页标题词匹配率。
- **简介依据**：全部基于摘要，未读全文，不代表已核实全文结论。

## 执行方式（可复用）
宿主机没有 pip/venv。pypdf 用 PyPI 上的纯 Python wheel 解压得到，不安装到系统：

```bash
cd /root/time_series_literature
LIB=/tmp/tsl_pylib; STAGE=/tmp/tsl_staging      # 任意可写目录；放在本目录之外
mkdir -p "$LIB" && curl -sSL -o /tmp/pypdf-5.1.0.whl \
  https://files.pythonhosted.org/packages/04/fc/6f52588ac1cb4400a7804ef88d0d4e00cfe57a7ac6793ec3b00de5a8758b/pypdf-5.1.0-py3-none-any.whl
echo "3bd4f503f4ebc58bae40d81e81a9176c400cbbac2ba2d877367595fb524dfdfc  /tmp/pypdf-5.1.0.whl" | sha256sum -c \
  && python3 -I -c "import zipfile; zipfile.ZipFile('/tmp/pypdf-5.1.0.whl').extractall('$LIB')"

python3 -I scripts/fetch_metadata_en.py .        # 已有缓存的条目会跳过；删除 metadata_cache_en.json 可全部重取
python3 -I scripts/verify_venues_en.py .
python3 -I scripts/download_verify_en.py . "$STAGE" "$LIB"   # 已核验通过的文件会跳过
python3 -I scripts/build_catalog_en.py .
sha256sum -c checksums_en.sha256
```

新增文献的流程：在 `seed_list_cn.json` 追加条目（编号续排），在 `annotations_cn.json` 补写简介，然后按上面的顺序重新运行。下载脚本拒绝覆盖哈希不同的同名文件。

## 访问与请求规范
- 只下载公开 PDF，来源为 arXiv、期刊开放获取页面和作者主页。不绕过付费墙、登录或验证码。
- 请求间隔：arXiv 至少 4 秒，其他主机至少 3 秒。每个 URL 最多尝试 3 次；遇到 401/402/403/404/451 立即停止，不再重试。
- 下载文件先放进独立的空暂存目录，核验通过后才移入 `pdfs/`。

## 总进度（脚本自动生成）

<!-- PROGRESS:START -->
| 分类 | 进度 | 主分类 | 独有 | 跨类 | 近三年占比 | 三年前 | 状态 |
|---|---|---|---|---|---|---|---|
| [通用方法](domains/01_general_methods/) | 已核验全文 58 / 目标约 50；待核验 0；下载失败 0。 | 58 | 57 | 1 | 53/58（91.4%） | 5 | 达标 |
| [金融](domains/02_finance/) | 已核验全文 1 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 1 | 1/1（100.0%） | 0 | 进行中 |
| [空气质量](domains/03_air_quality/) | 已核验全文 0 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 0 | - | 0 | 未开始 |
| [水质](domains/04_water_quality/) | 已核验全文 0 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 0 | - | 0 | 未开始 |
| [气象与气候](domains/05_weather_climate/) | 已核验全文 0 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 0 | - | 0 | 未开始 |
| [能源与电力](domains/06_energy_power/) | 已核验全文 1 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 1 | 1/1（100.0%） | 0 | 进行中 |
| [水文与水资源](domains/07_hydrology/) | 已核验全文 0 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 0 | - | 0 | 未开始 |
| [交通与出行](domains/08_transport/) | 已核验全文 0 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 0 | - | 0 | 未开始 |
| [工业与设备](domains/09_industrial/) | 已核验全文 0 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 0 | - | 0 | 未开始 |
| [医疗与公共卫生](domains/10_health/) | 已核验全文 0 / 目标约 50；待核验 0；下载失败 0。 | 0 | 0 | 0 | - | 0 | 未开始 |

全库去重：已核验论文 58 篇，已核验 PDF 文件 58 个；待核验 0；下载失败 0（均不计入）。
<!-- PROGRESS:END -->
