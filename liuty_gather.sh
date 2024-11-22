#!/bin/bash

BLUE='\033[34m'
GREEN='\033[32m'
NC='\033[0m'

chmod +x ./sh/*.sh

echo -e "${BLUE}正在检查环境...${NC}"
if [ -d "./OneForAll/results" ]; then
    rm -f ./OneForAll/results/*.csv
    if [ $? -eq 0 ]; then
        echo -e "${BLUE}稍等一下..${NC}"
    else
        echo -e "${RED}稍等一下.${NC}"
        exit 1
    fi
else
    echo -e "${RED}稍等一下下.${NC}"
    exit 1
fi

if [ "$1" = "-u" ]; then
    URL="$2"
    shift 2
else
    echo -e "${BLUE}Usage: $0 -u <URL>${NC}"
    exit 1
fi

echo -e "${BLUE}开始使用360Quake进行资产测绘...${NC}"
python3 quake.py

echo -e "${BLUE}正在提取url中...${NC}"
./sh/tiqu.sh

echo -e "${BLUE}开始使用oneforall进行子域名收集...${NC}"
python3 ./OneForAll/oneforall.py --target "$URL" run

echo -e "${BLUE}正在提取url中...${NC}"
./sh/tiqu2.sh

echo -e "${BLUE}正在将收集到的url进行合并+去重...${NC}"
./sh/quchong.sh

echo -e "${BLUE}开始进行存活检测...${NC}"
./windfire/windfire-linux-amd64 -f ./result/url.txt -o ./windfire/live.csv

echo -e "${BLUE}开始进行url提取...${NC}"
./sh/tiqu3.sh

echo -e "${BLUE}开始进行js检测...${NC}"
python3 ./jsfinder/JSFinder.py -f ./result/urls.txt -ou ./result/jsresult.txt

echo -e "${BLUE}开始整理js扫描结果...${NC}"
./sh/quchu.sh

echo -e "${BLUE}开始批量域名反查ip...${NC}"
python3 nslookup_ip.py

rm ./result/url.txt ./result/jsresult.txt

echo -e "${BLUE}扫描完成！！IP结果请查看文件：result/resolved_ip.txt，URL及子域名结果请查看文件：result/urls.txt，JS检测结果请查看文件：result/jsresult.txt${NC}"
