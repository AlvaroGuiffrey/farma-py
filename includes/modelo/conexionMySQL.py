# -*- coding: utf-8 -*-
#
# conexionMySQL.py
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de terceros:
import mysql.connector
from mysql.connector import errorcode

class ConexionMySQL:

    def __init__(self):
        self.user = 'root'
        self.password = ''
        self.host = '127.0.0.1'
        self.database = 'farma'
        self.ccnx = None

    def conectar(self):
        if self.ccnx == None:
            try:
                self.ccnx = mysql.connector.connect(user=self.user,
                                       password=self.password,
                                       host=self.host,
                                       database=self.database)

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
            else:
                return self.ccnx

    def desconectar(self):
        self.ccnx.close()
