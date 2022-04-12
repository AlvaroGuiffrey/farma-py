# -*- coding: utf-8 -*-
#
# bancoMovGrupoVO.py
#
# Creado: 06/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la libreria standar
from datetime import datetime
from builtins import int

# Modulos que se importan

class BancoMovGrupoVO:

    # Atributos de clase

    # Atributos de instancia
    def __init__(self):
        self.id_db = int(0)
        self.nombre = str('')
        self.orden = str('')
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

    def get_orden(self):
        return self.orden

    def get_id_grupo(self):
        return self.id_grupo

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

    def set_orden(self, orden):
        self.orden = orden

    def set_estado(self, estado):
        self.estado = estado

    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act

    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
