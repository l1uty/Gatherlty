#!/bin/bash

dir_path="./windfire/"  # 请替换为实际的oneforall/target目录路径
csv_file=$(ls $dir_path/*.csv)  
output_file="./result/urls.txt"

if [ -z "$csv_file" ]; then
    echo "未找到CSV文件"
    exit 1
fi

awk -F, '{if (NR==1) header=$0; else print $5}' $csv_file > $output_file

echo "URLs已提取到文件: $output_file"
