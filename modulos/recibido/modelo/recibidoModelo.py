#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# recibidoModelo.py
#
# Creado: 27/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.recibido.modelo.recibidoActiveRecord import RecibidoActiveRecord

class RecibidoModelo(RecibidoActiveRecord):
    '''
    Clase para realizar operaciones en la tabla recibidos.
    
    Realiza operaciones varias de consultas sobre la  tabla recididos 
    de la base de datos farma_py, hereda todos los métodos CRUD de la clase 
    RecibidoActiveRecord y los atributos y métodos de la clase RecibidoVO.
    '''

    def find_listar(self, opciones):
        """
        Obtiene los registros para listar.
        
        Obtiene los registros de la tabla para listar en la vista 
        según el rango de fechas seleccionado, ordenados por periodo, fecha 
        y número. 
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.  
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, periodo, fecha, tipo, punto_venta, numero,"
                    "nro_doc_emisor, importe_total, afip_rec, prov_rec "
                    "FROM recibidos WHERE fecha >= %s AND fecha <= %s "
                    "ORDER BY periodo, fecha, numero")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
    def find_buscar(self, opciones):
        """
        Obtiene los registros de la busqueda para listar.
        
        Obtiene los registros buscados de la tabla para listar en la vista 
        según el rango de fechas seleccionado (obligatorios) y otros (no
        obligatorios), ordenados por periodo, fecha e id.
        @param fecha_d: fecha desde donde comienza la consulta (oblig.).
        @param fecha_h: fecha máxima de la consulta (oblig.).
        @param tipo: tipo de comprobante según AFIP, valor 0 = todos.
        @param numero: numero del comprobante que se busca, valor 0 = todos.
        @param prov: número de doc del emisor según AFIP (CUIT, CUIL, etc).  
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valores = []
        valores.append(opciones['fecha_d'])
        valores.append(opciones['fecha_h'])
        consulta = ("SELECT id, periodo, fecha, tipo, punto_venta, numero,"
                    "nro_doc_emisor, importe_total, afip_rec, prov_rec "
                    "FROM recibidos WHERE fecha >= %s AND fecha <= %s ")
        if int(opciones['periodo']) > 0:
            consulta += (" AND periodo = %s")
            valores.append(opciones['periodo'])
        if int(opciones['tipo']) > 0:
            consulta += (" AND tipo = %s")
            valores.append(opciones['tipo']) 
        if int(opciones['numero']) > 0:
            consulta += (" AND numero = %s")
            valores.append(opciones['numero'])
        if not opciones['prov'] == "0":
            consulta += (" AND nro_doc_emisor = %s")
            valores.append(opciones['prov'])
        consulta += (" ORDER BY periodo, fecha, numero, id")
        valor = tuple(valores)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
    def find_conciliar(self, opciones):
        """
        Obtiene los registros para conciliar datos.
        
        Obtiene los registros de la tabla para conciliar datos con otras 
        tablas según el rango de fechas seleccionado. 
        @param fecha_d: fecha desde donde comienza la conciliación.
        @param fecha_h: fecha máxima de la conciliación.  
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, tipo, punto_venta, numero, nro_doc_emisor, "
                    "iva, importe_total, afip_rec, prov_rec FROM recibidos "
                    "WHERE fecha between %s AND %s AND "
                    "(afip_rec = 0 OR prov_rec = 0)")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
    def find_descargar(self, opciones):
        """
        Obtiene los registros de la busqueda para descargar.
        
        Obtiene los registros buscados de la tabla para descargar en un 
        archivo según el rango de fechas seleccionado (obligatorios) y 
        otros (no obligatorios), ordenados por fecha e id.
        @param fecha_d: fecha desde donde comienza la consulta (oblig.).
        @param fecha_h: fecha máxima de la consulta (oblig.).
        @param tipo: tipo de comprobante según AFIP, valor 0 = todos.
        @param numero: numero del comprobante que se busca, valor 0 = todos.
        @param prov: número de doc del emisor según AFIP (CUIT, CUIL, etc).   
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valores = []
        valores.append(opciones['fecha_d'])
        valores.append(opciones['fecha_h'])
        consulta = ("SELECT id, periodo, fecha, tipo, punto_venta, numero, " 
                "nro_doc_emisor, importe_gravado, importe_no_grav, "
                "importe_exento, iva, importe_total FROM recibidos "
                "WHERE fecha >= %s AND fecha <= %s ")
        if opciones['tipo']:
            if int(opciones['tipo']) > 0:
                consulta += (" AND tipo = %s")
                valores.append(opciones['tipo']) 
        if opciones['numero']:
            if int(opciones['numero']) > 0:
                consulta += (" AND numero = %s")
                valores.append(opciones['numero'])
        if opciones['prov']:
            if not opciones['prov'] == "0":
                consulta += (" AND nro_doc_emisor = %s")
                valores.append(opciones['prov'])
        consulta += (" ORDER BY fecha, numero, id")
        valor = tuple(valores)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
    def find_all_fecha_dic(self):
        """
        Obtiene todos los registros desde una fecha.
        
        @return: datos para construir el diccionario que se utiliza en agregar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, tipo, punto_venta, numero, nro_doc_emisor "
                    "FROM recibidos WHERE fecha >= %s")
        valor = (self.get_fecha(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
    def update_conciliar(self):
        """
        Modifica los datos del registro por conciliación.
        
        Persiste sobre la tabla modificando los datos por conciliación.
        @param RecibidoVO: id, afip_rec y prov_rec.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE recibidos SET afip_rec=%s, prov_rec=%s, "
                "id_usuario_act=%s, fecha_act=%s WHERE id=%s")
        valor = (self.get_afip_rec(), self.get_prov_rec(), 
                 self.get_id_usuario_act(), self.get_fecha_act(), 
                 self.get_id())
        cursor.execute(query, valor)
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        