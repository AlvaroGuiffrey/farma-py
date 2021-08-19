#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# recibidoActiveRecord.py
#
# Creado: 17/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.recibido.modelo.recibidoVO import RecibidoVO


class RecibidoActiveRecord(RecibidoVO):
    '''
    Clase que implementa el patrón Active Record en la tabla recibidos.
    
    Permite realizar operaciones del tipo CRUD sobre la tabla recididos de
    la base de datos farma en mysql. Hereda los atributos y métodos de la 
    clase RecibidoVO. 
    La conexión a la base de datos se realiza por una instancia de la clase 
    ConexionMySQL.
    '''
   
    # Atributos de la instancia:
    def __init__(self):
        """ 
        Iniciliza los atributos necesarios.
        """
        self.cantidad = int(0)
        self.id_insert = int(0)
        
    # Métodos:
    def find(self):
        """
        Obtiene un renglón de la tabla.
        
        @param id: índice de la tabla. 
        @return: RecibidoVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """ 
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM recibidos WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_periodo(dato[1])
            self.set_fecha(dato[2])
            self.set_tipo(dato[3])
            self.set_punto_venta(dato[4])
            self.set_numero(dato[5])
            self.set_nro_doc_emisor(dato[6])
            self.set_importe_gravado(dato[7])
            self.set_importe_no_grav(dato[8])
            self.set_importe_exento(dato[9])
            self.set_importe_mono(dato[10])
            self.set_perc_gan(dato[11])
            self.set_perc_iva(dato[12])
            self.set_perc_dgr(dato[13])
            self.set_perc_mun(dato[14])
            self.set_impuesto_int(dato[15])
            self.set_iva(dato[16])
            self.set_importe_total(dato[17])
            self.set_comentario(dato[18])
            self.set_estado(dato[19])
            self.set_afip_rec(dato[20])
            self.set_prov_rec(dato[21])
            self.set_id_usuario_act(dato[22])
            self.set_fecha_act(dato[23])
            return dato
        else:
            return None
        
    def insert(self):
        """
        Agrega un registro a la tabla.
        
        @param RecibidoVO: con los datos a insertar en el nuevo registro. 
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("INSERT INTO recibidos (periodo, fecha, tipo,"
                "punto_venta, numero, nro_doc_emisor, importe_gravado, "
                "importe_no_grav, importe_exento, importe_mono, "
                "perc_gan, perc_iva, perc_dgr, perc_mun, impuesto_int, "
                "iva, importe_total, comentario, estado, afip_rec, "
                "prov_rec, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        valor = (self.get_periodo(), self.get_fecha(), self.get_tipo(), 
                self.get_punto_venta(), self.get_numero(), 
                self.get_nro_doc_emisor(), self.get_importe_gravado(), 
                self.get_importe_no_grav(), self.get_importe_exento(),
                self.get_importe_mono(), self.get_perc_gan(),
                self.get_perc_iva(), self.get_perc_dgr(),
                self.get_perc_mun(), self.get_impuesto_int(), 
                self.get_iva(), self.get_importe_total(),
                self.get_comentario(), self.get_estado(),
                self.get_afip_rec(), self.get_prov_rec(), 
                self.get_id_usuario_act(), self.get_fecha_act())
        cursor.execute(query, valor)
        ccnx.commit()
        self.cantidad = cursor.rowcount
        self.id_insert = cursor.lastrowid
        cursor.close()
        ccnx.close()
            
    def count(self):
        """
        Obtiene la cantidad de registros de la tabla.
        
        @return: se accede al valor por el metodo get_cantidad().
        """    
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT COUNT(*) FROM recibidos")
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
    
    def get_id_insert(self):
        """ 
        Método para retornar el id del último insert.
        
        @return: se accede al id de la última operación insert realizada 
        en la tabla.
        """
        return self.id_insert