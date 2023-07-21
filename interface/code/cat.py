import json

import requests

encoding = '2'
def getunionid(code):
    appid = 'wx892666f0ea3b287d'
    secret = '37d015b48a04d7238cc916ab0146aa94'
    grant_type = 'authorization_code'
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' \
          + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=' + grant_type \
        # 将所需信息添加进url
    res = requests.get(url)  # 调用微信官方接口，获取返回信息。
    data = json.loads(res.text)  # 解码得到用户唯一标识
    return data['openid']


def xxx():
    global encoding
    print(encoding)