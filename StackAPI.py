# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 19:59:00 2016

@author: Klym
"""
import httplib, urllib, zlib, json

class StackAPI(object):

    OAuth_KEY = '9exEtZTa)9zfaIxbCIgdEA(('
    errors = 0
    
    def __init__(self):
        self.connect()
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept-Encoding' : 'gzip'}
    
    def __del__(self):
        self.conn.close()
    
    def connect(self):
        self.conn = httplib.HTTPSConnection("api.stackexchange.com")
    
    def get(self, category, params):
        params['key'] = StackAPI.OAuth_KEY
        params['order'] = 'desc'
        params['site'] = 'stackoverflow'
        params = urllib.urlencode(params)
        self.conn.request("GET", "/2.2/%s?%s" % (category, params), "", self.headers)
        data, has_more, backoff = self.read_response()
        return data, has_more, backoff

    def read_response(self):
        try:
            response = self.conn.getresponse()
        except httplib.HTTPException as e:
            StackAPI.errors += 1
            raise Exception(e.message)
        dataJSON = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)            
        json_data = json.loads(dataJSON)
        if response.status == 200:
            pass
        else:
            err_str = "%s %s\n%s" % (response.status, response.reason, json_data["error_message"])
            StackAPI.errors += 1
            raise Exception(err_str)
        return json_data["items"], json_data["has_more"], json_data.get("backoff", 0)