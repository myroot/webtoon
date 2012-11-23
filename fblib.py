#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

def getPageToken(user_token,pageid) :
    url = 'https://graph.facebook.com/hi.root/accounts?access_token=%s'%(user_token)
    html = urllib.urlopen(url)
    data = json.load(html)
    for x in data['data']:
        print x
        if x['id'] == pageid:
            return x['access_token']


def PostPageLink(pageid, token, msg, link) :
    url = 'https://graph.facebook.com/%s/feed'%(pageid)
    params = {'access_token':token,'message':msg,'link':link}
    params = urllib.urlencode(params)    
    request = urllib2.Request(url, params)
    response = urllib2.urlopen(request)
    #data = json.load(response)
    #print data



if __name__ == '__main__':
    token = open('access_token.txt','r').read()
    pageid = '163794787090004'
    pagetoken = getPageToken(token,pageid)
    PostPageLink(pageid, pagetoken,'테스트','http://naver.com')

