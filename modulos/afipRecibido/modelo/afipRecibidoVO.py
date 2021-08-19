#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# afipRecibidoVO.py
#
# Creado: 27/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la librería estandar:
from builtins import int

class AfipRecibidoVO(object):
    """ 
    Clase que implementa el patrón Value Object para la tabla.
    
    Realiza un mapeo de los atributos de la tabla afip_recibidos de la 
    base de datos farma en mysql, mediante la implememtación de métodos 
    get y set para interactuar con los controladores y las vistas.
    """
 
    # Atributos de instancia
    def __init__(self):
        """
        Método que inicializa los atributos de la instancia para mapear las
        columnas de la tabla afip_recibidos
        """
        self.id_db = int(0)
        self.fecha = '0000-00-00'
        self.tipo = int(0)
        self.punto_venta = int(0)
        self.numero_d = int(0)
        self.numero_h = int(0)
        self.cai = int(0)
        self.tipo_doc_emisor = int(0)
        self.nro_doc_emisor = int(0)
        self.nombre_emisor = ''
        self.tipo_cambio = int(0)
        self.moneda = ''
        self.importe_gravado = float(0.00)
        self.importe_no_grav = float(0.00)
        self.importe_exento = float(0.00)
        self.iva = float(0.00)
        self.importe_total = float(0.00)
        self.comentario = ''
        self.estado = int(0)
        self.rec = int(0)
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
    
    def get_fecha(self):
        return self.fecha
    
    def get_tipo(self):
        return self.tipo
    
    def get_punto_venta(self):
        return self.punto_venta
    
    def get_numero_d(self):
        return self.numero_d
    
    def get_numero_h(self):
        return self.numero_h
    
    def get_cai(self):
        return self.cai
    
    def get_tipo_doc_emisor(self):
        return self.tipo_doc_emisor
    
    def get_nro_doc_emisor(self):
        return self.nro_doc_emisor
    
    def get_nombre_emisor(self):
        return self.nombre_emisor
    
    def get_tipo_cambio(self):
        return self.tipo_cambio
    
    def get_moneda(self):
        return self.moneda
    
    def get_importe_gravado(self):
        return self.importe_gravado
    
    def get_importe_no_grav(self):
        return self.importe_no_grav
    
    def get_importe_exento(self):
        return self.importe_exento
    
    def get_iva(self):
        return self.iva
    
    def get_importe_total(self):
        return self.importe_total
    
    def get_comentario(self):
        return self.comentario
    
    def get_estado(self):
        return self.estado
    
    def get_rec(self):
        return self.rec
    
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
        
    def set_fecha(self, fecha):
        self.fecha = fecha
    
    def set_tipo(self, tipo):
        self.tipo = tipo
        
    def set_punto_venta(self, punto_venta):
        self.punto_venta = punto_venta
        
    def set_numero_d(self, numero_d):
        self.numero_d = numero_d
        
    def set_numero_h(self, numero_h):
        self.numero_h = numero_h
        
    def set_cai(self, cai):
        self.cai = cai
        
    def set_tipo_doc_emisor(self, tipo_doc_emisor):
        self.tipo_doc_emisor = tipo_doc_emisor
        
    def set_nro_doc_emisor(self, nro_doc_emisor):
        self.nro_doc_emisor = nro_doc_emisor
        
    def set_nombre_emisor(self, nombre_emisor):
        self.nombre_emisor = nombre_emisor
        
    def set_tipo_cambio(self, tipo_cambio):
        self.tipo_cambio = tipo_cambio
        
    def set_moneda(self, moneda):
        self.moneda = moneda
        
    def set_importe_gravado(self, importe_gravado):
        self.importe_gravado = importe_gravado
        
    def set_importe_no_grav(self, importe_no_grav):
        self.importe_no_grav = importe_no_grav
        
    def set_importe_exento(self, importe_exento):
        self.importe_exento = importe_exento
        
    def set_iva(self, iva):
        self.iva = iva
        
    def set_importe_total(self, importe_total):
        self.importe_total = importe_total
        
    def set_comentario(self, comentario):
        self.comentario = comentario
    
    def set_estado(self, estado):
        self.estado = estado
    
    def set_rec(self, rec):
        self.rec = rec
        
    def set_prov_rec(self, prov_rec):
        self.prov_rec = prov_rec
            
    def set_id_usuario_act(self, id_usuario_act):
        self.id_usuario_act = id_usuario_act
        
    def set_fecha_act(self, fecha_act):
        self.fecha_act = fecha_act
            