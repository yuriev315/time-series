# 最小运行环境报告：time-series

## 1. 仓库与目录
- 仓库：`yuriev315/time-series`（文献库：目录、阅读指南和维护脚本，不含模型训练）。
- 本地目录：`/root/time-series/`。增量分支：`minimum-runtime-20261104`，基于 `release-lite-20261029`。

## 2. 最小 Python 环境
CPython 3.10，隔离的 venv。不需要 GPU，不需要编译型包。

## 3. 必需依赖与安装
依据实际 import 判定。第三方依赖只有 2 个：`pypdf==5.1.0`（仓库 README 指定的版本和哈希）、`typing_extensions==4.16.0`（Python 3.10 下 pypdf 需要）。其余都是标准库。分类见 `manifests/minimum_runtime_dependencies.csv`。

## 4. Windows Python 3.10 兼容性
**没有在真实 Windows 上运行过。** wheel 都是纯 Python，已按 Windows 目标平台离线解析通过。代码里有两个 Windows 问题，源码未改：
- `scripts/ratelimit_en.py` 导入 `fcntl`，Windows 没有这个模块，因此 `fetch_metadata`、`search_candidates`、`download_papers`、`download_materials` 无法启动。已提供垫片 `windows_offline/minimal/compat/fcntl.py`：只模拟测试过，它会取消跨进程限速，一次只运行一个联网脚本。
- `read_text()` 没有指定编码，非 UTF-8 系统下会报错，必须加 `-X utf8`。`PYTHONUTF8` 环境变量在 `-I` 下无效。

## 5. 实际验证
共 18 项，见 `manifests/runtime_test_results.csv`：**13 项通过，2 项失败，3 项未测**。
- 通过：Python 3.10 离线安装、导入、12 个脚本编译、main 的 58 个 PDF 校验、离线重建目录、pypdf 解析真实 PDF、真实联网获取 1 条 arXiv 元数据等。
- 失败：T09、T11，都是在 Linux 上模拟 Windows 条件，确认了第 4 节的两个问题。有规避办法，但未在 Windows 验证。
- 未测：真实 Windows、完整下载流程、GPU（不适用）。
- 重建结果说明：release-lite 的 536 行论文和校验和与提交内容一致，但已提交目录多出的 116 行书籍和讲义没有脚本能生成。main 分支已提交的目录是旧的（58 行，重建为 218 行）。

## 6. 已下载的数据集和模型
**都没有，也都不需要。** 仓库运行不依赖任何模型或数据集。

## 7. `.url` 占位
3 个，都是原 Release 的完整文献 tar（每个约 1.4 GiB），URL 已实测有效，运行脚本不需要它们。见 `manifests/url_placeholders.csv`。

## 8. 缺失依赖与外部要求
见 `manifests/missing_requirements.csv`。主要是真实 Windows 验证、完整下载流程未测，以及刷新文献库时需要的网络服务（arXiv、Crossref、OpenAlex 等，代码里没有 API key）。

## 9. 清理
按批准已删除，明细见 `manifests/deletion_log.csv`。Git 镜像改用 `--max-pack-size=95m` 重新打包，最大包文件 99 MB，历史和引用未变；仓库里最大的对象只有 40 MB，这不是拆分大文件。

剩余候选见 `manifests/cleanup_candidates.csv`：
- 原 Release 的 3 个 tar（超过 100 MiB，但属于原始附件，**未删除，需要你决定**）。
- `state/`、`logs/`、`external_resources/`、`manifests/superseded/`，都是已删归档的记录，可选删除。

## 10. 磁盘
- 当前占用约 0.9 GB，其中 Git 镜像占 0.8 GB。
- 已删除本地文件 47.6 GiB，共 453,485 个。
- 已移除本次之前上传的 Release 附件 31 个，10.68 GiB。
- 已取消下载：8,423 个文件。

## 11. 最终状态
**`RUNNABLE_WITH_URL_PLACEHOLDERS`**

核心功能（离线重建目录、校验、PDF 解析）已在 Linux + CPython 3.10 上实测通过，完整文献全文仍在外部（3 个占位）。主要目标平台 Windows 尚未实测，这是最大的未验证项。

## 12. 安装和运行命令

Windows（未实测）：

```bat
git clone --depth 1 -b minimum-runtime-20261104 https://github.com/yuriev315/time-series.git
cd time-series
py -3.10 -m venv .venv
.venv\Scripts\python -m pip install --no-index --find-links windows_offline\minimal\wheels --require-hashes -r manifests\windows_python310_requirements.txt
robocopy . work /E /XD .git .venv work
.venv\Scripts\python -I -X utf8 scripts\build_catalog_en.py work
```

联网刷新元数据（Windows 需要垫片，不能加 `-I`）：

```bat
set PYTHONPATH=%CD%\windows_offline\minimal\compat
set TSL_LOCK_DIR=%TEMP%\tsl_ratelimit
.venv\Scripts\python -X utf8 scripts\fetch_metadata_en.py work
```

Linux（步骤已实测）：

```bash
git clone --depth 1 -b minimum-runtime-20261104 https://github.com/yuriev315/time-series.git
cd time-series
python3.10 -m venv .venv
.venv/bin/python -m pip install --no-index --find-links windows_offline/minimal/wheels --require-hashes -r manifests/ubuntu_requirements.txt
mkdir work && cp -r scripts catalog_cn.csv work/
.venv/bin/python -I -X utf8 scripts/build_catalog_en.py work
```

请在副本 `work` 上运行：`build_catalog_en.py` 会覆盖目录，原地运行会丢掉那 116 行书籍和讲义。
