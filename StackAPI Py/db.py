# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:30:54 2016

@author: Klym
"""
import pyodbc, datetime

class DataBase(object):
    
    errors = 0    
    
    def __init__(self):
        connection_str = 'DRIVER={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Database=stackoverflow;Trusted_Connection=Yes;'
        try:
            with pyodbc.connect(connection_str) as self.cnxn:
                self.cursor = self.cnxn.cursor()
        except pyodbc.Error as err:
            print err.args[1].decode("cp1251")
            raise SystemExit(1)

    def __del__(self):
        if hasattr(DataBase, "cursor"):
            self.cursor.close()
            self.cnxn.close()
    
    def select(self, func, proc_fn, params = None):
        sql_select_stmt = func()
        try:
            self.cursor.execute(sql_select_stmt, params)
            row = self.cursor.fetchone()
            if not row:
                raise Exception("No results in database")
            return proc_fn(row)
        except pyodbc.DatabaseError as err:
            pass
            #print err.args[1].decode("cp1251")
        return None
    
    def select_all(self, func, proc_fn):
        try:            
            self.cursor.execute(func())
            rows = self.cursor.fetchall()
            return map(proc_fn, rows)
        except Exception as err:
            pass
            #print err.args[1].decode("cp1251")
        return None
    
    def insert(self, data, func):
        count = 0
        for i in range(0, len(data)):
            sql_insert_stmt, fields = func(data[i])
            try:
                self.cursor.execute(sql_insert_stmt, fields)
                self.cursor.commit()
            except pyodbc.DatabaseError as err:
                #print err.args[1].decode("cp1251")
                DataBase.errors += 1
                count += 1
        return len(data) - count
    
    @staticmethod
    def users(row):
        is_employee = 1 if row["is_employee"] else 0
        age = row.get("age")
        location = row.get("location")
        date = datetime.datetime.fromtimestamp(int(row["creation_date"]))
        return ("insert into [dbo].[users] ([id], [user_type], [display_name], [age], [location], [reputation], [is_employe], [creation_date], [view_count], [question_count], [answer_count]) values (?,?,?,?,?,?,?,?,?,?,?)", (row["user_id"], row["user_type"], row["display_name"], age, location, row["reputation"], is_employee, date, row["view_count"], row["question_count"], row["answer_count"]))
    
    @staticmethod
    def users_get():
        return "select [id] from [dbo].[users] where (select count(*) from [dbo].[questions] where [user_id] = [users].[id]) = 0 and [question_count] != 0"
    
    @staticmethod
    def tags(row):
        has_synonyms = 1 if row["has_synonyms"] else 0
        return ("insert into [dbo].[tags] ([name], [count], [has_synonyms]) values (?,?,?)", (row["name"], row["count"], has_synonyms))
        
    @staticmethod
    def get_tag_id():
        return "select [id] from [dbo].[tags] where name = ?"
    
    @staticmethod
    def q_tags(row):
        return ("insert into [dbo].[q_tags] ([question_id], [tag_id]) values (?,?)", (row["question_id"], row["tag_id"]))
    
    @staticmethod
    def questions(row):
        user_id = row["owner"]["user_id"]
        is_answered = 1 if row["is_answered"] else 0
        date = datetime.datetime.fromtimestamp(int(row["creation_date"]))
        return ("insert into [dbo].[questions] ([id], [user_id], [title], [body], [is_answered], [view_count], [answer_count], [score], [up_vote_count], [creation_date]) values (?,?,?,?,?,?,?,?,?,?)", (row["question_id"], user_id, row["title"], row["body"], is_answered, row["view_count"], row["answer_count"], row["score"], row["up_vote_count"], date))
    
    @staticmethod
    def questions_get():
        return "select [id] from [dbo].[questions] where (select count(*) from [dbo].[answers] where [question_id] = [questions].[id]) = 0 and [answer_count] != 0"
    
    @staticmethod
    def answers(row):
        user_id = row["owner"].get("user_id", 0)
        is_accepted = 1 if row["is_accepted"] else 0
        date = datetime.datetime.fromtimestamp(int(row["creation_date"]))
        return ("insert into [dbo].[answers] ([id], [user_id], [question_id], [is_accepted], [body], [score], [up_vote_count], creation_date) values (?,?,?,?,?,?,?,?)", (row["answer_id"], user_id, row["question_id"], is_accepted, row["body"], row["score"], row["up_vote_count"], date))
    
    @staticmethod
    def answers_get():
        return "select [id] from [dbo].[answers] where (select count(*) from [dbo].[comments] where [answer_id] = [answers].[id]) = 0"
    
    @staticmethod
    def comments(row):
        user_id = row["owner"].get("user_id", 0)
        date = datetime.datetime.fromtimestamp(int(row["creation_date"]))
        answer_id = None if row["post_type"] == "question" else row["post_id"]
        question_id = None if row["post_type"] == "answer" else row["post_id"]
        edited = 1 if row["edited"] else 0
        return ("insert into [dbo].[comments] ([id], [user_id], [answer_id], [question_id], [body], [score], [edited], [creation_date]) values (?,?,?,?,?,?,?,?)", (row["comment_id"], user_id, answer_id, question_id, row["body"], row["score"], edited, date))