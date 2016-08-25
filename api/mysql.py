#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import MySQLdb
import time
import string
from DBUtils.PooledDB import PooledDB
import dbconfig


ERROR = {0:"OK", 1:"Parameter Error", 2:"Database Error", 3:u"您已赞", 4:u"你无权开通直播"}
Default_Snapshot = "http://7xvsyw.com2.z0.glb.qiniucdn.com/n.jpg"

class DbManager():
    def __init__(self):
        kwargs = {}
        kwargs['host'] =  dbconfig.DBConfig.getConfig('database', 'dbhost')
        kwargs['port'] =  int(dbconfig.DBConfig.getConfig('database', 'dbport'))
        kwargs['user'] =  dbconfig.DBConfig.getConfig('database', 'dbuser')
        kwargs['passwd'] =  dbconfig.DBConfig.getConfig('database', 'dbpassword')
        kwargs['db'] =  dbconfig.DBConfig.getConfig('database', 'dbname')
        kwargs['charset'] =  dbconfig.DBConfig.getConfig('database', 'dbcharset')
        self._pool = PooledDB(MySQLdb, mincached=1, maxcached=15, maxshared=10, maxusage=10000, **kwargs)

    def getConn(self):
        return self._pool.connection()

_dbManager = DbManager()

def getConn():
    return _dbManager.getConn()

def Query(ownerid):
    con = getConn()
    cur =  con.cursor()

    inited = []
    live = []
    stopped = []
    result = {'ownerid': ownerid}

    sql = "select live.liveid, title, snapshot, persons, date_format(startime, '%Y-%m-%d %H:%i') from live, owner \
          where live.liveid = owner.liveid and owner.ownerid = {0} and live.state = 0".format(ownerid)
    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['liveid'] = channel[0]
        temp['title'] = channel[1]
        temp['snapshot'] = channel[2]
        temp['persons'] = channel[3]
        temp['startime'] = channel[4]
        inited.append(temp)

    sql = "select live.liveid, title, snapshot, persons, rtmp_live_url from live, owner \
          where live.liveid = owner.liveid and owner.ownerid = {0} and live.state = 1".format(ownerid)
    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['liveid'] = channel[0]
        temp['title'] = channel[1]
        temp['snapshot'] = channel[2]
        temp['persons'] = channel[3]
        temp['rtmp_live_url'] = channel[4]
        live.append(temp)

    sql = "select live.liveid, title, snapshot, persons, playback_hls_url from live, owner\
          where live.liveid = owner.liveid and owner.ownerid = {0} and live.state = 2".format(ownerid)
    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['liveid'] = channel[0]
        temp['title'] = channel[1]
        temp['snapshot'] = channel[2]
        temp['supports'] = channel[3]
        temp['playback_hls_url'] = channel[4]
        stopped.append(temp)

    result['inited'] = inited
    result['live'] = live
    result['stopped'] =  stopped


    cur.close()
    con.close()
    return result

def QueryMy(ownerid):
    con = getConn()
    cur =  con.cursor()

    inited = list()

    sql = "select live.liveid, state, title, snapshot, tojson, supports, date_format(startime,'%Y-%m-%d %H:%i'),playback_hls_url \
          from live, owner where live.liveid = owner.liveid and owner.ownerid = {0} and live.state != 1 \
          order by live.startime desc".format(ownerid)
    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['liveid'] = channel[0]
        temp['state'] = channel[1]
        temp['title'] = channel[2]
        temp['snapshot'] = channel[3]
        temp['tojson'] = channel[4]
        temp['supports'] = channel[5]
        temp['startime'] = channel[6]
        temp['playback_hls_url'] = channel[7]
        inited.append(temp)
    cur.close()
    con.close()
    return inited


def QueryAll(shop, keywords=None):
    con = getConn()
    cur =  con.cursor()

    inited = []
    live = []
    stopped = []
    result = dict()

    if keywords != None:
        sql = "select live.liveid, title, snapshot, persons, date_format(startime, '%Y-%m-%d %H:%i'),ownerid,public from live,\
            owner where owner.liveid=live.liveid and live.state = 0 and live.shop={0} and \
            live.title like '%{1}%'".format(shop, keywords)
    else:
        sql = "select live.liveid, title, snapshot, persons, date_format(startime, '%Y-%m-%d %H:%i'),ownerid,public from live,\
            owner where owner.liveid=live.liveid and live.state = 0 and live.shop={0}".format(shop)

    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['liveid'] = channel[0]
        temp['title'] = channel[1]
        temp['snapshot'] = channel[2]
        temp['persons'] = channel[3]
        temp['startime'] = channel[4]
        temp['ownerid'] = channel[5]
        temp['public'] = channel[6]
        inited.append(temp)

    if keywords != None:
        sql = "select live.liveid, title, snapshot, persons, rtmp_live_url,ownerid,public from live,\
           owner   where live.liveid=owner.liveid and live.state = 1 and live.shop={0}\
           and live.title like '%{1}%' order by live.persons".format(shop, keywords)
    else:
        sql = "select live.liveid, title, snapshot, persons, rtmp_live_url,ownerid,public from live,\
           owner   where live.liveid=owner.liveid and live.state = 1 and live.shop={0} order by live.persons".format(shop)

    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['liveid'] = channel[0]
        temp['title'] = channel[1]
        temp['snapshot'] = channel[2]
        temp['persons'] = channel[3]
        temp['rtmp_live_url'] = channel[4]
        temp['ownerid'] = channel[5]
        temp['public'] = channel[6]
        live.append(temp)

    if keywords != None:
        sql = "select live.liveid, title, snapshot, supports, playback_hls_url,ownerid,public from live,\
           owner  where live.liveid=owner.liveid and live.state = 2 and live.shop={0}\
           and live.title like '%{1}%' order by live.supports".format(shop, keywords)
    else:
        sql = "select live.liveid, title, snapshot, supports, playback_hls_url,ownerid,public from live,\
           owner  where live.liveid=owner.liveid and live.state = 2 and live.shop={0} order by live.supports".format(shop)

    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['liveid'] = channel[0]
        temp['title'] = channel[1]
        temp['snapshot'] = channel[2]
        temp['supports'] = channel[3]
        temp['playback_hls_url'] = channel[4]
        temp['ownerid'] = channel[5]
        temp['public'] = channel[6]
        stopped.append(temp)

    result['inited'] = inited
    result['live'] = live
    result['stopped'] =  stopped

    result['code'] =  0
    result['message'] =  ERROR[0]

    cur.close()
    con.close()
    return result


def Detail(liveid):
    con = getConn()
    cur =  con.cursor()

    result = {'liveid': liveid}

    sql = "select state,snapshot, title, publish_url, rtmp_live_url, hls_live_url, \
           playback_hls_url, persons, supports, tojson, \
           date_format(startime, '%Y-%m-%d %H:%i') from live where liveid = '{0}' ".format(liveid)
    cur.execute(sql)
    res = cur.fetchall()
    live = res[0]
    if len(live) >= 8 :
        result['state'] = live[0]
        result['snapshot'] = live[1]
        result['title'] = live[2]
        result['publish_url'] = live[3]
        result['rtmp_live_url'] = live[4]
        result['hls_live_url'] = live[5]
        result['playback_hls_url'] = live[6]
        result['persons'] = live[7]
        result['supports'] = live[8]
        result['tojson'] = live[9]
        result['startime'] = live[10]

    cur.close()
    con.close()
    result['code'] =  0
    result['message'] =  ERROR[0]
    return result

def Support(liveid, userid):

    result = dict()

    con = getConn()
    cur =  con.cursor()
    sql = "select liveid from supports where liveid = '{0}' and  userid={1} ".format(liveid, userid)
    cur.execute(sql)
    res = cur.fetchall()
    if len(res) >= 1:
        result['code'] =  3
        result['message'] =  ERROR[3]
        return result

    sql = "update live set supports = supports + 1 where liveid = '{0}' ".format(liveid)
    cur.execute(sql)
    con.commit()

    sql = "insert into supports (liveid,userid) values ('{0}', {1}) ".format(liveid, userid)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

    result['code'] =  0
    result['message'] =  ERROR[0]
    return result

def Delete(liveid):
    con = getConn()
    cur =  con.cursor()

    result = dict()

    sql = "delete from live where liveid = '{0}' ".format(liveid)
    cur.execute(sql)
    con.commit()

    sql = "delete from owner where liveid = '{0}' ".format(liveid)

    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()
    result['code'] =  0
    result['message'] =  ERROR[0]
    return result


def Create(ownerid, channel, title, mystr, shopstr, public, cover=Default_Snapshot):
    con = getConn()
    cur =  con.cursor()

    result = dict()

    #liveid, state, snapshot,title,publish_url,playback_hls_url, rtmp_live_url, persions, supports, tojson, hls_live_url
    sql = "insert into live values('{0}', 0, '{1}', '{2}',\
           '{3}', '{4}', '{5}', 0, 0, '{6}', '{7}', '{8}', {9}, {10}) ".format(channel['liveid'], cover, title,\
            channel['publish_url'], channel['playback_hls_url'],channel['rtmp_live_url'],\
            channel['tojson'], channel['hls_live_url'], mystr, shopstr, public)


    cur.execute(sql)
    con.commit()
    sql = "insert into owner values({0}, '{1}')".format(ownerid, channel['liveid'])
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()
    result['code'] =  0
    result['message'] =  ERROR[0]
    return result

def Products(liveid):

    result = dict()

    con = getConn()
    cur =  con.cursor()
    sql = "select goodsid from products where liveid = '{0}'".format(liveid)
    cur.execute(sql)
    res = cur.fetchall()

    cur.close()
    con.close()
    goods =  [x[0] for x in res]

    result['code'] =  0
    result['message'] =  ERROR[0]
    result['number'] =  len(res)
    result['goods'] =  goods
    return result

def SaveProducts(liveid, products):

    param = [(liveid, product) for product in products]
    print param
    sql = "insert into products (liveid, goodsid) values(%s, %s)"

    con = getConn()
    cur =  con.cursor()
    cur.executemany(sql, param)
    con.commit()
    cur.close()
    con.close()

def ApplyLive(userid, name, gender, idc, imageURL):
    sql = "insert into users values(0, '{0}','{1}', '{2}', '{3}', 0, '{4}')".format(userid, name, gender, idc, imageURL)
    con = getConn()
    cur =  con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

def HasLive(userid):

    result = dict()
    result['code'] =  0
    result['message'] =  ERROR[0]

    sql = "select userid from users where userid='{0}' and approved=1".format(userid)
    con = getConn()
    cur =  con.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    con.close()
    if len(res) == 0:
        result['code'] =  4
        result['message'] =  ERROR[4]
    return result

if __name__ ==  '__main__':
    #print Support("z1.mycs.xiechc",11233)
    import cjson
#    print cjson.encode(Products("13"))
#    print cjson.encode(Products("1"))
#    print Products("b")
    #SaveProducts("z1.66boss.xiechc",['1','2','3'])
    print HasLive('00')
    a = u"王"
    b =u"女"
    ApplyLive("1234", a.encode('utf-8'), b.encode('utf-8'), "133333333333", "afadf.jpg")
