#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# afipComprobanteActiveRecord.py
#
# Creado: 05/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.afip.modelo.afipComprobanteVO import AfipComprobanteVO


class AfipComprobanteActiveRecord(AfipComprobanteVO):
    '''
    Clase que implementa el patrón Active Record en la tabla afip_comprobantes.
    
    Permite realizar operaciones del tipo CRUD sobre la tabla afip_comprobantes
    de la base de datos farma en mysql. Hereda los atributos y métodos de la 
    clase AfipComprobanteVO. 
    La conexión a la base de datos se realiza por una instancia de la clase 
    ConexionMySQL.
    '''

    
    # Atributos de la instancia:
    def __init__(self):
        """ 
        Iniciliza los atributos necesarios.
        """
        self.cantidad = int(0)
        
    # Métodos:
    def find(self):
        """
        Obtiene un renglón de la tabla.
        
        @param codigo: índice de la tabla. 
        @return: AfipComprobanteVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """ 
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM afip_comprobantes WHERE codigo = %s")
        cursor.execute(consulta, (self.get_codigo(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        if self.cantidad == 1:
            self.set_codigo(dato[0])
            self.set_descripcion(dato[1])
            self.set_alias(dato[2])
            self.set_letra(dato[3])
            return dato
        else:
            return None
        
    def find_all(self):
        """
        Obtiene todos los renglones de la tabla.
        
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM afip_comprobantes")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
        
    def count(self):
        """
        Obtiene la cantidad de registros de la tabla.
        
        @return: se accede al valor por el metodo get_cantidad().
        """    
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT COUNT(*) FROM afip_comprobantes")
        cursor.execute(consulta)
        dato = cursor.fetchone()
        self.cantidad = dato[0]
        cursor.close()
        ccnx.close()        
    
    def get_cantidad(self):
        """ 
        Método para retornar la cantidad de registros.
        
        @return: se accede al valor de la cantidad de registros afectados de
                la última operación realizada en la tabla.
        """
        return self.cantidad
    