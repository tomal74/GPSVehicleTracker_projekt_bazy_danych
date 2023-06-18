# -*- coding: utf-8 -*-
"""
Created on Wed May 17 00:42:08 2023

@author: Tomasz Konieczka
"""

class DRIVER: 
    DRIVER_TABLE = 'dbo.Driver'
    
    DRIVER_TABLE_d = {'first_name' : 'first_name', 'surname' : 'surname', 'driver_id' : 'driver_id', 'offense_cnt' : 'offense_cnt', \
                  'total_driving_time' : 'total_driving_time', 'driving_rating' : 'driving_rating'}
        
    driving_rating_MAX = 9.0

class DBO:
    #cars
    ID = 0
    BRAND = 1
    PLATE = 2
    VIN = 3
    YOP = 4
    TDT = 5
    MILAGE = 6
    

class TRIP:
    ID = 0
    DRIVER_ID = 1
    CAR_ID = 2
    GPX = 3