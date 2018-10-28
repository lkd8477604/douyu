#-*- coding:utf-8 -*-
#_author:John
#date:2018/10/25 0:07
#softwave: PyCharm
import requests
import json
from multiprocessing import Pool
import pymongo
import datetime

client = pymongo.MongoClient('localhost')
db = client['douyu']
cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def single_page_info(page):
    respones = requests.get('https://www.douyu.com/gapi/rkc/directory/0_0/{}'.format(page))
    datas = json.loads(respones.text)
    items = datas['data']['rl']
    for item in items:
        data = {
            '标题': item['rn'],
            '主播': item['nn'],
            '人气': item['ol'],
            '类别': item['c2name'],
            '房间号': item['rid'],
            '时间': cur_time
        }
        # 不保存相同时间相同主播名的记录
        if db['host_infos'].update({'主播': data['主播'], '时间': data['时间']}, {'$set': data}, True):
            print('Save to Mongo, {}'.format(data))
        else:
            print('Save to Mong fail, {}'.format(data))
    print('已经完成第{}页'.format(page))

if __name__ == '__main__':
    pool = Pool()
    #多线程抓200页
    pool.map(single_page_info, [page for page in range(1, 201)])