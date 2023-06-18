# -*- coding: utf-8 -*-
"""
Created on Mon May 15 22:54:07 2023

@author: Tomasz Konieczka
"""

from colorama import Fore, Back, Style

class DBG:
    DEBUG = True
    
    _ERR  = '[ ERROR ] '
    _WARN = '[ WARN ]  '
    _INFO = '[ INFO ]  '
    _DATA = '[ DATA ]  '

    @staticmethod
    def ERR(s):
        if(DBG.DEBUG==True):
            print(Fore.RED + Style.BRIGHT + DBG._ERR, s)
            print(Style.RESET_ALL, end='')
    
    @staticmethod
    def WARN(s):
        if(DBG.DEBUG==True):
            print(Fore.YELLOW + Style.BRIGHT + DBG._WARN, s)
            print(Style.RESET_ALL, end='')
    
    @staticmethod
    def INFO(s):
        if(DBG.DEBUG==True):
            print(Fore.BLUE + Style.BRIGHT + DBG._INFO, s)
            print(Style.RESET_ALL, end='')
            
    @staticmethod
    def DATA(s, newLine=True):
        if(DBG.DEBUG==True):
            print(Fore.CYAN + Style.BRIGHT + DBG._DATA, s, end='\n' if newLine==True else '')
            print(Style.RESET_ALL, end='')
        
