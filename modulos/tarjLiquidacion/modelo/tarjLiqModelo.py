#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: latin-1 -*-
#
# tarjLiqModelo.py
#
# Creado: 15/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.tarjLiquidacion.modelo.tarjLiqActiveRecord import TarjLiqActiveRecord

class TarjLiqModelo(TarjLiqActiveRecord):
    '''
    Clase para realizar operaciones en la tabla tarj_liquidaciones.

    Realiza operaciones varias de consultas sobre la  tabla tarj_liquidaciones
    de la base de datos farma-py; hereda todos los métodos CRUD de la clase
    TarjLiqActiveRecord; y los atributos y métodos de la clase
    TarjLiqVO.
    '''

    def update_banco(self):
        """
        Modifica los datos del registro.

        @param TarjLiqVO: opera_banco, marca_banco, fecha_banco.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valor = (self.get_marca_banco(), self.get_fecha_banco(),
                self.get_opera_banco(), self.get_id_usuario_act(),
                self.get_fecha_act(), self.get_id())
        query = ("UPDATE tarj_liquidaciones SET marca_banco=%s, fecha_banco=%s, "
                "opera_banco=%s, id_usuario_act=%s, fecha_act=%s WHERE id=%s")
        cursor.execute(query, valor)
        self.ultimo_id = cursor.lastrowid
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()

    def find_liquidacion(self):
        """
        Obtiene un registro activo por el número de liquidación e id del
        producto.

        @param liquidacion: TarjLiqVO.
        @param estado: 1 - activo.
        @return: TarjLiqVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_liquidaciones WHERE liquidacion = %s "
                    "AND estado = 1")
        valor = (self.get_liquidacion(), )
        cursor.execute(consulta, valor)
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_liquidacion(dato[1])
            self.set_id_producto(dato[2])
            self.set_id_operador(dato[3])
            self.set_fecha_pago(dato[4])
            self.set_banco_suc(dato[5])
            self.set_moneda(dato[6])
            self.set_importe_bruto(dato[7])
            self.set_importe_desc(dato[8])
            self.set_importe_neto(dato[9])
            self.set_cupones(dato[10])
            self.set_cupones(dato[11])
            self.set_fecha_proceso(dato[12])
            self.set_marca_banco(dato[13])
            self.set_fecha_banco(dato[14])
            self.set_opera_banco(dato[15])
            self.set_arancel(dato[16])
            self.set_costo_financiero(dato[17])
            self.set_otros_deb(dato[18])
            self.set_iva_arancel(dato[19])
            self.set_iva_costo_financiero(dato[20])
            self.set_iva_otros_deb(dato[21])
            self.set_impuesto_debcred(dato[22])
            self.set_impuesto_interes(dato[23])
            self.set_retencion_iva(dato[24])
            self.set_retencion_imp_gan(dato[25])
            self.set_retencion_ing_brutos(dato[26])
            self.set_percepcion_iva(dato[27])
            self.set_percepcion_ing_brutos(dato[28])
            self.set_estado(dato[29])
            self.set_id_usuario_act(dato[30])
            self.set_fecha_act(dato[31])
            return dato
        else:
            return None

    def find_liquidacion_fecha(self):
        """
        Obtiene un registro activo por el número de liquidación.

        @param liquidacion: TarjLiqVO.
        @param fecha_pago: TarjLiqVO
        @param estado: 1 - activo.
        @return: TarjLiqVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_liquidaciones WHERE liquidacion = %s "
                    "AND fecha_pago = %s AND estado = 1")
        valor = (self.get_liquidacion(), self.get_fecha_pago(),)
        cursor.execute(consulta, valor)
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_liquidacion(dato[1])
            self.set_id_producto(dato[2])
            self.set_id_operador(dato[3])
            self.set_fecha_pago(dato[4])
            self.set_banco_suc(dato[5])
            self.set_moneda(dato[6])
            self.set_importe_bruto(dato[7])
            self.set_importe_desc(dato[8])
            self.set_importe_neto(dato[9])
            self.set_cupones(dato[10])
            self.set_cupones(dato[11])
            self.set_fecha_proceso(dato[12])
            self.set_marca_banco(dato[13])
            self.set_fecha_banco(dato[14])
            self.set_opera_banco(dato[15])
            self.set_arancel(dato[16])
            self.set_costo_financiero(dato[17])
            self.set_otros_deb(dato[18])
            self.set_iva_arancel(dato[19])
            self.set_iva_costo_financiero(dato[20])
            self.set_iva_otros_deb(dato[21])
            self.set_impuesto_debcred(dato[22])
            self.set_impuesto_interes(dato[23])
            self.set_retencion_iva(dato[24])
            self.set_retencion_imp_gan(dato[25])
            self.set_retencion_ing_brutos(dato[26])
            self.set_percepcion_iva(dato[27])
            self.set_percepcion_ing_brutos(dato[28])
            self.set_estado(dato[29])
            self.set_id_usuario_act(dato[30])
            self.set_fecha_act(dato[31])
            return dato
        else:
            return None

    def find_importe_fecha(self):
        """
        Obtiene un registro activo por el importe neto y fecha de pago.

        @param importe_neto: TarjLiqVO.
        @param fecha_pago: TarjLiqVO
        @param estado: 1 - activo.
        @return: TarjLiqVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_liquidaciones WHERE importe_neto = %s "
                    "AND fecha_pago = %s AND estado = 1")
        valor = (self.get_importe_neto(), self.get_fecha_pago(),)
        cursor.execute(consulta, valor)
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_liquidacion(dato[1])
            self.set_id_producto(dato[2])
            self.set_id_operador(dato[3])
            self.set_fecha_pago(dato[4])
            self.set_banco_suc(dato[5])
            self.set_moneda(dato[6])
            self.set_importe_bruto(dato[7])
            self.set_importe_desc(dato[8])
            self.set_importe_neto(dato[9])
            self.set_cupones(dato[10])
            self.set_cupones(dato[11])
            self.set_fecha_proceso(dato[12])
            self.set_marca_banco(dato[13])
            self.set_fecha_banco(dato[14])
            self.set_opera_banco(dato[15])
            self.set_arancel(dato[16])
            self.set_costo_financiero(dato[17])
            self.set_otros_deb(dato[18])
            self.set_iva_arancel(dato[19])
            self.set_iva_costo_financiero(dato[20])
            self.set_iva_otros_deb(dato[21])
            self.set_impuesto_debcred(dato[22])
            self.set_impuesto_interes(dato[23])
            self.set_retencion_iva(dato[24])
            self.set_retencion_imp_gan(dato[25])
            self.set_retencion_ing_brutos(dato[26])
            self.set_percepcion_iva(dato[27])
            self.set_percepcion_ing_brutos(dato[28])
            self.set_estado(dato[29])
            self.set_id_usuario_act(dato[30])
            self.set_fecha_act(dato[31])
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
        consulta = ("SELECT * FROM tarj_liquidaciones WHERE estado = 1")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha(self):
        """
        Obtiene todos los registros activos de una fecha de pago.

        @param fecha: TarjLiqVO.
        @param estado: 1 - activo.
        @return: datos para construir el diccionario.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_liquidaciones WHERE fecha_pago=%s AND "
                    "estado = 1")
        valor = (self.get_fecha_pago(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_dic(self):
        """
        Obtiene todos los registros activos desde una fecha de pago.

        @param fecha_pago: TarjLiqVO.
        @param estado: 1 = activo.
        @return: datos para construir el diccionario que se utiliza en agregar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, liquidacion, fecha_pago FROM tarj_liquidaciones"
                    " WHERE fecha_pago >= %s AND estado=1")
        valor = (self.get_fecha_pago(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_pendientes(self):
        """
        Obtiene todos los registros activos pendientes desde una fecha de pago.

        @param fecha_pago: TarjLiqVO.
        @param estado: 1 = activo.
        @return: datos que se utilizan para armar el inventario de cupones
                pendientes de pago, ordenados por fecha y liquidación.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, liquidacion, id_producto, fecha_pago "
                    "FROM tarj_liquidaciones "
                    "WHERE fecha_pago > %s AND estado=1 "
                    "ORDER BY fecha_pago, liquidacion")
        valor = (self.get_fecha_pago(),)
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
        según el rango y tipo de fechas seleccionado, ordenados por liquidación.
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.
        @param tipo: si es la fecha de pago o proceso.
        @return: datos
        """

        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, liquidacion, fecha_proceso, fecha_pago, "
                    "id_producto, importe_bruto, importe_desc, importe_neto, "
                    "cupones, marca_cupones, marca_banco, fecha_banco, "
                    "opera_banco FROM tarj_liquidaciones WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_proceso >= %s AND fecha_proceso <= %s "
                        "AND estado=1 ORDER BY liquidacion, fecha_proceso")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_pago >= %s AND fecha_pago <= %s "
                        "AND estado=1 ORDER BY liquidacion, fecha_pago")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_conciliar(self, opciones):
        """
        Obtiene los registros activos para conciliar.

        Obtiene los registros activos de la tabla para conciliar con cupones
        según el rango y tipo de fechas seleccionado, ordenados por liquidación.
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.
        @param tipo: si es la fecha de pago o proceso.
        @param marca_cupones: 0 - sin verif y 2 - con diferencia
        @return: datos
        """

        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, liquidacion, fecha_proceso, fecha_pago, "
                    "id_producto, importe_bruto, importe_desc, importe_neto, "
                    "cupones, marca_cupones, marca_banco, fecha_banco, "
                    "opera_banco FROM tarj_liquidaciones WHERE "
                    "(marca_cupones = 0 OR marca_cupones = 2) AND ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_proceso >= %s AND fecha_proceso <= %s "
                        "AND estado=1 ORDER BY liquidacion, fecha_proceso")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_pago >= %s AND fecha_pago <= %s "
                        "AND estado=1 ORDER BY liquidacion, fecha_pago")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
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
        obligatorios), ordenados por liquidación y fecha.
        @param fecha_d: fecha desde donde comienza la consulta (oblig.).
        @param fecha_h: fecha máxima de la consulta (oblig.).
        @param tipo: tipo de fecha (operación o presentación) (oblig.).
        @param liquidacion: número de liquidación que se busca, valor 0 = todos.
        @param id_producto: id de producto que se busca, valor 0 = todos.
        @param marca_cup: marca de cupones que se busca, valor 9 = todos.
        @param banco_cup: marca de acred. banco que se busca, valor 9 = todos.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valores = []
        valores.append(opciones['fecha_d'])
        valores.append(opciones['fecha_h'])
        consulta = ("SELECT id, liquidacion, fecha_proceso, fecha_pago, "
                    "id_producto, importe_bruto, importe_desc, importe_neto, "
                    "cupones, marca_cupones, marca_banco, fecha_banco, "
                    "opera_banco FROM tarj_liquidaciones WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_proceso >= %s AND fecha_proceso <= %s ")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_pago >= %s AND fecha_pago <= %s ")
        if int(opciones['liquidacion']) > 0:
            consulta += (" AND liquidacion = %s")
            valores.append(int(opciones['liquidacion']))
        if int(opciones['id_producto']) > 0:
            consulta += (" AND id_producto = %s")
            valores.append(opciones['id_producto'])
        if int(opciones['marca_cupones']) != 9:
            consulta += (" AND marca_cupones = %s")
            valores.append(opciones['marca_cupones'])
        if int(opciones['marca_banco']) != 9:
            consulta += (" AND marca_banco = %s")
            valores.append(opciones['marca_banco'])
        if int(opciones['tipo'])==1:
            consulta += (" AND estado=1 ORDER BY liquidacion, fecha_proceso")
        if int(opciones['tipo'])==2:
            consulta += (" AND estado=1 ORDER BY liquidacion, fecha_pago")
        valor = tuple(valores)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_resumen(self, opciones):
        """
        Obtiene los registros de la busqueda para armar resumen impositivo.

        Obtiene los registros buscados de la tabla para armar resumen impositivo
        según período y operador (obligatorios) ordenados por producto.
        @param fecha_d: fecha desde donde comienza la consulta (oblig.).
        @param fecha_h: fecha máxima de la consulta (oblig.).
        @param id_operador: id del operador que se busca (oblig.).
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_liquidaciones WHERE "
                    "fecha_pago >= %s AND fecha_pago <= %s "
                    "AND id_operador = %s AND estado = 1 ORDER BY id_producto")
        valor = (opciones['fecha_d'], opciones['fecha_h'], opciones['id_operador'],)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
