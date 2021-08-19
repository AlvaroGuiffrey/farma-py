#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# recibidoVO.py
#
# Creado: 17/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la librería estandar:
from builtins import int

class RecibidoVO(object):
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
        self.periodo = int(0)
        self.fecha = '0000-00-00'
        self.tipo = int(0)
        self.punto_venta = int(0)
        self.numero = int(0)
        self.nro_doc_emisor = int(0)
        self.importe_gravado = float(0.00)
        self.importe_no_grav = float(0.00)
        self.importe_exento = float(0.00)
        self.importe_mono = float(0.00)
        self.perc_gan = float(0.00)
        self.perc_iva = float(0.00)
        self.perc_dgr = float(0.00)
        self.perc_mun = float(0.00)
        self.impuesto_int = float(0.00)
        self.iva = float(0.00)
        self.importe_total = float(0.00)
        self.comentario = ''
        self.estado = int(0)
        self.afip_rec = int(0)
        self.prov_rec = int(0)
        self.id_usuario_act = int(0)
        self.fecha_act = '0000-00-00 00:00:00'
        
    # Métodos 
    """ 
    Métodos que nos permiten retornar el valor de los atributos para 
    interactuar utilizando el patrón MVC.
    """ 
    def get_id(self):
        return self.id_db
    
    def get_periodo(self):
        return self.periodo
    
    def get_fecha(self):
        return self.fecha
    
    def get_tipo(self):
        return self.tipo
    
    def get_punto_venta(self):
        return self.punto_venta
    
    def get_numero(self):
        return self.numero
    
    def get_nro_doc_emisor(self):
        return self.nro_doc_emisor
    
    def get_importe_gravado(self):
        return self.importe_gravado
    
    def get_importe_no_grav(self):
        return self.importe_no_grav
    
    def get_importe_exento(self):
        return self.importe_exento
    
    def get_importe_mono(self):
        return self.importe_mono
    
    def get_perc_gan(self):
        return self.perc_gan
    
    def get_perc_iva(self):
        return self.perc_iva
    
    def get_perc_dgr(self):
        return self.perc_dgr
    
    def get_perc_mun(self):
        return self.perc_mun
    
    def get_impuesto_int(self):
        return self.impuesto_int
    
    def get_iva(self):
        return self.iva
    
    def get_importe_total(self):
        return self.importe_total
    
    def get_comentario(self):
        return self.comentario
    
    def get_estado(self):
        return self.estado
    
    def get_afip_rec(self):
        return self.afip_rec
    
    def get_prov_rec(self):
        return self.prov_rec
    
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
    
    def set_periodo(self, periodo):
        self.periodo = periodo
        
    def set_fecha(self, fecha):
        self.fecha = fecha
    
    def set_tipo(self, tipo):
        self.tipo = tipo
        
    def set_punto_venta(self, punto_venta):
        self.punto_venta = punto_venta
        
    def set_numero(self, numero):
        self.numero = numero
        
    def set_nro_doc_emisor(self, nro_doc_emisor):
        self.nro_doc_emisor = nro_doc_emisor
        
    def set_importe_gravado(self, importe_gravado):
        self.importe_gravado = importe_gravado
        
    def set_importe_no_grav(self, importe_no_grav):
        self.importe_no_grav = importe_no_grav
        
    def set_importe_exento(self, importe_exento):
        self.importe_exento = importe_exento
        
    def set_importe_mono(self, importe_mono):
        self.importe_mono = importe_mono
        
    def set_perc_gan(self, perc_gan):
        self.perc_gan = perc_gan
        
    def set_perc_iva(self, perc_iva):
        self.perc_iva = perc_iva
        
    def set_perc_dgr(self, perc_dgr):
        self.perc_dgr = perc_dgr
        
    def set_perc_mun(self, perc_mun):
        self.perc_mun = perc_mun
        
    def set_impuesto_int(self, impuesto_int):
        self.impuesto_int = impuesto_int
        
    def set_iva(self, iva):
        self.iva = iva
        
    def set_importe_total(self, importe_total):
        self.importe_total = importe_total
        
    def set_comentario(self, comentario):
        self.comentario = comentario
        
    def set_estado(self, estado):
        self.estado = estado
        
    def set_afip_rec(self, afip_rec):
        self.afip_rec = afip_rec
        
    def set_prov_rec(self, prov_rec):
        self.prov_rec = prov_rec
        
    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act
        
    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
