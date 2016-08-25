#!/usr/bin/env python
#coding=utf-8

import time
import json
import hashlib
import requests

def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()

appKey = '57b7e87ee0f55aa3be003eca'
appMasterSecret = 'xlt6dfvq2a6e3qu06t3am27fucq3xmjp'

def send(body, appmastersecret, url = 'http://msg.umeng.com/api/send', method = 'POST'):
    post_body = json.dumps(body)
    sign = md5('{}{}{}{}'.format(method, url, post_body, appmastersecret))
    r = requests.post(url + '?sign=' + sign, data=post_body)


def message(title, text, alias, url = 'http://www.66boss.com'):
    timestamp = int(time.time() * 1000)
    body = {'appkey': appKey,
          'timestamp': timestamp,
          'type': 'customizedcast',
          'alias_type': 'QQ',
          'alias': alias,
          'payload': {'body': {'ticker': '老板找你:)',
                               'title': title,
                               'text': text,
                               'url': url,
                               'custom':'CaiGe',
                               'after_open': 'go_app'},
                     'display_type':'notification'
                     }
          }

    send(body, appMasterSecret)

if __name__ == '__main__':
    message("新消息", "我要一百万", 'xcc')
