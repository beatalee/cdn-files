# -*- coding: utf-8 -*-
import uuid
import requests
import hashlib
import time

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '2a379572e1eBB267'
APP_SECRET = 'x7Xm1Bke21r6riW0912pCXfySpzVH5f4IvHN'
### 8>B; wp 

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(pre_str, l_from='EN',l_go='zh-CHS'):
    q = pre_str
    data = {}
    data['from'] = l_from
    data['to'] = l_go
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    import json
    data = json.loads(str(response.content.decode("utf-8")))
    if int(data["errorCode"]) != 0:
        return {"response": {"translation": None, "origin_str": q}}

    return {"response": {"translation": data["translation"], "origin_str": q, "errorCode":data["errorCode"]}}



def translate_en2cn(content):
    return connect(content)["response"]["translation"]