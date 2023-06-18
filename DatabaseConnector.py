# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:04:54 2023

@author: Tomasz Konieczka
"""


from DBG import DBG
import pyodbc 

class DatabaseConnector:
    
    def __init__(self, server, database, username, passwd=''):
        self.isConnected = False
        
        self.server   = server
        self.database = database
        self.username = username
        self.passwd   = passwd
        
        self.cnxn = None
        
        # try create conection
        if(not passwd):
            self.encrypt = 'no'
            try:
                self.cnxn     = \
                pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT='+self.encrypt+';UID='+username+'; Trusted_Connection=yes;')
                self.isConnected = True
            except Exception as e:
                DBG.ERR("Error during conection to DB: " + str(e))
                return
        else:
            self.encrypt = 'yes'
            try:
                self.cnxn     = \
                    pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT='+self.encrypt+';UID='+username+';PWD='+self.passwd)
                self.isConnected = True
            except Exception as e:
                DBG.ERR("Error during conection to DB: " + str(e))
                return
                
        self.cursor = self.cnxn.cursor()
        
        if self.isConnected:
            DBG.INFO('Connected to database: ' + self.database + ' -- OK')
            
        
    def __del__(self):
        if(self.cnxn != None):
            DBG.INFO('Connection has been closed...')
            self.cnxn.close()