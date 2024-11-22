import requests
import sys
version = sys.version_info
if version < (3, 0):
    print('python版本过低，请使用python3+')
    sys.exit()
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ttt = """360-QUAKE搜索引擎
"""
print(ttt)

email = '123@qq.com'  # 账号，可不填
key = ''
maxcount = 10000

headers = {'Content-Type': 'application/json', "X-QuakeToken": key}
count = 0
starts = 0
result_filename = 'result/quake_result.txt'
text = str(input('请输入查询语法：'))
with open(result_filename, 'a', encoding='utf-8') as f:
    f.write(text + '\n')
keyword = text
while True:
    try:
        data = {"query": keyword, "start": starts, "size": 100}
        url = 'https://quake.360.cn/api/v3/search/quake_service'
        req = requests.post(url, data=json.dumps(data), verify=False, headers=headers, timeout=50)
        rsp = json.loads(req.text)
        starts = starts + 100
        if len(rsp['data']) >= 1:
            for xxx in rsp['data']:
                try:
                    if 'http/ssl' == xxx['service']['name']:
                        count = count + 1
                        print('https://' + xxx['service']['http']['host'] + ':' + str(xxx['port']), xxx['service']['http']['title'], '\t第：' + str(count))
                        with open(result_filename, 'a', encoding='utf-8') as f:
                            f.write('https://' + xxx['service']['http']['host'] + ':' + str(xxx['port']) + '\t' + str(xxx['service']['http']['title']) + '\n')
                    elif 'http' == xxx['service']['name']:
                        count = count + 1
                        print('http://' + xxx['service']['http']['host'] + ':' + str(xxx['port']), xxx['service']['http']['title'], '\t第：' + str(count))
                        with open(result_filename, 'a', encoding='utf-8') as f:
                            f.write('http://' + xxx['service']['http']['host'] + ':' + str(xxx['port']) + '\t' + str(xxx['service']['http']['title']) + '\n')
                    else:
                        count = count + 1
                        print(str(xxx['service']['name']) + '\t' + str(xxx['ip']) + '\t' + str(xxx['hostname']) + str(xxx['port']), '\t第：' + str(count))
                        with open(result_filename, 'a', encoding='utf-8') as f:
                            f.write(str(xxx['service']['name']) + '\t' + str(xxx['ip']) + '\t' + str(xxx['hostname']) + str(xxx['port']) + '\n')
                except Exception as e:
                    pass
        else:
            if count != 0:
                print('本次检索到', count, '条数据，结果保存在' + result_filename)
                sys.exit()
            elif count == 0:
                print('本次检索到', count, '条数据')
                os.remove(result_filename)
                sys.exit()
        if count >= maxcount:
            print('本次检索到', count, '条数据，结果保存在' + result_filename)
            sys.exit()
    except Exception as e:
        try:
            if req.status_code == 401:
                print('无效的key')
                os.remove(result_filename)
                sys.exit()
        except Exception as e2:
            pass
        os.remove(result_filename)
        print('出错啦', e)
        sys.exit()
