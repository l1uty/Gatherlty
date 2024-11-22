#!/bin/bash

# 定义输入文件
file1="./result/result1.txt"
file2="./result/result2.txt"

# 定义输出文件
output_file="./result/url.txt"

# 合并两个文件，并去除重复行，然后保存到输出文件
sort -u $file1 $file2 > $output_file

# 检查输出文件是否创建成功
if [ -f "$output_file" ]; then
    echo "URLs已合并并去重，保存到文件：$output_file"
    # 删除原始文件
    rm $file1
    rm $file2
    echo "已删除原始文件：$file1 和 $file2"
else
    echo "合并或保存过程中出错"
fi
