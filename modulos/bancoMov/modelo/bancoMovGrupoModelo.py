# -*- coding: utf-8 -*-
#
# bancoMovGrupoModelo.py
#
# Creado: 06/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.bancoMov.modelo.bancoMovGrupoActiveRecord import BancoMovGrupoActiveRecord

class BancoMovGrupoModelo(BancoMovGrupoActiveRecord):
    '''
    Clase para realizar operaciones en la tabla banco_mov_grupo.

    Realiza operaciones varias de consultas sobre la tabla banco_mov_grupo
    de la base de datos farma-py; hereda todos los métodos CRUD de la clase
    BancoMovGrupoActiveRecord; y los atributos y métodos de la clase
    BancoMovGrupoVO.
    '''

    def find_all(self):
        """
        Obtiene todos los registros activos de la tabla.

        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM banco_mov_grupo WHERE estado = 1")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
