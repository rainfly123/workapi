#!/usr/bin/env python
import os
import cjson
import tornado
import tornado.ioloop
import tornado.web
import mysql
import qiniu
import datetime
from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen
import urllib
import string
import random
import json

ACCESS_URL = "http://live.66boss.com/livepic/"
STORE_PATH="/live/www/html/applylive/"
ACCESS_PATH="http://live.66boss.com/applylive/"

class QueryHandler(tornado.web.RequestHandler):
    def get(self):
        results = list()
        resp = dict() 

        temp = self.get_arguments("ownerid", strip=True)
        owners = temp[0].split(',')
        resp['code'] =  0
        resp['message'] =  mysql.ERROR[0]
        resp['channels'] = results
        for owner in owners:
            try:
                ownerid = int(owner)
                result = mysql.Query(ownerid)
                results.append(result)
            except:
                resp['message'] = "parameter error"
                resp['code'] = 1
                break

        self.write(cjson.encode(resp))

class QueryMyHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        temp = self.get_arguments("ownerid", strip=True)
        resp['code'] =  0
        resp['message'] =  mysql.ERROR[0]
        try:
            ownerid = int(temp[0])
            result = mysql.QueryMy(ownerid)
            resp['channels'] = result
        except:
            resp['message'] = "parameter error"
            resp['code'] = 1

        self.write(cjson.encode(resp))

class QueryAllHandler(tornado.web.RequestHandler):
    def get(self):
        result = dict()
        shop = "1"  #default shop
        keywords = None  #default keywords

        resp = self.get_arguments("shop", strip=True)
        if len(resp) > 0 and len(resp[0]) > 0:
            shop = resp[0]

        respk = self.get_arguments("keywords", strip=True)
        if len(respk) > 0 and len(respk[0]) > 0:
            keywords = respk[0].encode("utf-8")

        try:
            result = mysql.QueryAll(shop, keywords)
        except:
            result['message'] = "parameter error"
            result['code'] = 1

        self.write(cjson.encode(result))

class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        result = dict()
        liveid = self.get_arguments("liveid", strip=True)
        try:
            result = mysql.Detail(liveid[0])
        except:
            result['message'] = "parameter error"
            result['code'] = 1

        self.write(cjson.encode(result))


class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        result = dict()
        liveid = self.get_arguments("liveid", strip=True)
        try:
            result = mysql.Delete(liveid[0])
        except:
            result['message'] = "parameter error"
            result['code'] = 1

        self.write(cjson.encode(result))


class SupportHandler(tornado.web.RequestHandler):
    def get(self):
        result = dict()
        liveid = self.get_arguments("liveid", strip=True)
        userid = self.get_arguments("userid", strip=True)
        try:
            result = mysql.Support(liveid[0], userid[0])
        except:
            result['message'] = "parameter error"
            result['code'] = 1

        self.write(cjson.encode(result))

class CreateHandler(tornado.web.RequestHandler):
    def get(self):
        result = dict()
        ownerid = self.get_arguments("ownerid", strip=True)
        ownerid = int(ownerid[0])
        title = self.get_arguments("title", strip=True)
        title = title[0].encode("utf-8")
        time = self.get_arguments("startime", strip=True)[0]
        mystr = ""
        shop = self.get_arguments("shop", strip=True)
        if len(shop) > 0 and len(shop[0]) > 0:
            shopstr = shop[0]
        else:
            shopstr = "1"

        publicstr = "1"
        public = self.get_arguments("public", strip=True)
        if len(public) > 0:
            publicstr = public[0]

        try:
            datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            mystr = time
        except:
            mystr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        resp = qiniu.CreateLiveStream()

        cover = self.get_arguments("snapshot", strip=True)
        coverstr = None
        if len(cover) > 0 and len(cover[0]) > 0:
            coverstr = cover[0]

        if coverstr == None:
            result = mysql.Create(ownerid, resp, title, mystr, shopstr, publicstr)
        else:
            result = mysql.Create(ownerid, resp, title, mystr, shopstr, publicstr, (ACCESS_URL + coverstr))

        params = {"liveid": resp['liveid']}
        url = url_concat("http://127.0.0.1:12345/newchannel?", params)
        http_client = AsyncHTTPClient()
        non = http_client.fetch(url)

        products = self.get_arguments("products", strip=True)
        if len(products) > 0 and len(products[0]) > 0:
            productsl =  products[0].split(',')
            mysql.SaveProducts(resp['liveid'], productsl)

        self.write(cjson.encode(result))

class ProductHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        URL = "http://webapi/app/supplier.php?act=get_goods_detail"
        result = dict()
        liveid = self.get_arguments("liveid", strip=True)
        try:
            result = mysql.Products(liveid[0])
        except:
            result['message'] = "parameter error"
            result['code'] = 1
            self.write(cjson.encode(result))
            return

        result['goods_detail'] = list()
        for good in result['goods']:
            client = tornado.httpclient.AsyncHTTPClient()
            temp = dict()
            temp['goods_id'] = good
            data = urllib.urlencode(temp)
            response = yield client.fetch(URL, method='POST', body=data)
            response = json.loads(response.body)
            result['goods_detail'].append(response['result'])

        self.write(cjson.encode(result))

class StopHandler(tornado.web.RequestHandler):
    def get(self):
        liveid = self.get_arguments("liveid", strip=True)
        try:
            result = qiniu.StopRTMP(liveid[0])
        except:
            pass

        self.write("OK")

class StopChanHandler(tornado.web.RequestHandler):
    def get(self):
        liveid = self.get_arguments("liveid", strip=True)
        if len(liveid) > 0 and len(liveid[0]) > 0:
            liveid = liveid[0]

        params = {"liveid": liveid}
        url = url_concat("http://127.0.0.1:12345/stopchannel?", params)
        http_client = AsyncHTTPClient()
        non = http_client.fetch(url)
        self.write("OK")



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
    <form action='http://live.66boss.com/api/upload' enctype="multipart/form-data" method='post'>
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
            image = ACCESS_PATH + image[0]
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

application = tornado.web.Application([
    (r"/query", QueryHandler),
    (r"/queryall", QueryAllHandler),
    (r"/querymy", QueryMyHandler),
    (r"/delete", DeleteHandler),
    (r"/detail", DetailHandler),
    (r"/support", SupportHandler),
    (r"/create", CreateHandler),
    (r"/products", ProductHandler),
    (r"/stop", StopHandler),
    (r"/stopchan", StopChanHandler),

    (r'/upload',UploadFileHandler),
    (r'/haslive', HasLiveHandler),
    (r'/applylive', ApplyLiveHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

