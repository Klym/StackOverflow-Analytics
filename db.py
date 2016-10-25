# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:30:54 2016

@author: Klym
"""
import pyodbc, datetime

class DataBase(object):
    
    def __init__(self):
        connection_str = 'DRIVER={ODBC Driver 13 for SQL Server};Server=localhost\SQLEXPRESS;Database=stackoverflow;Trusted_Connection=Yes;'
        with pyodbc.connect(connection_str) as self.cnxn:
            self.cursor = self.cnxn.cursor()            

    def __del__(self):
        self.cursor.close()
        self.cnxn.close()
    
    def select(self, func, proc_fn):
        sql_select_stmt = func()
        try:
            self.cursor.execute(sql_select_stmt)
            rows = self.cursor.fetchall()
            return map(proc_fn, rows)
        except pyodbc.DatabaseError as err:
            print err.args[1].decode("cp1251")
        return None
    
    def insert(self, data, func):
        count = 0
        for i in range(0, len(data)):
            sql_insert_stmt, fields = func(data, i)
            try:
                self.cursor.execute(sql_insert_stmt, fields)
                self.cursor.commit()
            except pyodbc.DatabaseError as err:
                print i, err.args[1].decode("cp1251")
                count += 1
        return len(data) - count
    
    @staticmethod
    def users(data, i):
        isEmployee = 1 if data[i]["is_employee"] else 0
        age = data[i].get("age")
        location = data[i].get("location")
        date = datetime.datetime.fromtimestamp(int(data[i]["creation_date"]))
        return ("insert into [dbo].[users] ([id], [user_type], [display_name], [age], [location], [reputation], [is_employe], [creation_date], [view_count], [question_count], [answer_count]) values (?,?,?,?,?,?,?,?,?,?,?)", (data[i]["user_id"], data[i]["user_type"], data[i]["display_name"], age, location, data[i]["reputation"], isEmployee, date, data[i]["view_count"], data[i]["question_count"], data[i]["answer_count"]))
    
    @staticmethod
    def users_get():
        return "select [id] from [dbo].[users]"
    
    @staticmethod
    def users_proc(row):
        return row[0]
        
    @staticmethod
    def tags(data, i):
        has_synonyms = 1 if data[i]["has_synonyms"] else 0
        return ("insert into [dbo].[tags] ([name], [count], [has_synonyms]) values (?,?,?)", (data[i]["name"], data[i]["count"], has_synonyms))