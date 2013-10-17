#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from xml.dom import minidom




def daum( id ) :
    url = 'http://cartoon.media.daum.net/webtoon/rss/%s'%id
    f = urllib.urlopen(url)
    dom = minidom.parse(f)
    Toontitle = dom.getElementsByTagName('title')[0].lastChild.nodeValue
    lastest = dom.getElementsByTagName('item')[0]
    title = lastest.getElementsByTagName('title')[0].lastChild.nodeValue
    link = lastest.getElementsByTagName('link')[0].lastChild.nodeValue
    print Toontitle, title,link

if __name__ == '__main__':
    daum('miseng')
    daum('afterwedding')

