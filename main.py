# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:00:04 2016

@author: Klym
"""
from db import DataBase
from StackAPI import StackAPI

def main():
    stackapi = StackAPI()
    db = DataBase()
    
    for i in range(1, 100):
        users = stackapi.getUsers(i, 100)
        if users is None:
            break
        db.insertUsers(users)
    
    del stackapi
    del db
    
if __name__ == "__main__":
    main()