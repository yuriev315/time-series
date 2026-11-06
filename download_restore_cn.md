# 下载与解压

Release `ts-full-20261029` 中的 tar 包不压缩。把所有 tar 解压到同一目录，就能得到完整资料库。

```bash
mkdir time-series-library
for f in time_series_*_batch*.tar; do tar -xf "$f" -C time-series-library; done
```

Windows 10/11 自带 `tar`，命令相同（在 PowerShell 中逐个解压即可）。

解压后：

- `pdfs/`、`pending_pdfs/`：论文全文
- `books/files/`：书籍
- `university_materials/files/`：课程讲义
- `*.url`：占位文件，打开后到原始来源下载。文件里的 `SHA256` 可用来核对下载结果。

每个 tar 的成员列表见 `archive_index_cn.csv`。每个 tar 的 SHA-256 见 Release 中的 `upload_report_cn.md`。
