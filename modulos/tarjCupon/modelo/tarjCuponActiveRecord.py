#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjCuponActiveRecord.py
#
# Creado: 01/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.tarjCupon.modelo.tarjCuponVO import TarjCuponVO


class TarjCuponActiveRecord(TarjCuponVO):
    '''
    Clase que implementa el patrón Active Record en la tabla tarj_cupones.

    Permite realizar operaciones del tipo CRUD sobre la tabla tarj_cupones de
    la base de datos farma-py en mysql; hereda los atributos y métodos de la
    clase TarjCuponVO; y La conexión a la base de datos se realiza por una
    instancia de la clase ConexionMySQL.
    '''

    # Atributos de la instancia:
    def __init__(self):
        """
        Iniciliza los atributos necesarios.
        """
        self.cantidad = int(0)
        self.ultimo_id = int(0)

    # Métodos:
    def find(self):
        """
        Obtiene un renglón de la tabla.

        @param id: índice de la tabla desde TarjCuponVO.
        @return: TarjCuponVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_cupones WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
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

    def insert(self):
        """
        Agrega un registro a la tabla.

        @param TarjCuponVO: con los datos a insertar en el nuevo registro.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valor = (self.get_cupon(), self.get_fecha(), self.get_numero(),
                self.get_id_producto(), self.get_moneda(), self.get_importe(),
                self.get_descuento(), self.get_neto(), self.get_cuota(),
                self.get_autorizacion(), self.get_error(),
                self.get_comentario(), self.get_fecha_presentacion(),
                self.get_lote(), self.get_liquidacion(), self.get_estado(),
                self.get_id_usuario_act(), self.get_fecha_act())
        query = ("INSERT INTO tarj_cupones (cupon, fecha, numero, id_producto, "
                "moneda, importe, descuento, neto, cuota, autorizacion, "
                "error, comentario, fecha_pre, lote, liquidacion, "
                "estado, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s)")

        cursor.execute(query, valor)
        self.ultimo_id = cursor.lastrowid
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()

    def update(self):
        """
        Modifica los datos del registro.

        @param TarjCuponVO: datos varios.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE tarj_cupones SET cupon=%s, fecha=%s, numero=%s,"
                "id_producto=%s, moneda=%s, importe=%s, descuento=%s, neto=%s,"
                "cuota=%s, autorizacion=%s, error=%s, comentario=%s,"
                "fecha_pre=%s, lote=%s, liquidacion=%s, estado=%s,"
                "id_usuario_act=%s, fecha_act=%s WHERE id=%s")
        valor = (self.get_cupon(), self.get_fecha(), self.get_numero(),
                 self.get_id_producto(), self.get_moneda(), self.get_importe(),
                 self.get_descuento(), self.get_neto(), self.get_cuota(),
                 self.get_autorizacion(), self.get_error(),
                 self.get_comentario(), self.get_fecha_presentacion(),
                 self.get_lote(), self.get_liquidacion(), self.get_estado(),
                 self.get_id_usuario_act(), self.get_fecha_act(),
                 self.get_id())
        cursor.execute(query, valor)
        self.ultimo_id = cursor.lastrowid
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
        consulta = ("SELECT COUNT(*) FROM tarj_cupones")
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

    def get_ultimo_id(self):
        """
        Método para retornar el último id.

        @return: se accede al valor del id del registros de
                la última operación realizada en la tabla.
        """
        return self.ultimo_id
