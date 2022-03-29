# -*- coding: utf-8 -*-
#
# chequeEmiVO.py
#
# Creado: 16/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la libreria standar
from datetime import datetime
from builtins import int

# Modulos que se importan

class ChequeEmiVO:

    # Atributos de clase

    # Atributos de instancia
    def __init__(self):
        self.id_db = int(0)
        self.id_cheque = str('')
        self.numero = int(0)
        self.fecha_emi = date.today()
        self.fecha_pago = date.today()
        self.importe = float(-0.00)
        self.cuit_emi = str('')
        self.nombre_emi = str('')
        self.cmc7 = str('')
        self.tipo = str('')
        self.caracter = str('')
        self.concepto = str('')
        self.referencia = str('')
        self.valor_ref = str('')
        self.estado_cheque = str('')
        self.id_mov_banco = int(0)
        self.fecha_banco = date.today()
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

    def get_id_cheque(self):
        return self.id_cheque

    def get_numero(self):
        return self.numero

    def get_fecha_emi(self):
        return self.fecha_emi

    def get_fecha_pago(self):
        return self.fecha_pago

    def get_importe(self):
        return self.importe

    def get_cuit_emi(self):
        return self.cuit_emi

    def get_nombre_emi(self):
        return self.nombre_emi

    def get_cmc7(self):
        return self.cmc7

    def get_tipo(self):
        return self.tipo

    def get_caracter(self):
        return self.caracter

    def get_concepto(self):
        return self.concepto

    def get_referencia(self):
        return self.referencia

    def get_valor_ref(self):
        return self.valor_ref

    def get_estado_cheque(self):
        return self.estado_cheque

    def get_id_mov_banco(self):
        return self.id_mov_banco

    def get_fecha_banco(self):
        return self.fecha_banco

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

    def set_id_cheque(self, id_cheque):
        self.id_cheque = id_cheque

    def set_numero(self, numero):
        self.numero = numero

    def set_fecha_emi(self, fecha_emi):
        self.fecha_emi = fecha_emi

    def set_fecha_pago(self, fecha_pago):
        self.fecha_pago = fecha_pago

    def set_importe(self, importe):
        self.importe = importe

    def set_cuit_emi(self, cuit_emi):
        self.cuit_emi = cuit_emi

    def set_nombre_emi(self, nombre_emi):
        self.nombre_emi = nombre_emi

    def set_cmc7(self, cmc7):
        self.cmc7 = cmc7

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_caracter(self, caracter):
        self.caracter = caracter

    def set_concepto(self, concepto):
        self.concepto = concepto

    def set_referencia(self, referencia):
        self.referencia = referencia

    def set_valor_ref(self, valor_ref):
        self.valor_ref = valor_ref

    def set_estado_cheque(self, estado_cheque):
        self.estado_cheque = estado_cheque

    def set_id_mov_banco(self, id_mov_banco):
        self.id_mov_banco = id_mov_banco

    def set_fecha_banco(self, fecha_banco):
        self.fecha_banco = fecha_banco

    def set_estado(self, estado):
        self.estado = estado

    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act

    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
