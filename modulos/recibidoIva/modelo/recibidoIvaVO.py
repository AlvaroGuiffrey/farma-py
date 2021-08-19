#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# recibidoIvaVO.py
#
# Creado: 20/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la librería estandar:
from builtins import int

class RecibidoIvaVO(object):
    """ 
    Clase que implementa el patrón Value Object para la tabla.
    
    Realiza un mapeo de los atributos de la tabla recibidos de la 
    base de datos farma en mysql, mediante la implememtación de métodos 
    get y set para interactuar con los controladores y las vistas.
    """
 
    # Atributos de instancia
    def __init__(self):
        """
        Método que inicializa los atributos de la instancia para mapear las
        columnas de la tabla recibidos
        """
        self.id_db = int(0)
        self.id_recibido = int(0)
        self.condicion = int(0)
        self.neto = float(0.00)
        self.iva = float(0.00)
        self.estado = int(0)
        self.id_usuario_act = int(0)
        self.fecha_act = '0000-00-00 00:00:00'
        
    # Métodos 
    """ 
    Métodos que nos permiten retornar el valor de los atributos para 
    interactuar utilizando el patrón MVC.
    """ 
    def get_id(self):
        return self.id_db
    
    def get_id_recibido(self):
        return self.id_recibido
    
    def get_condicion(self):
        return self.condicion
    
    def get_neto(self):
        return self.neto
    
    def get_iva(self):
        return self.iva
    
    def get_estado(self):
        return self.estado
    
    def get_id_usuario_act(self):
        return self.id_usuario_act
    
    def get_fecha_act(self):
        return self.fecha_act
    
    """ 
    Métodos que nos permiten setear con valores los atributos para 
    interactuar utilizando el patrón MVC.
    """ 
    def set_id(self, id_db):
        self.id_db = id_db
    
    def set_id_recibido(self, id_recibido):
        self.id_recibido = id_recibido
        
    def set_condicion(self, condicion):
        self.condicion = condicion
    
    def set_neto(self, neto):
        self.neto = neto
        
    def set_iva(self, iva):
        self.iva = iva
        
    def set_estado(self, estado):
        self.estado = estado
        
    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act
        
    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
