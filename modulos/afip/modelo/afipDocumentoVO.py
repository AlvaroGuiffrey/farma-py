#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# afipDocumentoVO.py
#
# Creado: 05/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 
from builtins import int

class AfipDocumentoVO(object):
    """ 
    Clase que implementa el patrón Value Object para la tabla.
    
    Realiza un mapeo de los atributos de la tabla afip_documentos de 
    la base de datos farma en mysql, mediante la implememtación de métodos 
    get y set para interactuar con los controladores y las vistas.
    """
    
    # Atributos de instancia
    def __init__(self):
        """
        Método que inicializa los atributos de la instancia para mapear 
        las columnas de la tabla afip_comprobantes
        """
        self.codigo = int(0)
        self.descripcion = ''
                     
    # Métodos 
    """ 
    Métodos que nos permiten retornar el valor de los atributos para 
    interactuar utilizando el patrón MVC.
    """ 
    def get_codigo(self):
        return self.codigo
    
    def get_descripcion(self):
        return self.descripcion
    
    """ 
    Métodos que nos permiten setear con valores los atributos para 
    interactuar utilizando el patrón MVC.
    """ 
    def set_codigo(self, codigo):
        self.codigo = codigo
        
    def set_descripcion(self, descripcion):
        self.descripcion = descripcion
        