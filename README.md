---

# CZIMetaData

## 项目概述

该项目用于解析 Zeiss Axio Scan7 产生的 CZI 文件，主要功能包括：
1. **提取 XML 元数据**：从 CZI 文件中提取完整 XML 元数据，并保存为 `metadata.xml`。
2. **通道信息解析**：从 XML 元数据中解析各通道信息，包括通道名称、是否激活以及是否采集等。
3. **融合图数据读取**：利用 [AICSImageIO](https://github.com/AllenCellModeling/aicsimageio) 库获取融合图数据，并保证返回的数据形状包含彩色信息（RGB）。
4. **图像处理与保存**：对每个通道进行简单的 min–max 归一化（转换至 8 位），并利用 [tifffile](https://pypi.org/project/tifffile/) 将图像保存为 BigTIFF/OME‑TIFF 格式文件，输出文件名中包含通道名称。

> **注意**：对于一些 Zen lite 类型的 CZI 文件，可能只有部分通道采集有效数据，其他通道可能全为 0。此时不保存全 0 图像。

## 项目依赖

本项目依赖于以下 Python 库：
- [AICSImageIO](https://github.com/AllenCellModeling/aicsimageio)（用于读取 CZI 文件）  
- [czifile](https://github.com/AllenCellModeling/czifile)（备用的 CZI 文件读取库）  
- [tifffile](https://pypi.org/project/tifffile/)（用于保存超大 TIFF 图像）  
- [numpy](https://numpy.org/)  
- [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)（Python 标准库，用于 XML 解析）  
- [argparse](https://docs.python.org/3/library/argparse.html)（Python 标准库，用于命令行参数解析）  
- [logging](https://docs.python.org/3/library/logging.html)（Python 标准库，用于日志输出）

安装所需库的命令示例如下：

```bash
pip install aicsimageio czifile tifffile numpy
```

## 使用方法

### 命令行运行

将代码保存为 `parse_czi_zenlite.py`，然后使用以下命令运行：

```bash
python parse_czi_zenlite.py <czi_file> <output_dir>
```

其中：
- `<czi_file>` 为输入的 CZI 文件路径。
- `<output_dir>` 为输出目录路径，处理后会在该目录下生成：
  - `metadata.xml`：保存的 CZI 文件 XML 元数据；
  - 各通道图像文件，文件名格式为 `<通道名称>.ome.tif`。

### 示例

```bash
python parse_czi_zenlite.py /path/to/your/file.czi /path/to/output/
```

## 代码说明

### 1. 元数据提取与通道解析

- **save_metadata()**  
  使用 AICSImageIO 读取 CZI 文件后，尝试获取 `img.metadata.raw` 属性；若不存在，则转换为字符串。最终将 XML 元数据保存为 `metadata.xml`。

- **parse_xml_string()**  
  对获取的 XML 字符串去除无效字符后，使用 Python 标准库 `xml.etree.ElementTree` 解析为 XML Element 对象。

- **parse_channels()**  
  从解析后的 XML 中读取 `<MultiTrackSetup>/<Track>/<Channels>/<Channel>` 节点，提取各通道的属性（名称、IsActivated、IsSelected）。

### 2. 融合图数据读取

- 项目使用 AICSImageIO 的 `get_image_data("SCYX", squeeze=False, S=0, T=0)` 方法读取融合图数据，并要求返回数据形状为 `(1, C, Y, X, 3)`，其中 3 表示彩色（RGB）样本维度。
- 如果 AICSImageIO 返回的数据不包含彩色维度，则自动尝试使用 czifile 获取数据。

### 3. 图像处理与保存

- **min_max_scale_to_8bit()**  
  对图像进行简单的 min–max 归一化，将像素值拉伸到 0～255，并转换为 uint8 类型。

- 对于每个通道，先检测整个图像数据是否全为 0（全为 0 则跳过保存），否则进行归一化后调用 tifffile 保存为 BigTIFF/OME‑TIFF 格式，保存时指定 `photometric="rgb"`，保证保存的图像为彩色。


## 注意事项

- **XML 解析问题**  
  如果 XML 元数据中存在不合法的字符，可能会导致解析错误。此时可参考 XML 清洗方案或直接使用 `img.metadata` 的原始内容。

- **数据形状**  
  代码期望的融合图形状为 (1, C, Y, X, 3)，如果你采集的数据不同（例如单通道或灰度数据），请相应调整代码。

- **环境要求**  
  该代码在 Python 3.x 下测试。请确保 AICSImageIO、czifile、tifffile、numpy 等库版本符合要求。

---

