#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import BeautifulSoup
import MySQLdb
import dbpass
import fblib
import khan
from xml.dom import minidom

naver_webtoon = {
 '신의탑':'183559',
 '생활의참견':'25613',
 '마음의소리':'20853',
 '역전야매요리':'409630',
 '노블레스':'25455',
 '선천적얼간이들':'478261',
 '사랑일까':'492659',
 '당신만 몰라':'459545',
 '레사':'478262',
 '방과 후 전쟁활동':'517773',
 '복학왕':'626907',
 '기사도':'471181',
 '웃지 않는 개그반':'503253',
 '전자오락수호대':'637931',
 '...':'675554',
 '이말년 서유기':'602921',
 '...':'597481',
 '...':'119874',
 '...':'651673'
}

daum_webtoon = {
 '미생':'miseng',
 '결혼해도 똑같네':'afterwedding',
 '마녀':'witchlove',
 '잉어왕':'petermon',
 '묘진전':'godstory',
 '여행해도 똑같네':'travelwithdonggu'
}

db = None
def connectDB():
    global db
    if db :
        return db
    db = MySQLdb.connect('localhost', dbpass.id, dbpass.passwd, dbpass.dbname)
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    return db

def checkDup(link):
    cur = db.cursor()
    r = cur.execute('select * from webtoon where link like %s', (link))
    return r > 0

def insertDb(toon,title,link):
    cur = db.cursor()
    r = cur.execute('insert into webtoon (toon,link,title) values ( %s, %s, %s)',(toon,link,title))

def http_get( url ):
    request = urllib2.Request( url )
    request.add_header('Referer', url)
    request.add_header('Referer', url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13')
    response = urllib2.urlopen(request)
    return response


def naverToon(toonid):
    url = 'http://comic.naver.com/webtoon/list.nhn?titleId=%s'%(toonid)
    html = http_get(url).read()
    chunk = '<td class="title">'
    chunk2 = '<a href="'
    idx = html.find('<div class="detail">')
    html = html[idx+10:]
    idx = html.find('<h2>')
    html = html[idx+4:]
    idx = html.find('<')
    toonTitle = html[:idx].strip()
    idx = html.find(chunk)
    html = html[idx+len(chunk):]
    idx = html.find(chunk2)
    html = html[idx+len(chunk2):]
    idx = html.find('"')
    link = html[:idx]
    html = html[idx+1:]
    idx = html.find('>')
    html = html[idx+1:]
    idx = html.find('<')
    title = html[:idx]
    link = 'http://comic.naver.com'+link
    return {'toon':toonTitle,'title':title,'link':link}

def daumToon( id ) :
    url = 'http://cartoon.media.daum.net/webtoon/rss/%s'%id
    f = urllib.urlopen(url)
    dom = minidom.parse(f)
    toonTitle = dom.getElementsByTagName('title')[0].lastChild.nodeValue
    lastest = dom.getElementsByTagName('item')[0]
    title = lastest.getElementsByTagName('title')[0].lastChild.nodeValue
    link = lastest.getElementsByTagName('link')[0].lastChild.nodeValue
    toonTitle = toonTitle.encode('utf-8')
    title = title.encode('utf-8')
    link = link.encode('utf-8')

    return {'toon':toonTitle, 'title':title, 'link': link}

def crawling() :
    token = open('access_token.txt','r').read()
    pageid = '163794787090004'
    pagetoken = token #fblib.getPageToken(token,pageid)

    toon = naverToon('675554')
    toon['link'] = toon['link'].split('weekday=')[0]
    print toon['toon'],toon['title'],toon['link']
    if not checkDup(toon['link']) :
        insertDb(toon['toon'], toon['title'], toon['link'])
        msg = '%s / %s'%(toon['toon'],toon['title'])
        fblib.PostPageLink(pageid, pagetoken,msg,toon['link'])
    for key in naver_webtoon.values():
        toon = naverToon(key)
        toon['link'] = toon['link'].split('weekday=')[0]
        print toon['toon'],toon['title'],toon['link']
        if not checkDup(toon['link']) :
            insertDb(toon['toon'], toon['title'], toon['link'])
            msg = '%s / %s'%(toon['toon'],toon['title'])
            fblib.PostPageLink(pageid, pagetoken,msg,toon['link'])
    for key in daum_webtoon.values():
        toon = daumToon( key )
        print toon['toon'],toon['title'],toon['link']
        if not checkDup(toon['link']) :
            insertDb(toon['toon'], toon['title'], toon['link'])
            msg = '%s / %s'%(toon['toon'],toon['title'])
            fblib.PostPageLink(pageid, pagetoken,msg,toon['link'])

    #toon = khan.dori()
    #print toon['toon'],toon['title'],toon['link']
    #if not checkDup(toon['link']) :
    #    insertDb(toon['toon'], toon['title'], toon['link'])
    #    msg = '%s / %s'%(toon['toon'],toon['title'])
    #    fblib.PostPageLink(pageid, pagetoken,msg,toon['link']) 
        


if __name__ == '__main__':
    connectDB()
    crawling()
