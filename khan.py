#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import BeautifulSoup

def http_get( url ):
    request = urllib2.Request( url )
    request.add_header('Referer', url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13')
    response = urllib2.urlopen(request)
    return response


def dori():
    url = 'http://m.khan.co.kr/news_sub_list.html?code=36'
    html = http_get(url).read().decode('cp949').encode('utf-8')
    chunk = '<a href="view.html?category=&med_id=khan&artid='
    idx = html.find(chunk)
    while idx != -1 :
        html = html[idx+len(chunk):]
        idx = html.find('&')
        artid = html[:idx]
        idx = html.find('<span class="title">')
        html = html[idx+len('<span class="title">'):]
        idx = html.find('</span>')
        title = html[:idx]
        idx = html.find('<span class="date">')
        html = html[idx+len('<span class="date">'):]
        idx = html.find('</span>')
        date = html[:idx]
        #print title,artid,date
        if title == '[장도리]':
            return {'toon':'장도리','title':date,'link':'http://m.khan.co.kr/view.html?category=&med_id=khan&artid=%s'%artid}
        idx = html.find(chunk)

    
if __name__ == '__main__':
    print dori() 
