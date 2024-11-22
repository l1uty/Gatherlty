#!/bin/bash

# 定义输入文件和输出文件
input_file="./result/jsresult.txt"
output_file="./result/js_result.txt"

# 检查输入文件是否存在
if [ ! -f "$input_file" ]; then
    echo "输入文件不存在: $input_file"
    exit 1
fi

# 删除以.js、.vue和.css结尾的URL
grep -vE '\.(js|vue|css|svg)$' "$input_file" > "$output_file"

# 输出结果
echo "已经对js扫描进行了整理：$output_file"
