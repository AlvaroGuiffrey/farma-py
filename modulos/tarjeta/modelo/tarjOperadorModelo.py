#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjOperadorModelo.py
#
# Creado: 01/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.tarjeta.modelo.tarjOperadorActiveRecord import TarjOperadorActiveRecord

class TarjOperadorModelo(TarjOperadorActiveRecord):
    '''
    Clase para realizar operaciones en la tabla tarj_operadores.

    Realiza operaciones varias de consultas sobre la  tabla tarj_operadores
    de la base de datos farma-py, hereda todos los métodos CRUD de la clase
    TarjOperadorActiveRecord, y los atributos y métodos de la clase
    TarjOperadorVO.
    '''

    def find_nombre(self):
        """
        Obtiene un registro por el nombre.

        @param TarjOperadorVO: nombre.
        @param estado: 1 - activo.
        @return: datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, nombre, inicial, id_proveedor"
                    "FROM tarj_operadores WHERE nombre= %s AND estado = 1")
        cursor.execute(consulta, (self.get_nombre(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_nombre(dato[1])
            self.set_inicial(dato[2])
            self.set_id_proveedor(dato[3])
            self.set_estado(dato[4])
            self.set_id_usuario_act(dato[5])
            self.set_fecha_act(dato[6])
            return dato
        else:
            return None

    def find_all(self):
        """
        Obtiene todos los registros de la tabla.

        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_operadores WHERE estado = 1")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
