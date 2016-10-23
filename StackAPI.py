# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 19:59:00 2016

@author: Klym
"""
import httplib, urllib, zlib, json

class StackAPI(object):

    OAuth_KEY = '9exEtZTa)9zfaIxbCIgdEA(('
    
    def __init__(self):
        self.conn = httplib.HTTPSConnection("api.stackexchange.com")
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept-Encoding' : 'gzip'}
    
    def __del__(self):
        self.conn.close()
    
    def get(self, category, params):
        params['key'] = StackAPI.OAuth_KEY
        params['order'] = 'desc'
        params['site'] = 'stackoverflow'
        params = urllib.urlencode(params)
        self.conn.request("GET", "/2.2/%s?%s" % (category, params), "", self.headers)
        data = self.readResponse()
        return data

    def readResponse(self):
        response = self.conn.getresponse()    
        if response.status == 200:
            dataJSON = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)            
            parseData = json.loads(dataJSON)["items"]
            if len(parseData) is 0:
                return None
            return parseData
        else:
            print response.status, response.reason
        return None