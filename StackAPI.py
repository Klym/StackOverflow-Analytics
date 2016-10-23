# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 19:59:00 2016

@author: Klym
"""
import httplib, urllib, zlib, json

class StackAPI(object):
    
    def __init__(self):
        self.conn = httplib.HTTPSConnection("api.stackexchange.com")
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept-Encoding' : 'gzip'}
    
    def __del__(self):
        self.conn.close()
    
    def getUsers(self, page, pagesize):
        params = {'pagesize': pagesize, 'order': 'desc', 'sort': 'reputation', 'site': 'stackoverflow', 'filter': '!BTeL*ManaQamixcFXChIJdmUWwxR(9', 'key': '9exEtZTa)9zfaIxbCIgdEA(('}
        params["page"] = page
        params = urllib.urlencode(params)
        self.sendRequest('users', params)
        data = self.readResponse()
        if data is not None:
            return data
        return None
        
    def readResponse(self):
        response = self.conn.getresponse()    
        if response.status == 200:
            dataJSON = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
            if json.loads(dataJSON)["has_more"] == False:
                return None
            parseData = json.loads(dataJSON)["items"]
            return parseData
        else:
            print response.status, response.reason
        return None
    
    def sendRequest(self, category, params):
        self.conn.request("GET", "/2.2/%s?%s" % (category, params), "", self.headers)