#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/30/24
# @Author  : luoolu
# @Github  : https://luoolu.github.io
# @Software: PyCharm
# @File    : czi_metaData.py

import czifile
import xml.etree.ElementTree as ET


def read_czi_properties(filename):
    """打开 .czi 文件并获取元数据。"""
    with czifile.CziFile(filename) as czi:
        # 获取元数据
        metadata = czi.metadata()

    return metadata


def save_metadata_to_file(metadata, output_filename):
    """将元数据保存到指定文件。"""
    with open(output_filename, 'w') as file:
        file.write(metadata)


def print_czi_properties(metadata):
    """打印元数据并解析 XML 树。"""
    # 打印元数据的 XML 字符串
    print(metadata)

    # 解析 XML 字符串
    root = ET.fromstring(metadata)

    # 进一步解析 XML 树
    for element in root.findall(".//"):
        print(f"{element.tag}: {element.text}")


if __name__ == '__main__':
    # 使用方法
    filename = '/media/luolu/LOOLO/DATA/tsyy_test.czi'
    metadata = read_czi_properties(filename)

    print_czi_properties(metadata)

    # 将元数据保存到文件
    output_filename = 'czi_metadata.xml'
    save_metadata_to_file(metadata, output_filename)

    print(f"Metadata saved to {output_filename}")
