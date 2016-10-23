# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:00:04 2016

@author: Klym
"""
from db import DataBase
from StackAPI import StackAPI
import time

def main():
    stackapi = StackAPI()
    db = DataBase()
    
    start_time = time.time()
    '''    
    params = {'pagesize': 100, 'sort': 'reputation', 'filter': '!BTeL*ManaQamixcFXChIJdmUWwxR(9'}
    for i in range(1, 100):
        params['page'] = i
        users = stackapi.get('users', params)
        if users is None:
            break
        db.insertUsers(users)
    '''
    
    params = {'pagesize': 100, 'sort': 'popular'}
    count = 0    
    for i in range(1, 470):
        params['page'] = i
        tags = stackapi.get('tags', params)
        if tags is None:
            break
        tmpCnt = db.insertTags(tags)
        count += tmpCnt
        
    print "Добавлено строк в базу: %s" % count
    print "Время обработки: {:.3f} sec".format(time.time() - start_time)
    
    del stackapi
    del db
    
if __name__ == "__main__":
    main()