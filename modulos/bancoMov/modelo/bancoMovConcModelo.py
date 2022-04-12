# -*- coding: utf-8 -*-
#
# bancoMovConcModelo.py
#
# Creado: 06/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.bancoMov.modelo.bancoMovConcActiveRecord import BancoMovConcActiveRecord

class BancoMovConcModelo(BancoMovConcActiveRecord):
    '''
    Clase para realizar operaciones en la tabla banco_mov_conc.

    Realiza operaciones varias de consultas sobre la tabla banco_mov_conc
    de la base de datos farma-py; hereda todos los métodos CRUD de la clase
    BancoMovConcActiveRecord; y los atributos y métodos de la clase
    BancoMovConcVO.
    '''

    def find_concepto(self):
        """
        Obtiene un registro activo por el concepto del movimiento.

        @param concepto: BancoMovConcVO.
        @param estado: 1 - activo.
        @return: BancoMovConcVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM banco_mov_conc WHERE concepto = %s "
                    "AND estado = 1")
        valor = (self.get_concepto(),)
        cursor.execute(consulta, valor)
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_concepto(dato[1])
            self.set_comentario(dato[2])
            self.set_id_grupo(dato[3])
            self.set_estado(dato[4])
            self.set_id_usuario_act(dato[5])
            self.set_fecha_act(dato[6])
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
        consulta = ("SELECT * FROM banco_mov_conc WHERE estado = 1")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
