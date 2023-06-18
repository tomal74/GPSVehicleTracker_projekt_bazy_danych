# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:06:08 2023

@author: Tomasz Konieczka
"""

import pyodbc
from DBG import DBG

from DRIVER_TAB import DRIVER as dt

class DB_Manager:
    
    def __init__(self, DB_cursor):
        self.DB_cursor = DB_cursor
        self.unsavedChanges = False
        
    
    def printAll(self, table):
        rows =  self.DB_cursor.execute("SELECT * FROM " + table).fetchall() #fetchall wywswietli wszystkie kolumny -- fetchone jedna
        for row in rows:
            print(row)
            
        return rows
          
            
    def addDriver(self, first_name, surname, driverID):
        self.DB_cursor.execute(f"""  
                  INSERT INTO {dt.DRIVER_TABLE}({dt.DRIVER_TABLE_d['first_name']}, {dt.DRIVER_TABLE_d['surname']}, {dt.DRIVER_TABLE_d['driver_id']}, {dt.DRIVER_TABLE_d['driving_rating']})
                  VALUES( '{first_name}', '{surname}', {driverID}, {dt.driving_rating_MAX} )
                  """)
                  
        self.unsavedChanges = True  
        DBG.WARN(f'There are unsaved changes in {dt.DRIVER_TABLE}')
        
        
    def saveChanges(self):
        if(self.unsavedChanges == False):
            DBG.WARN('Nothing to save!')
            return
        
        self.DB_cursor.commit()
        self.unsavedChanges = False
        
        DBG.INFO('Changes have been saved successfully')
     
        
    def showAllTrips(self):
        self.printAll('dbo.Trips')
        
        
    # def addTrip(self):
    #     self.DB_cursor.execute("""
    #                            CREATE TABLE dbo.Trip1 (
    #                                TrasaID INT IDENTITY(1,1) PRIMARY KEY,
    #                                Pozycja GEOGRAPHY)
    #                            """)
    #     self.unsavedChanges = True 
    
    
    def addTrip(self, driver_id, car_vin, gpx_path):
        self.DB_cursor.execute(f"""  
                  INSERT INTO dbo.Trips
                  VALUES( {driver_id}, '{car_vin}', '{gpx_path}' )
                  """)        
                       
        self.unsavedChanges = True 
        
    def showAllCars(self):
        self.printAll('dbo.Cars')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        