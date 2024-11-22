#!/bin/bash

# 定义输入文件和输出文件
input_file="./result/quake_result.txt"
output_file="./result/result1.txt"

# 检查输入文件是否存在
if [ ! -f "$input_file" ]; then
    echo "输入文件不存在: $input_file"
    exit 1
fi

# 提取URL并保存到输出文件
grep -oP 'http[s]?://\S*' "$input_file" | sort -u > "$output_file"

# 检查输出文件是否创建成功
if [ -f "$output_file" ]; then
    # 输出结果
    echo "Quake中的URLs已提取到文件: $output_file"
    # 删除原文件
    rm "$input_file"
    echo "已删除原文件：$input_file"
else
    echo "提取或保存过程中出错"
fi
