


import pandas as pd
import datetime
import json
import urllib.request
import re


def get_data_from_bao(id,start_date='2010-01-01'):
    now_time = datetime.datetime.now()
    ##数据宝抓取：
    json_dict = {"start_date": start_date,
                 "end_date": datetime.datetime.strftime(now_time, "%Y-%m-%d"),
                 "indexlist": [{"index_id": id}
                               ]}
    # convert json_dict to JSON
    json_data = json.dumps(json_dict)
    # convert str to bytes (ensure encoding is OK)
    post_data = json_data.encode('utf-8')
    url = 'http://datacenter.dunhefund.com:8872/getindexdata'
    # we should also say the JSON content type header
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['username'] = 'jins'  # ID
    headers['password'] = 'Dh$20199'  # Password
    req = urllib.request.Request(url, post_data, headers)
    # send the request
    res = urllib.request.urlopen(req)
    response_data = res.read().decode("utf-8")
    response_json = json.loads(response_data)
    response_df = pd.DataFrame(response_json['data'][0]['indexdata'])


    name = response_json['data'][0]['index_title']
    name = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", name)

    response_df.columns = ['日期',name]
    response_df.index = pd.to_datetime(response_df['日期'])
    del response_df['日期']
    return response_df

