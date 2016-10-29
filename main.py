# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:00:04 2016

@author: Klym
"""
from db import DataBase
from StackAPI import StackAPI
import time, sys
reload(sys)
sys.setdefaultencoding('cp866')

def main():
    stackapi = StackAPI()
    db = DataBase()

    start_time = time.time()
    rows_count = 0

    users_count = 0
    '''
    params = {'pagesize': 100, 'sort': 'reputation', 'filter': '!BTeL*ManaQamixcFXChIJdmUWwxR(9'}
    for i in range(1, 2):
        params['page'] = i
        try:
            users, has_more, backoff = stackapi.get('users', params)
            if backoff > 0:
                print "Sleep %s" % backoff
                time.sleep(backoff)
                stackapi.connect()
        except Exception as e:
            print e.message
            break
        tmpCnt = db.insert(users, DataBase.users)
        rows_count += tmpCnt
        users_count += tmpCnt
        if not has_more:
            break
    print "Пользователи добавлены: %s" % users_count
    '''
    tags_count = 0
    '''
    params = {'pagesize': 100, 'sort': 'popular'}
    page = 1
    tmpCnt = 0
    while True:
        params['page'] = page
        try:
            tags, has_more, backoff = stackapi.get('tags', params)
            if backoff > 0:
                print "Sleep %s" % backoff
                time.sleep(backoff)
                stackapi.connect()
        except Exception as e:
            print e.message
            break
        tmpCnt = db.insert(tags, DataBase.tags)
        rows_count += tmpCnt
        tags_count += tmpCnt
        if not has_more:
            break
        page += 1
    print "Тэги добавлены: %s, запросов: %s" % (tags_count, page)
    '''
    
    u_ids = db.select_all(DataBase.users_get, lambda x: x[0])
    
    questions_count = 0
    many_tags_count = 0
    params = {'pagesize': 100, 'sort': 'activity', 'filter': '!FcbKgRDEwU1MPQ78HUmuZzcY8x'}
    tags = {}
    '''
    for i in range(0, len(u_ids)):
        page = 1
        tmpCnt = 0
        while True:
            params['page'] = page
            try:
                questions, has_more, backoff = stackapi.get('users/%s/questions' % u_ids[i], params)
                if backoff > 0:
                    print "Sleep %s" % backoff
                    time.sleep(backoff)
                    stackapi.connect()
            except Exception as e:
                print e.message
                break
            tmpCnt = db.insert(questions, DataBase.questions)
            rows_count += tmpCnt
            questions_count += tmpCnt
            
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
            rows_count += tmpCnt
            many_tags_count += tmpCnt
            
            if not has_more:
                break
            page += 1
        print "%s: Добавлены вопросы пользователя №%s (%s), запросов: %s" % (i + 1, u_ids[i], tmpCnt, page)
    '''
    q_ids = db.select_all(DataBase.questions_get, lambda x: x[0])
    answers_count = 0
    params = {'pagesize': 100, 'sort': 'activity', 'filter': '!1zSsisBYpfc6Z)_I78GqP'}
    '''
    for i in range(0, len(q_ids)):
        page = 1
        tmpCnt = 0
        while True:
            params['page'] = page
            try:
                answers, has_more, backoff = stackapi.get('questions/%s/answers' % q_ids[i], params)
                if backoff > 0:
                    print "Sleep %s" % backoff
                    time.sleep(backoff)
                    stackapi.connect()
            except Exception as e:
                print e.message
                break
            tmpCnt = db.insert(answers, DataBase.answers)
            rows_count += tmpCnt
            answers_count += tmpCnt
            if not has_more:
                break
            page += 1
        print "%s: Добавлены ответы к вопросу №%s (%s), запросов: %s" % (i + 1, q_ids[i], tmpCnt, page)
    '''
    a_ids = db.select_all(DataBase.answers_get, lambda x: x[0])
    comments_count = 0
    params = {'pagesize': 100, 'sort': 'votes', 'filter': '!SWKA(oW8Wg69*y33Fw'}
    end = False
    for i in range(0, len(a_ids)):
        page = 1
        tmpCnt = 0
        while True:
            params['page'] = page
            try:
                comments, has_more, backoff = stackapi.get('answers/%s/comments' % a_ids[i], params)
                if backoff > 0:
                    print "Sleep %s" % backoff
                    time.sleep(backoff)
                    stackapi.connect()
            except Exception as e:
                print e.message
                is_next = raw_input(u'Повторить попытку(y/n)?\n')
                if is_next == 'y':
                    break
                elif is_next == 'n':
                    comments, has_more, end = [], False, True
            tmpCnt = db.insert(comments, DataBase.comments)
            rows_count += tmpCnt
            comments_count += tmpCnt
            if not has_more:
                break
            page += 1
        if end:
            break
        print u"%s: Добавлены комментарии ответа №%s (%s), запросов: %s" % (i + 1, a_ids[i], tmpCnt, page)
    
    print u"\nОшибок базы данных: %s" % DataBase.errors
    print u"Ошибок получения данных: %s" % StackAPI.errors
    
    print u"\nПользователей добавлено: %s" % users_count
    print u"Тэгов добавлено: %s" % tags_count
    print u"Вопросов добавлено: %s" % questions_count
    print u"Связано тэгов с вопросами: %s" % many_tags_count
    print u"Ответов добавлено: %s" % answers_count
    print u"Комментариев добавлено: %s" % comments_count
    
    print u"\nДобавлено строк в базу: %s" % rows_count
    print u"Время обработки: {:.3f} sec".format(time.time() - start_time)
    
    del stackapi
    del db
    
if __name__ == "__main__":
    main()