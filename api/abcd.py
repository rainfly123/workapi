#!/usr/bin/python
#-*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import shutil
import os
import cjson
import mysql
import string
import random


STORE_PATH="/home/rain/www/html"
ACCESS_PATH="http://192.168.1.155:8080/"

def getFileName():
    source = list(string.lowercase) 
    random.shuffle(source)
    temp = source[:15]
    return "".join(temp)

class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='upload' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
''')

    def post(self):
        file_metas = self.request.files['file']   
        for meta in file_metas:
            suffix = os.path.splitext(meta['filename'])[1]
            filename = getFileName() + suffix
            filepath = os.path.join(STORE_PATH, filename)
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            self.write(ACCESS_PATH + filename)

class ApplyLiveHandler(tornado.web.RequestHandler):
    def get(self):
        result = dict()
        result['message'] = "OK"
        result['code'] = 0

        userid = self.get_arguments("userid", strip=True)
        name = self.get_arguments("name", strip=True)
        gender = self.get_arguments("gender", strip=True)
        idc = self.get_arguments("idc", strip=True)
        image = self.get_arguments("image", strip=True)

        try:
            userid = userid[0]
            idc = idc[0]
            name = name[0].encode("utf-8")
            gender = gender[0].encode("utf-8")
            image = "http://live.66boss.com/" + image[0]
            mysql.ApplyLive(userid, name, gender, idc, image)
        except:
            result['message'] = "parameter error"
            result['code'] = 1

        self.write(cjson.encode(result))

class HasLiveHandler(tornado.web.RequestHandler):
    def get(self):
        result = dict()
        userid = self.get_arguments("userid", strip=True)

        try:
            result = mysql.HasLive(userid[0])
        except:
            result['message'] = "parameter error"
            result['code'] = 1
        self.write(cjson.encode(result))



app=tornado.web.Application([
    (r'/upload',UploadFileHandler),
    (r'/haslive', HasLiveHandler),
    (r'/applylive', ApplyLiveHandler),
])

if __name__ == '__main__':
    app.listen(3000)
    print getFileName()
    tornado.ioloop.IOLoop.instance().start()
