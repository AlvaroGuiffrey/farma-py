# -*- coding: utf-8 -*-
#
# contabPCtaVO.py
#
# Creado: 14/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la libreria standar
from datetime import datetime
from builtins import int

# Modulos que se importan

class ContabPCtaVO:

    # Atributos de clase

    # Atributos de instancia
    def __init__(self):
        self.cuenta = str('')
        self.sub_cuenta = str('')
        self.nombre = str('')
        self.rubro = str('')
        self.inactiva = int(0)

    # Métodos
    """
    Métodos que nos permiten retornar el valor de los atributos para
    interactuar utilizando el patrón MVC.
    """
    def get_cuenta(self):
        return self.cuenta

    def get_sub_cuenta(self):
        return self.sub_cuenta

    def get_nombre(self):
        return self.nombre

    def get_rubro(self):
        return self.rubro

    def get_inactiva(self):
        return self.inactiva

    """
    Métodos que nos permiten setear con valores los atributos para
    interactuar utilizando el patrón MVC.
    """
    def set_cuenta(self, cuenta):
        self.cuenta = cuenta

    def set_sub_cuenta(self, sub_cuenta):
        self.sub_cuenta = sub_cuenta

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_rubro(self, rubro):
        self.rubro = rubro

    def set_inactiva(self, inactiva):
        self.inactiva = inactiva
