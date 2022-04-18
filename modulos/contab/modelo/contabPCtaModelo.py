# -*- coding: utf-8 -*-
#
# contabPCtaModelo.py
#
# Creado: 14/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.contab.modelo.contabPCtaActiveRecord import ContabPCtaActiveRecord

class ContabPCtaModelo(ContabPCtaActiveRecord):
    '''
    Clase para realizar operaciones en la tabla contab_p_ctas.

    Realiza operaciones varias de consultas sobre la tabla contab_p_ctas
    de la base de datos farma-py; hereda todos los métodos CRUD de la clase
    ContabPCtaActiveRecord; y los atributos y métodos de la clase
    ContabPCtaVO.
    '''

    def find_nombre(self):
        """
        Obtiene un registro activo por el nombre de la cuenta.

        @param nombre: ContabPCtaVO.
        @param inactiva: 0 - activa.
        @return: ContabPCtaVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM contab_p_ctas WHERE nombre = %s "
                    "AND inactiva = 0")
        valor = (self.get_nombre(),)
        cursor.execute(consulta, valor)
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_cuenta(dato[0])
            self.set_sub_cuenta(dato[1])
            self.set_nombre(dato[2])
            self.set_rubro(dato[3])
            self.set_inactiva(dato[4])
            return dato
        else:
            return None

    def find_all(self):
        """
        Obtiene todos los registros activos de la tabla.

        @param inactiva: 0 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM contab_p_ctas WHERE inactiva = 0")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
