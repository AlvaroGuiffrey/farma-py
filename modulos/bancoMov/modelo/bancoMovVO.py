# -*- coding: utf-8 -*-
#
# bancoMovVO.py
#
# Creado: 30/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la libreria standar
from datetime import datetime
from builtins import int

# Modulos que se importan

class BancoMovVO:

    # Atributos de clase

    # Atributos de instancia
    def __init__(self):
        self.id_db = int(0)
        self.fecha_mov = date.today()
        self.fecha_valor = date.today()
        self.importe = float(-0.00)
        self.numero = int(0)
        self.concepto = str('')
        self.id_grupo = int(0)
        self.marca = int(0)
        self.comentario = str('')
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

    def get_fecha_mov(self):
        return self.fecha_mov

    def get_fecha_valor(self):
        return self.fecha_valor

    def get_importe(self):
        return self.importe

    def get_numero(self):
        return self.numero

    def get_concepto(self):
        return self.concepto

    def get_id_grupo(self):
        return self.id_grupo

    def get_marca(self):
        return self.marca

    def get_comentario(self):
        return self.comentario

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

    def set_fecha_mov(self, fecha_mov):
        self.fecha_mov = fecha_mov

    def set_fecha_valor(self, fecha_valor):
        self.fecha_valor = fecha_valor

    def set_importe(self, importe):
        self.importe = importe

    def set_numero(self, numero):
        self.numero = numero

    def set_concepto(self, concepto):
        self.concepto = concepto

    def set_id_grupo(self, id_grupo):
        self.id_grupo = id_grupo

    def set_marca(self, marca):
        self.marca = marca

    def set_comentario(self, comentario):
        self.comentario = comentario

    def set_estado(self, estado):
        self.estado = estado

    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act

    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
