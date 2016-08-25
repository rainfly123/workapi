#!/usr/bin/python
#-*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import shutil
import os
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

app=tornado.web.Application([
    (r'/upload',UploadFileHandler),
])

if __name__ == '__main__':
    app.listen(3000)
    print getFileName()
    tornado.ioloop.IOLoop.instance().start()
