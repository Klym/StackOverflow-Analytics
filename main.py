# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:00:04 2016

@author: Klym
"""
from db import DataBase
from log import Log
from StackAPI import StackAPI
from datetime import datetime
import time, sys, argparse
reload(sys)
sys.setdefaultencoding('cp866')

def get_tags(stackapi, db, log):
    tags_count = 0
    params = {'pagesize': 100, 'sort': 'popular'}
    page = 1
    tmpCnt = 0
    while True:
        params['page'] = page
        try:
            tags, has_more, backoff = stackapi.get('tags', params)
            if backoff > 0:
                log.write(u"Ожидание: %s сек" % backoff)
                time.sleep(backoff)
                stackapi.connect()
        except Exception as e:
            log.write(e.message)
            break
        tmpCnt = db.insert(tags, DataBase.tags)
        tags_count += tmpCnt
        if not has_more:
            break
        page += 1
    log.write(u"Тэгов добавлено: %s, запросов: %s" % (tags_count, page))
    return tags_count

def get_users(stackapi, db, log, pages_from, pages_count):
    users_count = 0
    params = {'pagesize': 100, 'sort': 'reputation', 'filter': '!BTeL*ManaQamixcFXChIJdmUWwxR(9'}
    for i in range(pages_from, pages_count + 1):
        params['page'] = i
        try:
            users, has_more, backoff = stackapi.get('users', params)
            if backoff > 0:
                log.write(u"Ожидание: %s сек" % backoff)
                time.sleep(backoff)
                stackapi.connect()
        except Exception as e:
            log.write(e.message)
            break
        tmpCnt = db.insert(users, DataBase.users)
        users_count += tmpCnt
        if not has_more:
            break
    log.write(u"Пользователей добавлено: %s" % users_count)
    return users_count
    
def get_questions(stackapi, db, log):
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
                    log.write(u"Ожидание: %s сек" % backoff)
                    time.sleep(backoff)
                    stackapi.connect()
            except Exception as e:
                log.write(e.message)
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
                        if db.show_err:
                            log.write(u"Ошибка связи тэга с вопросом. Question id: %s, tag name: %s. Msg: %s" % (q["question_id"], tag, e.message))

            tmpCnt = db.insert(q_tags, DataBase.q_tags)
            many_tags_count += tmpCnt            
            if not has_more:
                break
            page += 1
        log.write(u"%s: Добавлены вопросы пользователя №%s (%s), запросов: %s" % (i + 1, u_ids[i], questions_count, page))
    return questions_count, many_tags_count

def get_answers(stackapi, db, log):
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
                    log.write(u"Ожидание: %s сек" % backoff)
                    time.sleep(backoff)
                    stackapi.connect()
            except Exception as e:
                log.write(e.message)
                break
            tmpCnt = db.insert(answers, DataBase.answers)
            answers_count += tmpCnt
            if not has_more:
                break
            page += 1
        log.write(u"%s: Добавлены ответы к вопросу №%s (%s), запросов: %s" % (i + 1, q_ids[i], tmpCnt, page))
    return answers_count

def get_comments(stackapi, db, log):
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
                    log.write(u"Ожидание: %s сек" % backoff)
                    time.sleep(backoff)
                    stackapi.connect()
            except Exception as e:
                '''
                is_next = raw_input(u'Повторить попытку(y/n)?\n')
                if is_next == 'y':
                    break
                elif is_next == 'n':
                    exit(0)
                '''
                log.write(e.message)
                break
            tmpCnt = db.insert(comments, DataBase.comments)
            comments_count += tmpCnt
            if not has_more:
                break
            page += 1
        log.write(u"%s: Добавлены комментарии ответа №%s (%s), запросов: %s" % (i + 1, a_ids[i], tmpCnt, page))
    return comments_count

def main():
    parser = argparse.ArgumentParser(description=u"Получение данных ресурса stackoverflow.com")
    parser.add_argument('-u', '--users', type=int, nargs=2, metavar=('from', 'count'), help=u'Получить пользователей ресурса')
    parser.add_argument('-t', '--tags', action='store_true', help=u'Получить все тэги ресурса')
    parser.add_argument('-q', '--questions', nargs='?', metavar='from', help=u'Получить вопросы пользователей после from(user_id)')
    parser.add_argument('-a', '--answers', nargs='?', metavar='from', help=u'Получить ответы к вопросам после from(question_id)')
    parser.add_argument('-c', '--comments', nargs='?', metavar='from', help=u'Получить комментарии к ответам после from(answer_id)')
    parser.add_argument('-l', '--log', type=str, nargs='?', const='out.log', metavar='path', help=u'Создать файл лога')
    args = parser.parse_args()
    
    # Создаем файл лога
    log = Log(args.log)
    
    # Соединяемся с базой и API
    start_time = time.time()
    stackapi = StackAPI()
    db = DataBase()
    rows_count, tags_count, users_count, questions_count, many_tags_count, answers_count, comments_count = 0, 0, 0, 0, 0, 0, 0
    
    log.write(u"Начало загрузки: %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    
    if args.tags:
        # Получаем тэги
        tags_count = get_tags(stackapi, db, log)
        rows_count += tags_count        
    if args.users is not None:
        # Получаем пользователей
        pages_count = args.users[0] if args.users[0] > 0 else 1
        pages = args.users[1] if args.users[1] > 0 else 1
        users_count = get_users(stackapi, db, log, pages_count, pages)
        rows_count += users_count
    if args.questions is not None:
        # Получаем вопросы
        questions_count, many_tags_count = get_questions(stackapi, db, log)
        rows_count += questions_count + many_tags_count
    if args.answers is not None:
        # Получаем ответы
        answers_count = get_answers(stackapi, db, log)
        rows_count += answers_count
    if args.comments is not None:
        # Получаем комментарии
        comments_count = get_comments(stackapi, db, log)
        rows_count += comments_count
    
    log.write(u"\nОшибок базы данных: %s" % DataBase.errors)
    log.write(u"Ошибок получения данных: %s" % StackAPI.errors)
    
    log.write(u"\nПользователей добавлено: %s" % users_count)
    log.write(u"Тэгов добавлено: %s" % tags_count)
    log.write(u"Вопросов добавлено: %s" % questions_count)
    log.write(u"Связано тэгов с вопросами: %s" % many_tags_count)
    log.write(u"Ответов добавлено: %s" % answers_count)
    log.write(u"Комментариев добавлено: %s" % comments_count)
    
    log.write(u"\nДобавлено строк в базу: %s" % rows_count)
    log.write(u"Время обработки: {:.3f} sec".format(time.time() - start_time))
    
    del log
    del stackapi
    del db
    
if __name__ == "__main__":
    main()