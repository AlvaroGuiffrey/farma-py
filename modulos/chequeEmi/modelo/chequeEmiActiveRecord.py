# -*- coding: utf-8 -*-
#
# chequeEmiActiveRecord.py
#
# Creado: 18/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.chequeEmi.modelo.chequeEmiVO import ChequeEmiVO


class ChequeEmiActiveRecord(ChequeEmiVO):
    '''
    Clase que implementa el patrón Active Record en la tabla cheques_emi.

    Permite realizar operaciones del tipo CRUD sobre la tabla cheques_emi de
    la base de datos farma-py en mysql; hereda los atributos y métodos de la
    clase ChequeEmiVO; y La conexión a la base de datos se realiza por una
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

        @param id: índice de la tabla desde chequeEmiVO.
        @return: chequeEmiVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM cheques_emi WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_id_cheque(dato[1])
            self.set_numero(dato[2])
            self.set_fecha_emi(dato[3])
            self.set_fecha_pago(dato[4])
            self.set_importe(dato[5])
            self.set_cuit_emi(dato[6])
            self.set_nombre_emi(dato[7])
            self.set_cmc7(dato[8])
            self.set_tipo(dato[9])
            self.set_caracter(dato[10])
            self.set_concepto(dato[11])
            self.set_referencia(dato[12])
            self.set_valor_ref(dato[13])
            self.set_estado_cheque(dato[14])
            self.set_id_mov_banco(dato[15])
            self.set_fecha_banco(dato[16])
            self.set_estado(dato[17])
            self.set_id_usuario_act(dato[18])
            self.set_fecha_act(dato[19])
            return dato
        else:
            return None

    def insert(self):
        """
        Agrega un registro a la tabla.

        @param chequeEmiVO: con los datos a insertar en el nuevo registro.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valor = (self.get_id_cheque(), self.get_numero(), self.get_fecha_emi(),
                self.get_fecha_pago(), self.get_importe(), self.get_cuit_emi(),
                self.get_nombre_emi(), self.get_cmc7(), self.get_tipo(),
                self.get_caracter(), self.get_concepto(), self.get_referencia(),
                self.get_valor_ref(), self.get_estado_cheque(),
                self.get_id_mov_banco(), self.get_fecha_banco(),
                self.get_estado(), self.get_id_usuario_act(),
                self.get_fecha_act())
        query = ("INSERT INTO cheques_emi (id_cheque, numero, fecha_emi, "
                "fecha_pago, importe, cuit_emi, nombre_emi, cmc7, tipo, "
                "caracter, concepto, referencia, valor_ref, estado_cheque, "
                "id_mov_banco, fecha_banco, estado, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s, %s)")

        cursor.execute(query, valor)
        self.ultimo_id = cursor.lastrowid
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()

    def update(self):
        """
        Modifica los datos del registro.

        @param chequeEmiVO: datos varios.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE cheques_emi SET id_cheque=%s, numero=%s, fecha_emi=%s,"
                "fecha_pago=%s, importe=%s, cuit_emi=%s, nombre_emi=%s,"
                "cmc7=%s, tipo=%s, caracter=%s, concepto=%s,"
                "referencia=%s, valor_ref=%s, estado_cheque=%s,"
                "id_mov_banco=%s, fecha_banco=%s, estado=%s,"
                "id_usuario_act=%s, fecha_act=%s WHERE id=%s")
        valor = (self.get_id_cheque(), self.get_numero(), self.get_fecha_emi(),
                self.get_fecha_pago(), self.get_importe(), self.get_cuit_emi(),
                self.get_nombre_emi(), self.get_cmc7(), self.get_tipo(),
                self.get_caracter(), self.get_concepto(), self.get_referencia(),
                self.get_valor_ref(), self.get_estado_cheque(),
                self.get_id_mov_banco(), self.get_fecha_banco(),
                self.get_estado(), self.get_id_usuario_act(),
                self.get_fecha_act(), self.get_id())
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
        consulta = ("SELECT COUNT(*) FROM cheques_emi")
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
