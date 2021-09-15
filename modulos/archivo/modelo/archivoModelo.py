# -*- coding: utf-8 -*-
#
# archivoModelo.py
#
# Creado: 11/06/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.archivo.modelo.archivoActiveRecord import ArchivoActiveRecord


class ArchivoModelo(ArchivoActiveRecord):
    '''
    Clase para realizar operaciones en la tabla archivos.

    Realiza operaciones varias de consultas sobre la  tabla archivos
    de la base de datos farma, hereda todos los métodos CRUD de la clase
    ArchivoActiveRecord y los atributos y métodos de la clase
    ArchivoVO.
    '''

    def find_all(self):
        """
        Obtiene todos los registros.

        Obtiene los registros de la tabla, ordenados por id.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, nombre, estado, id_usuario_act, fecha_act"
                    "FROM archivos ORDER BY id")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_comparar(self):
        """
        Obtiene los registros para comparar.

        @return: datos para construir la lista que se utiliza para comparar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT nombre FROM archivos WHERE estado=1")
        valor = (self.get_fecha(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
