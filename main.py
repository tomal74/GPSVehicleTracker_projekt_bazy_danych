# -*- coding: utf-8 -*-
"""
Created on Wed May 10 12:03:43 2023

@author: Tomasz Konieczka

Poznan University of Technology

Przemysłowe Systemy Baz Danych (projekt)

"""

# /backend/gpxstudio/CARS

from DBG import DBG
from DRIVER_TAB import DRIVER as dt
from DRIVER_TAB import DBO
from DRIVER_TAB import TRIP
from DatabaseConnector import DatabaseConnector
from DB_Manager import DB_Manager    

import winsound
import time
import random

import socket
import select
import multiprocessing

DBG.DEBUG = False  


PORT = 5557
#PORT = 8887
HOST = "127.0.0.1"

ROOT_PATH = 'backend/gpxstudio/CARS/'
GPXSTUDIO_ROOT = 'CARS/'

#kamil host
#HOST = "192.168.1.23"

class TCPclient:
    def __init__(self, port, host, maxConnectRetryNo):
        # get the hostname
        self.host = host # socket.gethostname()
        self.port = port # initiate port no above 1024
        self.client_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.connected = False
        self.connectionRetryCnt = 0
        self.maxConnectRetryNo = maxConnectRetryNo
        self.data = []
       
        #self.client_socket.settimeout(10.0)
        self.connect()
        
    def connect(self):
        while(self.connectionRetryCnt < self.maxConnectRetryNo):
            try:
                self.connectionRetryCnt += 1
                self.client_socket.connect((self.host, self.port))  # connect to the server
                self.connectionRetryCnt = 0
                if( self.client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0):
                    self.connected = True
                return
            except Exception as e:
                DBG.ERR("Error TCP during TCP connection attempt: " + str(e))
                
    def disconnect(self):
        self.client_socket.close()  
        self.connected = False
        
    def recData(self):

        if(self.connected == False):
            DBG.WARN("Socket not connected!, try to reconnect")
            return  b''
        
        try:
            self.data = self.client_socket.recv(4096)
            #self._TCPbuff += self.data

            # jezeli polaczenie zostalo zamkniete przez serwer, to recv, przestaje blokowac i zwraca 
            # puste dane - tak sprawdzamy czy polaczenie jest otwarte, natomiast settimeout() sprawdza
            # czy dane przylatuja (tzn. polaczenie jest otwarte ale nie leca dane)
            if(not self.data):
                self.connected = False   
                self.disconnect()
                self.data = b''
                DBG.ERR("The server has closed the connection")
        except (OSError, socket.timeout):
            DBG.ERR("Timeout or OSError - The server is not responding")
            self.connected = False
            self.disconnect()
                
        return self.data



from pynmeagps import NMEAReader

import gpxpy
import gpxpy.gpx
import datetime



class NMEA2GPX(TCPclient):
    GPX_BUFF_LEN = 1024 * 1024
    
    
    def __init__(self, port, host, maxConnectRetryNo, driver, car):
        super().__init__(port, host, maxConnectRetryNo)
        
        self.GPStime = datetime.time()
        self.ZDAtime = datetime.datetime(2023, 5, 26)
        
        self.lat = None
        self.lon = None
        self.EW = None
        self.NS = None
        self.alt = None
        self.quality = None
        self.speed_over_ground_kph = None
        self.TMG_true_north = None
        
        self.GGAcnt = 0
        self.VTGcnt = 0 
        self.ZDAcnt = 0
        self.isGGA = False
        self.isVTG = False
        self.isZDA = False
        
        self.gpx_str = ''
        
        self.gpx = None
        self.gpx_segment = None
        self.gpx_segment = None
        
        self.driver = driver
        self.car = car
        self.gpx_path = ''
        self.gpxstudio_path = '' 
    
    def nmea2gpx(self, parsed_data): 
        
        if(self.GGAcnt == 0):
            self.gpx = gpxpy.gpx.GPX()
            # Create first track in our GPX:
            self.gpx_track = gpxpy.gpx.GPXTrack()
            self.gpx.tracks.append(self.gpx_track)
            # Create first segment in our GPX track:
            self.gpx_segment = gpxpy.gpx.GPXTrackSegment()
            self.gpx_track.segments.append(self.gpx_segment)
        elif((self.GGAcnt > 0) and (self.VTGcnt > 0) and (self.isVTG == True) and (self.isGGA == True) and (self.ZDAcnt > 2)):
            self.isVTG = False
            self.isGGA = False
            self.isZDA = False
            # Create points:
            self.gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(self.lat, self.lon, elevation=self.alt, time=self.ZDAtime, speed=self.speed_over_ground_kph))
            
            gpx_len = len(self.gpx.to_xml())
            self.gpx_str = self.gpx.to_xml()
            if( gpx_len >  NMEA2GPX.GPX_BUFF_LEN ):
              # FIXME: sprawdzenieu dlugosci
                pass
            else:
                DBG.INFO( self.gpx.to_xml() )
            #winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
            
        # parse data from NMEA stream
        self.takeGPSdata(parsed_data)
            
        
    def takeGPSdata(self, parsed_data):
        if(parsed_data.msgID == 'GGA'):         # GGA
            self.GGAcnt += 1
            self.isGGA = True
            
            self.GPStime : datetime.time = parsed_data.time
            self.ZDAtime.replace(hour=self.GPStime.hour, minute=self.GPStime.minute, second=self.GPStime.second) 
            
            self.lat = round(parsed_data.lat, 5)
            self.lon = round(parsed_data.lon, 5)
            self.alt = parsed_data.alt
            self.quality = parsed_data.quality
            self.EW = parsed_data.EW
            self.NS = parsed_data.NS     
            
        elif(parsed_data.msgID == 'VTG'):       # VTG
            self.VTGcnt += 1
            self.isVTG = True
            
            self.speed_over_ground_kph = parsed_data.sogk
            self.TMG_true_north = parsed_data.cogt
            
        elif(parsed_data.msgID == 'ZDA'):       # ZDA 
            self.ZDAcnt += 1
            self.isZDA = True
            
            # datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])
            self.ZDAtime  = datetime.datetime(parsed_data.year, parsed_data.month, parsed_data.day, parsed_data.time.hour, \
                                              parsed_data.time.minute, parsed_data.time.second)          


    def saveGPXfile(self, file_name):
        # Otwarcie pliku w trybie dopisywania, jeśli plik nie istnieje to zostanie utworzony
        with open(file_name + '.gpx', "a+") as file:
            # Ustawienie wskaźnika na początku pliku
            file.seek(0)
            # Sprawdzenie, czy plik jest pusty
            is_empty = len(file.read()) == 0
            # Jeżeli plik jest pusty, to zapisz dane na początku pliku
            if is_empty:
                file.write(self.gpx_str)
            # W przeciwnym razie dodaj nową linię i dopisz dane na końcu pliku
            else:
                file.write("\n" + self.gpx_str)

            DBG.INFO('GPX file has been saved')       
            
    def main_loop(self, filename : str):    
        NMEAbuff = []
        
        while(True):
           # print('Hello from the child process', flush=True)
            data = self.recData()
            
            if(self.connected == False):
                break
            
            NMEAbuff = str.split(data.decode())
            for frame in NMEAbuff:
                parsed_data = NMEAReader.parse(frame)
                self.nmea2gpx(parsed_data)
         
        self.saveGPXfile(filename)
        print('end')
        
    def gpx_timeName(self):
        now = datetime.datetime.now()
        return now.strftime("%m%d%Y%H%M")
        
    def runMain(self):
        temp_path = self.car[DBO.PLATE] + '_' + self.gpx_timeName()
        
        self.gpxstudio_path = GPXSTUDIO_ROOT + temp_path + '.gpx'
        self.gpx_path = ROOT_PATH + temp_path 
        self.t1 = multiprocessing.Process(target=self.main_loop, args=(self.gpx_path,))
        if(self.connected == False):
            return -1
        print('listening GNSS device')
        self.t1.start()
        return 0
        
    def runMain2(self):
        self.t1 = multiprocessing.Process(target=self.main_loop, args=('car22',))
        self.t1.start()
        
                


if __name__ == '__main__':
    
    DBhandler = DatabaseConnector('localhost\sqlexpress', 'TSQL', 'MSI/tomal')
    db = DB_Manager(DBhandler.cursor)

    #db.addDriver('Jarosław', 'Gaca', 'NULL')
    dbo_drivers = db.printAll(dt.DRIVER_TABLE)
    dbo_cars = db.printAll('dbo.Cars')
    
    while(True):
        print('START...')
        rnd_car_no = random.randint(0, len(dbo_cars)-1)
        rnd_driver_no = random.randint(0, len(dbo_drivers)-1) 
        
        rnd_car = dbo_cars[rnd_car_no]
        rnd_driver = dbo_drivers[rnd_driver_no]
        
        print(rnd_car)
        print(rnd_driver)
        
        #db.addTrip()
        #run_server()
        nmr = NMEA2GPX(PORT, HOST, 3, rnd_driver, rnd_car)
        nmr.runMain()
        
        #nmr2 = NMEA2GPX(PORT+1, HOST, 3)
        #nmr2.runMain2()
        
        if(nmr.t1.is_alive() == True):
            nmr.t1.join()
            
            db.addTrip(nmr.driver[DBO.ID], nmr.car[DBO.ID], nmr.gpxstudio_path)
            db.saveChanges()
        time.sleep(2)

    
        # po zakonczeniu polaczenia zapisz plik .gpx 
        # (zapis nastapi takze po przekroczeniu wielkosci bufora - patrz wew klasy)    
    
    
    
    db.saveChanges()
    #DBhandler.cursor.commit()    
    del DBhandler
    
    
    
    
    
    
    
    
    
    
    
    
    