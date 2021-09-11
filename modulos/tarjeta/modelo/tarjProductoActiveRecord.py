#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjProductoActiveRecord.py
#
# Creado: 01/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.tarjeta.modelo.tarjProductoVO import TarjProductoVO


class TarjProductoActiveRecord(TarjProductoVO):
    '''
    Clase que implementa el patrón Active Record en la tabla tarj_productos.

    Permite realizar operaciones del tipo CRUD sobre la tabla tarj_productos de
    la base de datos farma-py en mysql; hereda los atributos y métodos de la
    clase TarjProductoVO; y La conexión a la base de datos se realiza por una
    instancia de la clase ConexionMySQL.
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

        @param id: índice de la tabla de TarjProductoVO.
        @return: TarjProductoVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_productos WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_nombre(dato[1])
            self.set_inicial(dato[2])
            self.set_codigo(dato[3])
            self.set_id_operador(dato[4])
            self.set_estado(dato[5])
            self.set_id_usuario_act(dato[6])
            self.set_fecha_act(dato[7])
            return dato
        else:
            return None

    def insert(self):
        """
        Agrega un registro a la tabla.

        @param TarjProductoVO: con los datos a insertar en el nuevo registro.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("INSERT INTO tarj_productos (nombre, inicial, codigo,"
                "id_operador, estado, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s)")
        valor = (self.get_nombre(), self.get_inicial(), self.get_codigo(),
                self.get_id_proveedor(), self.get_estado(),
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
        consulta = ("SELECT COUNT(*) FROM tarj_productos")
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
