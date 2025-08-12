# Parse_CZI — 高性能 Zeiss CZI 解析器
[![PyPI](https://img.shields.io/pypi/v/parse-czi.svg)](https://pypi.org/project/parse-czi/)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/pypi/pyversions/parse-czi.svg)
![Performance](https://img.shields.io/badge/performance-13.3x%20faster-brightgreen.svg)

> 面向 **Zeiss Axio Scan7** 等产生的 **CZI** 超大图像文件，提供极速解析、并行导出与完整元数据提取。设计为“即开即用的 **CLI 工具** + 生产可嵌入的 **Python 包**”。

<p align="center">
  <img src="assets/arch-overview.svg" alt="architecture overview" width="720"/>
</p>

---

## 目录
- [特性](#特性)
- [安装](#安装)
- [快速上手](#快速上手)
- [输出内容](#输出内容)
- [性能基准](#性能基准)
- [常见问题 / 故障排除](#常见问题--故障排除)
- [兼容性与依赖](#兼容性与依赖)
- [路线图](#路线图)
- [贡献](#贡献)
- [许可证](#许可证)
- [English README](#english-readme)

---

## 特性
- **XML 元数据完整提取** → 自动导出为 `metadata.xml`，保留成像维度、像素物理尺寸、通道信息与注释。
- **通道级导出（OME‑TIFF）** → 每个通道单独写出 `channel_*.ome.tif`，便于下游处理与批量作业。
- **并行加速** → 多线程流水线，I/O 与编码并行，典型 **4–8 线程** 即可吃满 SSD 带宽。
- **BigTIFF 自动切换** → 深度/尺寸超限时自动启用 **BigTIFF**，无须手调。
- **鲁棒归一化** → 通道内 **min‑max** 归一为 8‑bit（可保持 16‑bit），避免“通道发黑/发白”。
- **日志与进度** → 详细阶段耗时与资源信息，方便定位瓶颈。

---

## 安装
> 需要 **Python ≥ 3.8**。支持纯 Python wheel（`py3-none-any`），跨平台可用。

### 使用 PyPI（推荐）
```bash
python -m pip install -U parse-czi
# 或固定版本：
python -m pip install parse-czi==0.1.0
```

<details>
<summary>✅ 可复现安装（哈希固定）</summary>

`requirements.txt`：
```
parse-czi==0.1.0 \
  --hash=sha256:2a961574c26d83abd4c7dd0360cbb40e8fa11f7d1760f513fb235a3617adea \
  --hash=sha256:3d50ca7f00a7aa2e916d7d81989a3ce7e29088fb6ad99e972f50fb7774832d92
```
安装：
```bash
python -m pip install -r requirements.txt --require-hashes
```
</details>

<details>
<summary>🌐 离线 / 内网安装</summary>

**方式 A：先下载再安装**
```bash
python -m pip download parse-czi==0.1.0 -d pkgs
python -m pip install pkgs/parse_czi-0.1.0-py3-none-any.whl
# 或
python -m pip install pkgs/parse_czi-0.1.0.tar.gz
```

**方式 B：从 Release 附件/私有镜像安装**
- `parse_czi-0.1.0-py3-none-any.whl`（11.2 kB）  
- `parse_czi-0.1.0.tar.gz`（12.1 kB）
</details>

---

## 快速上手
最简命令：
```bash
python parse-czi-zenlite-ultrafast <czi_file> <output_dir>
```
并发示例（**推荐 4–8 线程**）：
```bash
python parse-czi-zenlite-ultrafast input.czi output/ --max-workers 8
```
**参数**：
- `czi_file`：输入 CZI 路径（含大尺寸/多通道）
- `output_dir`：输出目录
- `--max-workers`：并行线程数（默认 8）

> 说明：首次运行建议将输出目录置于 NVMe SSD；机械盘可能成为瓶颈。

---

## 输出内容
处理完成后，`<output_dir>` 结构如下：
```
output_dir/
├─ metadata.xml          # CZI 的完整 XML 元数据
├─ channel_0.ome.tif     # 通道 0（例如 DAPI）
├─ channel_1.ome.tif     # 通道 1（例如 FITC）
└─ …
```

---

## 性能基准
> **数据集**：49008 × 46496, 8 通道，原始 ~51GB  
> **平台**：NVMe SSD + 多核 CPU

| 指标           | 原版本 | 优化版本 | 提升倍数 |
|----------------|--------|----------|----------|
| 总处理时间     | 899.25 s | 67.60 s  | **13.3×** |
| 数据加载       | 281.55 s | 27.94 s  | **10.1×** |
| 图像保存       | 617.70 s | 30.03 s  | **20.6×** |

> 备注：性能取决于 I/O、并发与通道数；如为机械盘或低并发，表现会下降。

---

## 常见问题 / 故障排除
- **运行缓慢或卡住**：优先检查磁盘 I/O；将 `--max-workers` 设为 4–8；避免与重 I/O 进程竞争。  
- **保存报错 `"'I' format requires..."`**：属于超大图像保存限制，程序会自动切换 **BigTIFF** 重试。  
- **通道全黑/全白**：确认源文件通道是否有有效信号；必要时关闭归一化或改用 16‑bit 导出。  
- **内存不足**：降低并发；确保有足够 swap；必要时分批处理或迁移到更大内存机器。  
- **需要英文文档**：见文末 [English README](#english-readme)。

---

## 兼容性与依赖
- **Python**：≥ 3.8（建议 3.10/3.11/3.12）  
- **硬件**：建议 **16 GB+ RAM** 与 **NVMe SSD**  
- **核心依赖**：`aicsimageio`, `czifile`, `tifffile`, `numpy`  
- **可选依赖**：`numba`, `psutil`（JIT 加速与资源监控）

> 生产环境建议用 `venv/conda` 隔离，并锁定依赖版本。

---

## 路线图
- 更细粒度 **分块读写** 与内存峰值控制阈值  
- 输出进度条与 **性能剖析**（profiling）报表导出  
- 更多 CZI 变体与维度标注兼容性增强

---

## 贡献
欢迎提交 Issue / PR 改进：
- Bug 复现最小样例（含 CZI 子集或合成数据）
- 性能报告（硬件、线程数、数据规模）
- 新增功能的设计讨论与基准对比

**开发环境**
```bash
git clone https://github.com/luoolu/Parse_CZI.git
cd Parse_CZI
python -m pip install -r requirements.txt
```

**测试**
```bash
pytest -q
```

---

## 许可证
MIT License（详见 `LICENSE`）。

---

## English README

### Overview
**Parse_CZI** targets very large **CZI** images (e.g., from **Zeiss Axio Scan7**) and provides high‑throughput channel export (OME‑TIFF) and complete XML metadata extraction. It is designed as a fast **CLI** plus an embeddable **Python package**.

### Install
```bash
python -m pip install -U parse-czi
# or pin:
python -m pip install parse-czi==0.1.0
```

### Quick Start
```bash
python parse-czi-zenlite-ultrafast <czi_file> <output_dir>
# parallelism (recommend 4–8 workers)
python parse-czi-zenlite-ultrafast input.czi output/ --max-workers 8
```

### Outputs
```
output_dir/
├─ metadata.xml
├─ channel_0.ome.tif
├─ channel_1.ome.tif
└─ …
```

### Benchmarks
Dataset 49008×46496, 8 channels (~51GB):
- Total: 899.25 → 67.60 s (**13.3×**)
- Load: 281.55 → 27.94 s (**10.1×**)
- Save: 617.70 → 30.03 s (**20.6×**)

### Requirements
Python ≥ 3.8; NVMe SSD recommended. Core deps: `aicsimageio`, `czifile`, `tifffile`, `numpy`; optional: `numba`, `psutil`.

---

> 如果你希望我把 README 直接 PR 到仓库，或生成同款 **Release 文案**，告诉我分支与目标版本即可。
