# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:00:04 2016

@author: Klym
"""
from db import DataBase
from StackAPI import StackAPI
from datetime import datetime
import time, sys, argparse
reload(sys)
sys.setdefaultencoding('cp866')

def get_tags(stackapi, db):
    tags_count = 0
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
        tags_count += tmpCnt
        if not has_more:
            break
        page += 1
    print u"Тэги добавлены: %s, запросов: %s" % (tags_count, page)
    return tags_count

def get_users(stackapi, db, pages_count):
    users_count = 0
    params = {'pagesize': 100, 'sort': 'reputation', 'filter': '!BTeL*ManaQamixcFXChIJdmUWwxR(9'}
    for i in range(1, pages_count + 1):
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
        users_count += tmpCnt
        if not has_more:
            break
    print u"Пользователи добавлены: %s" % users_count
    return users_count
    
def get_questions(stackapi, db):
    u_ids = db.select_all(DataBase.users_get, lambda x: x[0])
    params = {'pagesize': 100, 'sort': 'activity', 'filter': '!FcbKgRDEwU1MPQ78HUmuZzcY8x'}
    tags = {}
    questions_count, many_tags_count = 0, 0
    
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
            many_tags_count += tmpCnt            
            if not has_more:
                break
            page += 1
        print u"%s: Добавлены вопросы пользователя №%s (%s), запросов: %s" % (i + 1, u_ids[i], questions_count, page)
    return questions_count, many_tags_count

def get_answers(stackapi, db):
    q_ids = db.select_all(DataBase.questions_get, lambda x: x[0])
    params = {'pagesize': 100, 'sort': 'activity', 'filter': '!1zSsisBYpfc6Z)_I78GqP'}
    answers_count = 0
        
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
            answers_count += tmpCnt
            if not has_more:
                break
            page += 1
        print u"%s: Добавлены ответы к вопросу №%s (%s), запросов: %s" % (i + 1, q_ids[i], tmpCnt, page)
    return answers_count

def get_comments(stackapi, db):
    a_ids = db.select_all(DataBase.answers_get, lambda x: x[0])
    params = {'pagesize': 100, 'sort': 'votes', 'filter': '!SWKA(oW8Wg69*y33Fw'}
    comments_count = 0
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
            except Exception:
                is_next = raw_input(u'Повторить попытку(y/n)?\n')
                if is_next == 'y':
                    break
                elif is_next == 'n':
                    exit(0)
            tmpCnt = db.insert(comments, DataBase.comments)
            comments_count += tmpCnt
            if not has_more:
                break
            page += 1
        print u"%s: Добавлены комментарии ответа №%s (%s), запросов: %s" % (i + 1, a_ids[i], tmpCnt, page)
    return comments_count

def main():
    parser = argparse.ArgumentParser(description=u"Получение данных ресурса stackoverflow.com")
    parser.add_argument('-u', '--users', type=int, help=u'Получить U страниц пользователей(U * 100)')
    parser.add_argument('-t', '--tags', action='store_true', help=u'Получить все тэги ресурса')
    parser.add_argument('-e', '--errors', action='store_true', help=u'Включить вывод ошибок')
    parser.add_argument('-l', '--log', action='store_true', help=u'Создать файл лога')
    args = parser.parse_args()
    
    start_time = time.time()
    stackapi = StackAPI()
    db = DataBase()
    rows_count, tags_count, users_count, questions_count, many_tags_count, answers_count, comments_count = 0, 0, 0, 0, 0, 0, 0
    
    print u"Начало загрузки: %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    # Получаем тэги
    if args.tags:
        tags_count = get_tags(stackapi, db)
        rows_count += tags_count
        
    if args.users is not None:
        # Получаем пользователей
        pages = args.users if args.users > 0 else 1
        users_count = get_users(stackapi, db, pages)
        rows_count += users_count
        # Получаем вопросы
        questions_count, many_tags_count = get_questions(stackapi, db)
        rows_count += questions_count + many_tags_count
        # Получаем ответы
        answers_count = get_answers(stackapi, db)
        rows_count += answers_count
        # Получаем комментарии
        comments_count = get_answers(stackapi, db)    
    
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