#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# afipComprobanteModelo.py
#
# Creado: 05/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.afip.modelo.afipComprobanteActiveRecord import AfipComprobanteActiveRecord

class AfipComprobanteModelo(AfipComprobanteActiveRecord):
    """
    Clase para realizar operaciones en la tabla afip_comprobantes.
    
    Realiza operaciones varias de consultas sobre la  tabla afip_comprobantes 
    de la base de datos farma_py, hereda todos los métodos CRUD de la clase 
    AfipComprobanteActiveRecord y los atributos y métodos de la clase 
    AfipComprobanteVO.
    """
    
    def find_all_select(self):
        """
        Obtiene los datos para armar un select para la vista.
        
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT codigo, descripcion FROM afip_comprobantes "
                    "ORDER BY descripcion")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    