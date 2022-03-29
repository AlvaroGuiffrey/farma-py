# -*- coding: utf-8 -*-
#
# chequeEmiModelo.py
#
# Creado: 19/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.chequeEmi.modelo.chequeEmiActiveRecord import ChequeEmiActiveRecord

class ChequeEmiModelo(ChequeEmiActiveRecord):
    '''
    Clase para realizar operaciones en la tabla cheques_emi.

    Realiza operaciones varias de consultas sobre la tabla cheques_emi
    de la base de datos farma-py; hereda todos los métodos CRUD de la clase
    ChequeEmiActiveRecord; y los atributos y métodos de la clase
    ChequeEmiVO.
    '''

    def find_numero(self):
        """
        Obtiene un registro activo por el numero de cheque.

        @param numero: ChequeEmiVO.
        @param estado: 1 - activo.
        @return: ChequeEmiVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM cheques_emi WHERE numero = %s "
                    "AND estado = 1")
        valor = (self.get_numero(),)
        cursor.execute(consulta, valor)
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

    def find_all(self):
        """
        Obtiene todos los registros activos de la tabla.

        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM cheques_emi WHERE estado = 1")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_emi(self):
        """
        Obtiene todos los registros activos de una fecha de emisión.

        @param fecha_emi: ChequeEmiVO.
        @param estado: 1 - activo.
        @return: datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM cheques_emi WHERE fecha_emi=%s "
                    "AND estado = 1")
        valor = (self.get_fecha_emi(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_pago(self):
        """
        Obtiene todos los registros activos de una fecha de pago.

        @param fecha_pago: ChequeEmiVO.
        @param estado: 1 - activo.
        @return: datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM cheques_emi WHERE fecha_pago=%s "
                    "AND estado = 1")
        valor = (self.get_fecha_emi(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_banco(self):
        """
        Obtiene todos los registros activos de una fecha debitados en banco.

        @param fecha_banco: ChequeEmiVO.
        @param estado: 1 - activo.
        @return: datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM cheques_emi WHERE fecha_banco=%s "
                    "AND estado = 1")
        valor = (self.get_fecha_banco(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_id_cheque_numero(self):
        """
        Obtiene todos los registros activos según parámetros.

        @param id_cheque: ChequeEmiVO.
        @param numero: ChequeEmiVO.
        @param estado: 1 - activo.
        @return: datos para ver si no existe el cheque a cargar o agregar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, id_cheque, numero, fecha_emi, estado_cheque "
                    "FROM cheques_emi WHERE id_cheque=%s AND numero=%s "
                    "AND estado=1")
        valor = (self.get_id_cheque(), self.get_numero())
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_listar(self, opciones):
        """
        Obtiene los registros activos para listar.

        Obtiene los registros activos de la tabla para listar en la vista
        según el rango y tipo de fechas seleccionado, ordenados por número.
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.
        @param tipo: si es la fecha de emisión, pago o débito.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, numero, fecha_emi, fecha_pago, "
                    "importe, nombre_emi, estado_cheque, fecha_banco "
                    "FROM cheques_emi WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_emi >= %s AND fecha_emi <= %s "
                        "AND estado=1 ORDER BY numero, fecha_emi")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_pago >= %s AND fecha_pago <= %s "
                        "AND estado=1 ORDER BY numero, fecha_pago")
        if int(opciones['tipo'])==3:
            consulta += ("fecha_banco >= %s AND fecha_banco <= %s "
                        "AND estado=1 ORDER BY numero, fecha_banco")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_inventario(self, opciones):
        """
        Obtiene los registros activos para listar el inventario.

        Obtiene los registros activos de la tabla para listar, en la vista,
        el inventario a la fecha seleccionada, ordenados por número.
        @param fecha: fecha del inventario.
        @param estado: 1 = activo.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, numero, fecha_emi, fecha_pago, "
                    "importe, nombre_emi, estado_cheque, fecha_banco "
                    "FROM cheques_emi WHERE fecha_emi <= %s AND "
                    "estado = 1 AND "
                    "fecha_banco = '0000-00-00' OR fecha_banco >= %s "
                    "ORDER BY numero")
        valor = (opciones['fecha'], opciones['fecha'])
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_buscar(self, opciones):
        """
        Obtiene los registros de la busqueda para listar.

        Obtiene los registros buscados de la tabla para listar en la vista
        según el rango y tipo de fechas seleccionado (obligatorios) y otros (no
        obligatorios), ordenados por fecha emisión y número.
        @param fecha_d: fecha desde donde comienza la consulta (oblig.).
        @param fecha_h: fecha máxima de la consulta (oblig.).
        @param tipo: tipo de fecha (emisión, pago y débito) (oblig.).
        @param numero: número del cheque que se busca, valor 0 = todos.
        @param nombre_emi: nombre del beneficiario, valor 0 = todos.
        @param estado_cheque: estado de los cheques que se buscan,
                                valor TODOS = todos.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valores = []
        valores.append(opciones['fecha_d'])
        valores.append(opciones['fecha_h'])
        consulta = ("SELECT id, numero, fecha_emi, fecha_pago, "
                    "importe, nombre_emi, estado_cheque, fecha_banco "
                    "FROM cheques_emi WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_emi >= %s AND fecha_emi <= %s ")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_pago >= %s AND fecha_pago <= %s ")
        if int(opciones['tipo'])==3:
            consulta += ("fecha_banco >= %s AND fecha_banco <= %s ")
        if int(opciones['numero']) > 0:
            consulta += (" AND numero = %s")
            valores.append(int(opciones['numero']))
        if str(opciones['nombre_emi']) != "0":
            consulta += (" AND nombre_emi = %s")
            valores.append(opciones['nombre_emi'])
        if str(opciones['estado_cheque']) != "TODOS":
            consulta += (" AND estado_cheque = %s")
            valores.append(opciones['estado_cheque'])
        if int(opciones['tipo'])==1:
            consulta += (" AND estado=1 ORDER BY fecha_emi, numero")
        if int(opciones['tipo'])==2:
            consulta += (" AND estado=1 ORDER BY fecha_pago, numero")
        if int(opciones['tipo'])==3:
            consulta += (" AND estado=1 ORDER BY fecha_banco, numero")
        valor = tuple(valores)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_nombre_emi_dic(self):
        """
        Obtiene todos los nombres de beneficiarios, sin repetir y ordenados,
        de registros activos.

        @return: datos para construir el diccionario que se utiliza en buscar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT DISTINCT nombre_emi FROM cheques_emi "
                    "WHERE estado=1 ORDER BY nombre_emi")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_dic(self):
        """
        Obtiene todos los registros activos desde una fecha de emisión.

        @return: datos para construir el diccionario que se utiliza en agregar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, id_cheque, numero, fecha_emi "
                    "FROM cheques_emi WHERE fecha_emi >= %s AND estado=1")
        valor = (self.get_fecha_emi(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
