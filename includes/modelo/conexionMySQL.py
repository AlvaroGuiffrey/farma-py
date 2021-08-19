# -*- coding: utf-8 -*-
# 
# conexionMySQL.py
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de terceros:
import mysql.connector
    

class ConexionMySQL:
    
    def __init__(self):
        self.user = 'root'
        self.password = ''
        self.host = '127.0.0.1'
        self.database = 'farma'
        self.ccnx = None
        
    def conectar(self):
        if self.ccnx == None:
            self.ccnx = mysql.connector.connect(user=self.user,
                                       password=self.password, 
                                       host=self.host,
                                       database=self.database)        
        
        return self.ccnx
   
    def desconectar(self):
        self.ccnx.close()  
                              
