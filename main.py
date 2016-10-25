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

    u_ids = db.select_all(DataBase.users_get, lambda x: x[0])
    '''
    count = 0
    params = {'pagesize': 100, 'sort': 'activity', 'filter': '!FcbKgRDEwU1MPQ78HUmuZzcY8x'}
    
    tags = {}
    
    for i in range(0, len(u_ids)):
        page = 1        
        while True:
            params['page'] = page
            try:
                questions, has_more = stackapi.get('users/%s/questions' % u_ids[i], params)
            except Exception as e:
                print e.message
                continue
            tmpCnt = db.insert(questions, DataBase.questions)
            count += tmpCnt
    
            # Готовим словарь тэгов
            q_tags = []
            for q in questions:
                for tag in q["tags"]:
                    tag_id = tags.get(tag)
                    try:
                        if tag_id is None:
                            tag_id = tags[tag] = db.select(DataBase.get_tag_id, lambda x: x[0], tag)
                        q_tags.append({"question_id": q["question_id"], "tag_id": tag_id})
                    except Exception as e:
                        print "Error while inserting tags. Question id: %s, tag name: %s. Msg: %s" % (q["question_id"], tag, e.message)
                                                
            tmpCnt = db.insert(q_tags, DataBase.q_tags)
            count += tmpCnt
    
            if not has_more:
                break
            page += 1
        print "%s: Обработан пользователь № %s" % (i + 1, u_ids[i])
    '''
    count = 0
    params = {'pagesize': 100, 'sort': 'activity', 'filter': '!1zSsisBYpfc6Z)_I78GqP'}

    for i in range(0, len(u_ids)):
        page = 1        
        while True:
            params['page'] = page
            try:
                answers, has_more = stackapi.get('users/%s/answers' % u_ids[i], params)
            except Exception:
                break
            tmpCnt = db.insert(answers, DataBase.answers)
            count += tmpCnt
            if not has_more:
                break
            page += 1
        print "%s: Обработан пользователь № %s" % (i + 1, u_ids[i])
   
    print "Добавлено строк в базу: %s" % count
    print "Время обработки: {:.3f} sec".format(time.time() - start_time)
    
    del stackapi
    del db
    
if __name__ == "__main__":
    main()