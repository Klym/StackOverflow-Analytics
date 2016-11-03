# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 00:12:28 2016

@author: Klym
"""

class Log(object):
    
    def __init__(self, path):
        self.file = None
        if path is not None:
            try:
                self.file = open(path, 'w')
            except:       
                print u"Не удается создать файл лога: %s" % path
                
    def write(self, line):
        print line
        if self.file is not None and not self.file.closed:
            self.file.write(line.encode('cp1251') + '\n')
        
    def __del__(self):
        if self.file is not None and not self.file.closed:
            self.file.close()