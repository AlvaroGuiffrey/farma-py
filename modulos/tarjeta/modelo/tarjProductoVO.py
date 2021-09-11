#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjProductoVO.py
#
# Creado: 01/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la libreria standar
from datetime import datetime
from builtins import int

# Modulos que se importan

class TarjProductoVO:

    # Atributos de clase

    # Atributos de instancia
    def __init__(self):
        self.id_db = int(0)
        self.nombre = str('')
        self.inicial = str('')
        self.codigo = str('')
        self.id_operador = int(0)
        self.estado = int(0)
        self.id_usuario_act = int(0)
        self.fecha_act = datetime.now()

    # Métodos
    """
    Métodos que nos permiten retornar el valor de los atributos para
    interactuar utilizando el patrón MVC.
    """
    def get_id(self):
        return self.id_db

    def get_nombre(self):
        return self.nombre

    def get_inicial(self):
        return self.inicial

    def get_codigo(self):
        return self.codigo

    def get_id_operador(self):
        return self.id_operador

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

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_inicial(self, inicial):
        self.inicial = inicial

    def set_codigo(self, codigo):
        self.codigo = codigo

    def set_id_operador(self, id_operador):
        self.id_operador = id_operador

    def set_estado(self, estado):
        self.estado = estado

    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act

    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
