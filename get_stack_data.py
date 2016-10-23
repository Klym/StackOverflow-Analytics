# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 12:08:29 2016

@author: Klym
"""

import pyodbc, httplib, urllib, zlib, json

server = 'tcp:myserver.database.windows.net'
database = 'mydb'
username = 'myusername'
password = 'mypassword'

#Connection String
connection_str = 'DRIVER={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Database=stackoverflow;Trusted_Connection=Yes;'
with pyodbc.connect(connection_str) as cnxn:
    cursor = cnxn.cursor()
    conn = httplib.HTTPSConnection("api.stackexchange.com")
    try:
        params = urllib.urlencode({'pagesize': 100, 'order': 'desc', 'sort': 'reputation', 'site': 'stackoverflow', 'filter': '!9YdnSBVLT'})
        headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept-Encoding' : 'gzip'}
        
        conn.request("GET", "/2.2/users?%s" % params, "", headers)
        response = conn.getresponse()    
        if response.status == 200:
            dataJSON = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
            parseData = json.loads(dataJSON)["items"]
            for i in range(0, len(parseData)):
                isEmployee = 1 if parseData[i]["is_employee"] else 0
                age = parseData[i].get("age")
                try:
                    cursor.execute("insert into [dbo].[users] ([id], [user_type], [display_name], [age], [reputation], [is_employe], [creation_date], [view_count]) values (?,?,?,?,?,?,?,?)", parseData[i]["user_id"], parseData[i]["user_type"], parseData[i]["display_name"], age, parseData[i]["reputation"], isEmployee, "2016-01-01", parseData[i]["view_count"])
                    cursor.commit()
                except pyodbc.DatabaseError as err:
                    print i, err.args[1].decode("cp1251")
        else:
            print response.status, response.reason
    finally:
        conn.close()
    cursor.close()