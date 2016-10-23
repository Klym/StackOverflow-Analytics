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
    
    def insertUsers(self, data):
        for i in range(0, len(data)):
            isEmployee = 1 if data[i]["is_employee"] else 0
            age = data[i].get("age")
            location = data[i].get("location")
            creation_date = datetime.datetime.fromtimestamp(int(data[i]["creation_date"]))
            date = creation_date.strftime("%y-%m-%d")
            try:
                self.cursor.execute("insert into [dbo].[users] ([id], [user_type], [display_name], [age], [location], [reputation], [is_employe], [creation_date], [view_count], [question_count], [answer_count]) values (?,?,?,?,?,?,?,?,?,?,?)", data[i]["user_id"], data[i]["user_type"], data[i]["display_name"], age, location, data[i]["reputation"], isEmployee, date, data[i]["view_count"], data[i]["question_count"], data[i]["answer_count"])
                self.cursor.commit()
            except pyodbc.DatabaseError as err:
                print i, err.args[1].decode("cp1251")