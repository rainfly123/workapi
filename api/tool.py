#!/usr/bin/env python
from pili import *

access_key = "_x8qeD4FD5BGveRZ3SC_2_7StAUl_T7O9Sxz-e9X"
secret_key = "mIEuQoIsUHw5eEgMhESAoDmQDXiw7tQVApcKue-E"

publish_key = "7cf0e739-8f53-4264-bea2-72aee33218e7"
hub_name   = "66boss"

credentials = Credentials(access_key, secret_key)
hub = Hub(credentials, hub_name)
stream = hub.create_stream(title=None, publishKey=publish_key, publishSecurity="static")
print  stream.to_json()
stream = hub.get_stream(stream_id="z1.66boss.xiechc")
# return stream object...
status = stream.status()
print status
url = stream.rtmp_publish_url()
print url
urls = stream.rtmp_live_urls()
for k in urls:
    print k, ":", urls[k]

urls = stream.hls_live_urls()
for k in urls:
    print k, ":", urls[k]
