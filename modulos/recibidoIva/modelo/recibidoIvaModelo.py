#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# recibidoIvaModelo.py
#
# Creado: 20/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.recibidoIva.modelo.recibidoIvaActiveRecord import RecibidoIvaActiveRecord

class RecibidoIvaModelo(RecibidoIvaActiveRecord):
    '''
    Clase para realizar operaciones en la tabla recibidos_iva.
    
    Realiza operaciones varias de consultas sobre la  tabla recididos_iva 
    de la base de datos farma_py, hereda todos los métodos CRUD de la clase 
    RecibidoIvaActiveRecord y los atributos y métodos de la clase 
    RecibidoIvaVO.
    '''

    def find_all_id_recibido(self):
        """
        Obtiene los registros según id de la tabla recibidos.
        
        Obtiene los registros de la tabla según el id de la tabla recibidos.
        @param id_recibido: de RecibidoIvaVO.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM recibidos_iva "
                    "WHERE id_recibido=%s ORDER BY id")
        valor = (self.get_id_recibido())
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
