# -*- coding: utf-8 -*-
#
# tarjLiqVO.py
#
# Creado: 14/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la libreria standar
from datetime import datetime
from builtins import int

# Modulos que se importan

class TarjLiqVO:

    # Atributos de clase

    # Atributos de instancia
    def __init__(self):
        self.id_db = int(0)
        self.liquidacion = int(0)
        self.id_producto = int(0)
        self.fecha_pago = date.today()
        self.banco_suc = str('')
        self.moneda = str('')
        self.importe_bruto = float(-0.00)
        self.importe_desc = float(-0.00)
        self.importe_neto = float(-0.00)
        self.cupones = int(0)
        self.marca_cupones = int(0)
        self.fecha_proceso = date.today()
        self.marca_banco = int(0)
        self.fecha_banco = date.today()
        self.opera_banco = int(0)
        self.arancel = float(-0.00)
        self.costo_financiero = float(-0.00)
        self.iva_arancel = float(-0.00)
        self.iva_costo_financiero = float(-0.00)
        self.impuesto_debcred = float(-0.00)
        self.impuesto_interes = float(-0.00)
        self.retencion_iva = float(-0.00)
        self.retencion_imp_gan = float(-0.00)
        self.retencion_ing_brutos = float(-0.00)
        self.percepcion_iva = float(-0.00)
        self.percepcion_ing_brutos = float(-0.00)
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

    def get_liquidacion(self):
        return self.liquidacion

    def get_id_producto(self):
        return self.id_producto

    def get_id_operador(self):
        return self.id_operador

    def get_fecha_pago(self):
        return self.fecha_pago

    def get_banco_suc(self):
        return self.banco_suc

    def get_moneda(self):
        return self.moneda

    def get_importe_bruto(self):
        return self.importe_bruto

    def get_importe_desc(self):
        return self.importe_desc

    def get_importe_neto(self):
        return self.importe_neto

    def get_cupones(self):
        return self.cupones

    def get_marca_cupones(self):
        return self.marca_cupones

    def get_fecha_proceso(self):
        return self.fecha_proceso

    def get_marca_banco(self):
        return self.marca_banco

    def get_fecha_banco(self):
        return self.fecha_banco

    def get_opera_banco(self):
        return self.opera_banco

    def get_arancel(self):
        return self.arancel

    def get_costo_financiero(self):
        return self.costo_financiero

    def get_otros_deb(self):
        return self.otros_deb

    def get_iva_arancel(self):
        return self.iva_arancel

    def get_iva_costo_financiero(self):
        return self.iva_costo_financiero

    def get_iva_otros_deb(self):
        return self.iva_otros_deb

    def get_impuesto_debcred(self):
        return self.impuesto_debcred

    def get_impuesto_interes(self):
        return self.impuesto_interes

    def get_retencion_iva(self):
        return self.retencion_iva

    def get_retencion_imp_gan(self):
        return self.retencion_imp_gan

    def get_retencion_ing_brutos(self):
        return self.retencion_ing_brutos

    def get_percepcion_iva(self):
        return self.percepcion_iva

    def get_percepcion_ing_brutos(self):
        return self.percepcion_ing_brutos

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

    def set_liquidacion(self, liquidacion):
        self.liquidacion = liquidacion

    def set_id_producto(self, id_producto):
        self.id_producto = id_producto

    def set_id_operador(self, id_operador):
        self.id_operador = id_operador

    def set_fecha_pago(self, fecha_pago):
        self.fecha_pago = fecha_pago

    def set_banco_suc(self, banco_suc):
        self.banco_suc = banco_suc

    def set_moneda(self, moneda):
        self.moneda = moneda

    def set_importe_bruto(self, importe_bruto):
        self.importe_bruto = importe_bruto

    def set_importe_desc(self, importe_desc):
        self.importe_desc = importe_desc

    def set_importe_neto(self, importe_neto):
        self.importe_neto = importe_neto

    def set_cupones(self, cupones):
        self.cupones = cupones

    def set_marca_cupones(self, marca_cupones):
        self.marca_cupones = marca_cupones

    def set_fecha_proceso(self, fecha_proceso):
        self.fecha_proceso = fecha_proceso

    def set_marca_banco(self, marca_banco):
        self.marca_banco = marca_banco

    def set_fecha_banco(self, fecha_banco):
        self.fecha_banco = fecha_banco

    def set_opera_banco(self, opera_banco):
        self.opera_banco = opera_banco

    def set_arancel(self, arancel):
        self.arancel = arancel

    def set_costo_financiero(self, costo_financiero):
        self.costo_financiero = costo_financiero

    def set_otros_deb(self, otros_deb):
        self.otros_deb = otros_deb

    def set_iva_arancel(self, iva_arancel):
        self.iva_arancel = iva_arancel

    def set_iva_costo_financiero(self, iva_costo_financiero):
        self.iva_costo_financiero = iva_costo_financiero

    def set_iva_otros_deb(self, iva_otros_deb):
        self.iva_otros_deb = iva_otros_deb

    def set_impuesto_debcred(self, impuesto_debcred):
        self.impuesto_debcred = impuesto_debcred

    def set_impuesto_interes(self, impuesto_interes):
        self.impuesto_interes = impuesto_interes

    def set_retencion_iva(self, retencion_iva):
        self.retencion_iva = retencion_iva

    def set_retencion_imp_gan(self, retencion_imp_gan):
        self.retencion_imp_gan = retencion_imp_gan

    def set_retencion_ing_brutos(self, retencion_ing_brutos):
        self.retencion_ing_brutos = retencion_ing_brutos

    def set_percepcion_iva(self, percepcion_iva):
        self.percepcion_iva = percepcion_iva

    def set_percepcion_ing_brutos(self, percepcion_ing_brutos):
        self.percepcion_ing_brutos = percepcion_ing_brutos

    def set_estado(self, estado):
        self.estado = estado

    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act

    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
