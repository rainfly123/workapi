#!/usr/bin/env python
from pili import *
import cjson
import random, string

access_key = "_x8qeD4FD5BGveRZ3SC_2_7StAUl_T7O9Sxz-e9X"
secret_key = "mIEuQoIsUHw5eEgMhESAoDmQDXiw7tQVApcKue-E"
publish_key = "7cf0e739-8f53-4264-bea2-72aee33218e7"
hub_name   = "66boss"

credentials = Credentials(access_key, secret_key)
hub = Hub(credentials, hub_name)

def random_str(randomlength=12):
    a = list(string.ascii_lowercase)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def CreateLiveStream():
    res = dict()
    stream = hub.create_stream(title=random_str(), publishKey=publish_key, publishSecurity="static")
    res['tojson'] = stream.to_json()

    temp = cjson.decode(res['tojson'])

    res['state'] = 0
    res['liveid'] = temp['id']
    res['publish_url'] = stream.rtmp_publish_url()
    res['rtmp_live_url'] = stream.rtmp_live_urls()['ORIGIN']
    res['hls_live_url'] = stream.hls_live_urls()['ORIGIN']
    res['playback_hls_url'] = ""
    res['createdAt'] = temp['createdAt']
    return res


def StopRTMP(liveid):
    stream = hub.get_stream(liveid)
    try:
        stream.disable()
    except:
        pass

if __name__ == '__main__':
    StopRTMP("z1.66boss.iyzkcvnmrlhx")
