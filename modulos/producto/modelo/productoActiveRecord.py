#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# productoActiveRecord.py
#
# Creado: 08/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos que se importan de la aplicación
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.producto.modelo.productoVO import ProductoVO

class ProductoActiveRecord(ProductoVO):
    
    
    # Atributos de la instancia:
    def __init__(self):
        """ 
        Método que iniciliza los atributos necesarios
        """
        self.cantidad = int(0)
    
    # Metodos:               
    def find(self):
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM productos WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
        dato = cursor.fetchone()
        cantidad = cursor.rowcount
        cursor.close()
        if cantidad == 1:         
            self.set_id(dato[0])
            self.set_nombre(dato[4])
            return dato
        else:
            return None
        
    def count(self):
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT COUNT(*) FROM productos")
        cursor.execute(consulta)
        dato = cursor.fetchone()
        self.cantidad = dato[0]        
    
    def get_cantidad(self):
        """ 
        Método para retornar la cantidad de renglones afectados
        """
        return self.cantidad