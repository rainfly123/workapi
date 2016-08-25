#!/usr/bin/env python
#coding=utf-8
import os
import cjson
import tornado
import tornado.ioloop
import tornado.web
import datetime
from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen
import urllib
import string
import random
import json
import cache
import pushclient

class SendHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        users = self.get_arguments("users", strip=True)
        message = self.get_arguments("message", strip=True)
        msgtype = self.get_arguments("msgtype", strip=True)
        if len(users) < 0 or len(message) < 0  or len(msgtype) < 0:
            self.write('{"error":1, "message":"wrong argument"}')
            return
        print message, users, msgtype
        users = users[0].split(',')
        message = message[0]
        msgtype = msgtype[0]

        title = cache.msgtypes.get(msgtype)
        if title is None:
            self.write('{"error":1, "message":"wrong argument"}')
            return
        for user in users:
            cache.Cache.q.put((user, msgtype, message))
        self.write('{"error":0, "message":"OK"}')



application = tornado.web.Application([
    (r"/send", SendHandler),
])

if __name__ == "__main__":
    t=cache.Cache()
    t.setDaemon(True)
    t.start()
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()


