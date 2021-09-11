#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjCuponVO.py
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

class TarjCuponVO:

    # Atributos de clase

    # Atributos de instancia
    def __init__(self):
        self.id_db = int(0)
        self.cupon = int(0)
        self.fecha = date.today()
        self.numero = int(0)
        self.id_producto = int(0)
        self.moneda = str('')
        self.importe = float(-0.00)
        self.descuento = float(-0.00)
        self.neto = float(-0.00)
        self.cuota = int(0)
        self.autorizacion = int(0)
        self.error = int(0)
        self.comentario = str('')
        self.fecha_presentacion = date.today()
        self.lote = int(0)
        self.liquidacion = int(0)
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

    def get_cupon(self):
        return self.cupon

    def get_fecha(self):
        return self.fecha

    def get_numero(self):
        return self.numero

    def get_id_producto(self):
        return self.id_producto

    def get_moneda(self):
        return self.moneda

    def get_importe(self):
        return self.importe

    def get_descuento(self):
        return self.descuento

    def get_neto(self):
        return self.neto

    def get_cuota(self):
        return self.cuota

    def get_autorizacion(self):
        return self.autorizacion

    def get_error(self):
        return self.error

    def get_comentario(self):
        return self.comentario

    def get_fecha_presentacion(self):
        return self.fecha_presentacion

    def get_lote(self):
        return self.lote

    def get_liquidacion(self):
        return self.liquidacion

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

    def set_cupon(self, cupon):
        self.cupon = cupon

    def set_fecha(self, fecha):
        self.fecha = fecha

    def set_numero(self, numero):
        self.numero = numero

    def set_id_producto(self, id_producto):
        self.id_producto = id_producto

    def set_moneda(self, moneda):
        self.moneda = moneda

    def set_importe(self, importe):
        self.importe = importe

    def set_descuento(self, descuento):
        self.descuento = descuento

    def set_neto(self, neto):
        self.neto = neto

    def set_cuota(self, cuota):
        self.cuota = cuota

    def set_autorizacion(self, autorizacion):
        self.autorizacion = autorizacion

    def set_error(self, error):
        self.error = error

    def set_comentario(self, comentario):
        self.comentario = comentario

    def set_fecha_presentacion(self, fecha_presentacion):
        self.fecha_presentacion = fecha_presentacion

    def set_lote(self, lote):
        self.lote = lote

    def set_liquidacion(self, liquidacion):
        self.liquidacion = liquidacion
                    
    def set_estado(self, estado):
        self.estado = estado

    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act

    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
