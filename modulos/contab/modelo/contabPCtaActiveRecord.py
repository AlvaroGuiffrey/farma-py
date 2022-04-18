# -*- coding: utf-8 -*-
#
# contabPCtaActiveRecord.py
#
# Creado: 14/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.contab.modelo.contabPCtaVO import ContabPCtaVO


class ContabPCtaActiveRecord(ContabPCtaVO):
    '''
    Clase que implementa el patrón Active Record en la tabla contab_p_cta.

    Permite realizar operaciones del tipo CRUD sobre la tabla contab_p_cta de
    la base de datos farma-py en mysql; hereda los atributos y métodos de la
    clase ContabPCtaVO; y La conexión a la base de datos se realiza por una
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

        @param cuenta: índice de la tabla desde contabPCtaVO.
        @return: contabPCtaVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM contab_p_ctas WHERE cuenta = %s")
        cursor.execute(consulta, (self.get_cuenta(),))
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


    def count(self):
        """
        Obtiene la cantidad de registros de la tabla.

        @return: se accede al valor por el metodo get_cantidad().
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT COUNT(*) FROM contab_p_ctas")
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
