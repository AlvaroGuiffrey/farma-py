#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# provRecibidoActiveRecord.py
#
# Creado: 19/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.provRecibido.modelo.provRecibidoVO import ProvRecibidoVO


class ProvRecibidoActiveRecord(ProvRecibidoVO):
    '''
    Clase que implementa el patrón Active Record en la tabla prov_recibidos.
    
    Permite realizar operaciones del tipo CRUD sobre la tabla prov_recididos de
    la base de datos farma en mysql. Hereda los atributos y métodos de la 
    clase ProvRecibidoVO. 
    La conexión a la base de datos se realiza por una instancia de la clase 
    ConexionMySQL.
    '''
   
    # Atributos de la instancia:
    def __init__(self):
        """ 
        Iniciliza los atributos necesarios.
        """
        self.cantidad = int(0)
        
    # Métodos:
    def find(self):
        """
        Obtiene un renglón de la tabla.
        
        @param id: índice de la tabla. 
        @return: ProvRecibidoVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """ 
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM prov_recibidos WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_fecha(dato[1])
            self.set_tipo(dato[2])
            self.set_punto_venta(dato[3])
            self.set_numero(dato[4])
            self.set_nro_doc_emisor(dato[5])
            self.set_importe_gravado(dato[6])
            self.set_importe_no_grav(dato[7])
            self.set_importe_exento(dato[8])
            self.set_importe_mono(dato[9])
            self.set_perc_gan(dato[10])
            self.set_perc_iva(dato[11])
            self.set_perc_dgr(dato[12])
            self.set_perc_mun(dato[13])
            self.set_impuesto_int(dato[14])
            self.set_iva(dato[15])
            self.set_importe_total(dato[16])
            self.set_comentario(dato[17])
            self.set_estado(dato[18])
            self.set_afip_rec(dato[19])
            self.set_rec(dato[20])
            self.set_id_usuario_act(dato[21])
            self.set_fecha_act(dato[22])
            return dato
        else:
            return None
        
    def insert(self):
        """
        Agrega un registro a la tabla.
        
        @param ProvRecibidoVO: con los datos a insertar en el nuevo registro. 
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("INSERT INTO prov_recibidos (fecha, tipo,"
                "punto_venta, numero, nro_doc_emisor, importe_gravado, "
                "importe_no_grav, importe_exento, importe_mono,"
                "perc_gan, perc_iva, perc_dgr, perc_mun, impuesto_int, "
                "iva, importe_total, comentario, estado, afip_rec, "
                "rec, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        valor = (self.get_fecha(), self.get_tipo(), 
                self.get_punto_venta(), self.get_numero(), 
                self.get_nro_doc_emisor(), self.get_importe_gravado(), 
                self.get_importe_no_grav(), self.get_importe_exento(),
                self.get_importe_mono(), self.get_perc_gan(),
                self.get_perc_iva(), self.get_perc_dgr(),
                self.get_perc_mun(), self.get_impuesto_int(), 
                self.get_iva(), self.get_importe_total(),
                self.get_comentario(), self.get_estado(),
                self.get_afip_rec(), self.get_rec(), 
                self.get_id_usuario_act(), self.get_fecha_act())
        cursor.execute(query, valor)
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
    
    def count(self):
        """
        Obtiene la cantidad de registros de la tabla.
        
        @return: se accede al valor por el metodo get_cantidad().
        """    
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT COUNT(*) FROM prov_recibidos")
        cursor.execute(consulta)
        dato = cursor.fetchone()
        self.cantidad = dato[0]
        cursor.close()
        ccnx.close()        
    
    def get_cantidad(self):
        """ 
        Método para retornar la cantidad de registros.
        
        @return: se accede al valor de la cantidad de registros afectados de
                la última operación realizada en la tabla.
        """
        return self.cantidad
    
