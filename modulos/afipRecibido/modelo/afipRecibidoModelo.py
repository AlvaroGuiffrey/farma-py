# -*- coding: utf-8 -*-
# 
# afipRecibidoModelo.py
#
# Creado: 27/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.afipRecibido.modelo.afipRecibidoActiveRecord import AfipRecibidoActiveRecord

class AfipRecibidoModelo(AfipRecibidoActiveRecord):
    '''
    Clase para realizar operaciones en la tabla afip_recibidos.
    
    Realiza operaciones varias de consultas sobre la  tabla afip_recididos 
    de la base de datos farma_py, hereda todos los métodos CRUD de la clase 
    AfipRecibidoActiveRecord y los atributos y métodos de la clase 
    AfipRecibidoVO.
    '''

    def find_listar(self, opciones):
        """
        Obtiene los registros para listar.
        
        Obtiene los registros de la tabla para listar en la vista 
        según el rango de fechas seleccionado, ordenados por fecha e id.
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.  
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, fecha, tipo, punto_venta, numero_d,"
                    "nombre_emisor, importe_total, rec, prov_rec, "
                    "nro_doc_emisor, comentario "
                    "FROM afip_recibidos WHERE fecha >= %s AND "
                    "fecha <= %s ORDER BY fecha, numero_d, id")
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
        obligatorios), ordenados por fecha e id.
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
        consulta = ("SELECT id, fecha, tipo, punto_venta, numero_d, " 
                "nombre_emisor, importe_total, rec, prov_rec, nro_doc_emisor, "
                "comentario FROM afip_recibidos "
                "WHERE fecha >= %s AND fecha <= %s ")
        if int(opciones['tipo']) > 0:
            consulta += (" AND tipo = %s")
            valores.append(opciones['tipo']) 
        if int(opciones['numero']) > 0:
            consulta += (" AND numero_d = %s")
            valores.append(opciones['numero'])
        if not opciones['prov'] == "0":
            consulta += (" AND nro_doc_emisor = %s")
            valores.append(opciones['prov'])
        consulta += (" ORDER BY fecha, numero_d, id")
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
        consulta = ("SELECT id, tipo, punto_venta, numero_d, nro_doc_emisor, "
                    "iva, importe_total, rec, prov_rec FROM afip_recibidos "
                    "WHERE fecha between %s AND %s AND "
                    "(rec = 0 OR prov_rec = 0)") 
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
        consulta = ("SELECT id, fecha, tipo, punto_venta, numero_d, " 
                "nombre_emisor, importe_gravado, importe_no_grav, "
                "importe_exento, iva, importe_total FROM afip_recibidos "
                "WHERE fecha >= %s AND fecha <= %s ")
        if opciones['tipo']:
            if int(opciones['tipo']) > 0:
                consulta += (" AND tipo = %s")
                valores.append(opciones['tipo']) 
        if opciones['numero']:
            if int(opciones['numero']) > 0:
                consulta += (" AND numero_d = %s")
                valores.append(opciones['numero'])
        if opciones['prov']:
            if not opciones['prov'] == "0":
                consulta += (" AND nro_doc_emisor = %s")
                valores.append(opciones['prov'])
        consulta += (" ORDER BY fecha, numero_d, id")
        valor = tuple(valores)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
    def find_prov_select(self):
        """
        Obtiene los diferentes proveedores.
        
        @return: datos para construir el diccionario que se utiliza para
        el select de proveedores (cuit y nombre).
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = (
            "SELECT nro_doc_emisor, nombre_emisor AS c FROM "
            "afip_recibidos GROUP BY nro_doc_emisor "
            "ORDER BY nombre_emisor"
            )
        cursor.execute(query)
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
        consulta = ("SELECT id, tipo, punto_venta, numero_d, nro_doc_emisor "
                    "FROM afip_recibidos WHERE fecha >= %s")
        valor = (self.get_fecha(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close() 
        return datos
    
    def update_comentario(self):
        """
        Modifica los datos del registro.
        
        Persiste sobre la tabla modificando el comentario de un registro.
        @param AfipRecibidoVO: id, comentario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE afip_recibidos SET comentario = %s, "
                "id_usuario_act = %s, fecha_act = %s WHERE id = %s")
        valor = (self.get_comentario(), self.get_id_usuario_act(), 
                 self.get_fecha_act(), self.get_id())
        cursor.execute(query, valor)
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
    
    def update_conciliar(self):
        """
        Modifica los datos del registro por conciliación.
        
        Persiste sobre la tabla modificando los datos por conciliación.
        @param AfipRecibidoVO: id, rec y prov_rec.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE afip_recibidos SET rec = %s, prov_rec = %s, "
                "id_usuario_act = %s, fecha_act = %s WHERE id = %s")
        valor = (self.get_rec(), self.get_prov_rec(), 
                 self.get_id_usuario_act(), self.get_fecha_act(), self.get_id()
                 )
        cursor.execute(query, valor)
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        