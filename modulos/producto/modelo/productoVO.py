#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# productoActiveRecord.py
#
# Creado: 08/08/2019
# Versi�n: 001
# �ltima modificaci�n: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos que se importan de la libreria standar
from datetime import datetime
from builtins import int

# Modulos que se importan

class ProductoVO:
    
    # Atributos de clase
    
    # Atributos de instancia
    def __init__(self):
        self.id_db = int(0)
        self.id_proveedor = int(0)
        self.codigo_b = int(0)
        self.codigo_p = str('')
        self.nombre = str('')
        self.precio = float(0.00)
        self.estado = int(0)
        self.id_articulo = int(0)
        self.id_usuario_act = int(0)
        self.fecha_act = datetime.now()
            
    # Métodos
    def get_id(self):
        return self.id_db
    
    def get_nombre(self):
        return self.nombre
        
 
    def set_id(self, id_db):
        self.id_db = id_db
    
    def set_nombre(self, nombre):
        self.nombre = nombre
        
  
            
            