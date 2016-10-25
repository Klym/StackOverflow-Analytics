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
    count = 0
    params = {'pagesize': 100, 'sort': 'reputation', 'filter': '!BTeL*ManaQamixcFXChIJdmUWwxR(9'}
    for i in range(1, 10):
        params['page'] = i
        users = stackapi.get('users', params)
        if users is None:
            break
        tmpCnt = db.insert(users, DataBase.users)
        count += tmpCnt
    '''
    
    '''
    params = {'pagesize': 100, 'sort': 'popular'}
    count = 0    
    for i in range(1, 470):
        params['page'] = i
        tags = stackapi.get('tags', params)
        if tags is None:
            break
        tmpCnt = db.insert(tags, DataBase.tags)
        count += tmpCnt
    '''
   
    count = 0
    u_ids = db.select(DataBase.users_get, lambda x: x[0])
    params = {'pagesize': 100, 'sort': 'activity', 'filter': '!FcbKgRDEwU1MPQ78HUmuZzcY8x'}
    #for i in range(1, len(u_ids) + 1):
    i = 1
    while True:
        params['page'] = i
        questions, no_more = stackapi.get('users/%s/questions' % u_ids[0], params)
        tmpCnt = db.insert(questions, DataBase.questions)
        count += tmpCnt
        if no_more:
            break        
        i += 1
        
        
        
    print "Добавлено строк в базу: %s" % count
    print "Время обработки: {:.3f} sec".format(time.time() - start_time)
    
    del stackapi
    del db
    
if __name__ == "__main__":
    main()