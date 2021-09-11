#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: latin-1 -*-
#
# tarjCuponModelo.py
#
# Creado: 01/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.tarjCupon.modelo.tarjCuponActiveRecord import TarjCuponActiveRecord

class TarjCuponModelo(TarjCuponActiveRecord):
    '''
    Clase para realizar operaciones en la tabla tarj_cupones.

    Realiza operaciones varias de consultas sobre la  tabla tarj_cupones
    de la base de datos farma-py; hereda todos los métodos CRUD de la clase
    TarjCuponActiveRecord; y los atributos y métodos de la clase
    TarjCuponVO.
    '''

    def find_cupon_fecha(self):
        """
        Obtiene un registro activo por el cupon.

        @param cupon: TarjCuponVO.
        @param estado: 1 - activo.
        @return: TarjCuponVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_productos WHERE cupon = %s "
                    "AND estado = 1")
        valor = (self.get_cupon(), self.get_fecha())
        cursor.execute(consulta, valor)
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_cupon(dato[1])
            self.set_fecha(dato[2])
            self.set_numero(dato[3])
            self.set_id_producto(dato[4])
            self.set_moneda(dato[5])
            self.set_importe(dato[6])
            self.set_descuento(dato[7])
            self.set_neto(dato[8])
            self.set_cuota(dato[9])
            self.set_autorizacion(dato[10])
            self.set_error(dato[11])
            self.set_comentario(dato[12])
            self.set_fecha_presentacion(dato[13])
            self.set_lote(dato[14])
            self.set_liquidacion(dato[15])
            self.set_estado(dato[16])
            self.set_id_usuario_act(dato[17])
            self.set_fecha_act(dato[18])
            return dato
        else:
            return None

    def find_all(self):
        """
        Obtiene todos los registros activos de la tabla.

        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_cupones WHERE estado = 1")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha(self):
        """
        Obtiene todos los registros activos de una fecha.

        @param fecha: TarjCuponVO.
        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_cupones WHERE fecha=%s estado = 1")
        valor = (self.get_fecha(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_dic(self):
        """
        Obtiene todos los registros activos desde una fecha.

        @return: datos para construir el diccionario que se utiliza en agregar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, cupon, fecha, numero, lote "
                    "FROM tarj_cupones WHERE fecha >= %s AND estado=1")
        valor = (self.get_fecha(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_lote(self):
        """
        Obtiene todos los registros activos de un lote.

        @param lote: TarjCuponVO.
        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_cupones WHERE lote=%s estado = 1")
        cursor.execute(consulta, (self.get_lote(),))
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_liquidacion(self):
        """
        Obtiene todos los registros activos de una liquidacion.

        @param liquidacion: TarjCuponVO.
        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_cupones WHERE liquidacion=%s estado = 1")
        cursor.execute(consulta, (self.get_liquidacion(),))
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_error(self):
        """
        Obtiene todos los registros activos con un error.

        @param error: TarjCuponVO.
        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_cupones WHERE error=%s estado = 1")
        cursor.execute(consulta, (self.get_error(),))
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_listar(self, opciones):
        """
        Obtiene los registros activos para listar.

        Obtiene los registros activos de la tabla para listar en la vista
        según el rango y tipo de fechas seleccionado, ordenados por cupon.
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.
        @param tipo: si es la fecha de operación o presentación.
        @return: datos
        """

        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, cupon, fecha, numero, id_producto, moneda,"
                    "importe, error, fecha_pre, lote, liquidacion, comentario "
                    "FROM tarj_cupones WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha >= %s AND fecha <= %s ")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_pre >= %s AND fecha_pre <= %s ")
        consulta += ("AND estado=1 ORDER BY cupon, fecha")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
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
        @param TarjCuponVO: id, comentario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        cursor.execute("SET NAMES utf8;")
        cursor.execute("SET CHARACTER SET utf8;")
        query = ("UPDATE tarj_cupones SET comentario = %s, "
                "id_usuario_act = %s, fecha_act = %s WHERE id = %s")
        valor = (self.get_comentario(), self.get_id_usuario_act(),
                 self.get_fecha_act(), self.get_id())
        cursor.execute(query, valor)
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()