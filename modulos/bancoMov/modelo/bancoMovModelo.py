# -*- coding: utf-8 -*-
#
# bancoMovModelo.py
#
# Creado: 30/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.bancoMov.modelo.bancoMovActiveRecord import BancoMovActiveRecord

class BancoMovModelo(BancoMovActiveRecord):
    '''
    Clase para realizar operaciones en la tabla banco_mov.

    Realiza operaciones varias de consultas sobre la tabla banco_mov
    de la base de datos farma-py; hereda todos los métodos CRUD de la clase
    BancoMovActiveRecord; y los atributos y métodos de la clase
    BancoMovVO.
    '''

    def find_numero(self):
        """
        Obtiene un registro activo por el numero del movimiento.

        @param numero: BancoMovVO.
        @param estado: 1 - activo.
        @return: BancoMovVO y datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM banco_mov WHERE numero = %s "
                    "AND estado = 1")
        valor = (self.get_numero(),)
        cursor.execute(consulta, valor)
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_fecha_mov(dato[1])
            self.set_fecha_valor(dato[2])
            self.set_importe(dato[3])
            self.set_numero(dato[4])
            self.set_concepto(dato[5])
            self.set_id_grupo(dato[6])
            self.set_marca(dato[7])
            self.set_comentario(dato[8])
            self.set_estado(dato[9])
            self.set_id_usuario_act(dato[10])
            self.set_fecha_act(dato[11])
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
        consulta = ("SELECT * FROM banco_mov WHERE estado = 1")
        cursor.execute(consulta)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_mov(self):
        """
        Obtiene todos los registros activos de una fecha de movimiento.

        @param fecha_mov: BancoMovVO.
        @param estado: 1 - activo.
        @return: datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM banco_mov WHERE fecha_mov=%s "
                    "AND estado = 1")
        valor = (self.get_fecha_mov(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_valor(self):
        """
        Obtiene todos los registros activos de una fecha valor.

        @param fecha_valor: BancoMovVO.
        @param estado: 1 - activo.
        @return: datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM banco_mov WHERE fecha_valor=%s "
                    "AND estado = 1")
        valor = (self.get_fecha_valor(),)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_fecha_dic(self):
        """
        Obtiene todos los registros activos desde una fecha de movimiento.

        @return: datos para construir el diccionario que se utiliza en agregar.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT fecha_mov, fecha_valor, importe, numero, concepto "
                    "FROM banco_mov WHERE fecha_mov >= %s AND estado=1")
        valor = (self.get_fecha_mov(),)
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
        @param tipo: si es la fecha de movimiento o valor.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, fecha_mov, fecha_valor, importe, numero, "
                    "concepto, id_grupo, marca, comentario "
                    "FROM banco_mov WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_mov >= %s AND fecha_mov <= %s "
                        "AND estado=1 ORDER BY fecha_mov, numero")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_valor >= %s AND fecha_valor <= %s "
                        "AND estado=1 ORDER BY fecha_valor, numero")
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
        obligatorios), ordenados por numero y fecha.
        @param fecha_d: fecha desde donde comienza la consulta (oblig.).
        @param fecha_h: fecha máxima de la consulta (oblig.).
        @param tipo: tipo de fecha (movimiento o valor) (oblig.).
        @param numero: número de referencia que se busca, valor 0 = todos.
        @param id_grupo: id de grupo que se busca, valor 0 = todos.
        @param marca: marca de conciliación que se busca, valor 9 = todos.
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valores = []
        valores.append(opciones['fecha_d'])
        valores.append(opciones['fecha_h'])
        consulta = ("SELECT id, fecha_mov, fecha_valor, importe, numero, "
                    "concepto, id_grupo, marca, comentario "
                    "FROM banco_mov WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_mov >= %s AND fecha_mov <= %s ")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_valor >= %s AND fecha_valor <= %s ")
        if int(opciones['numero']) > 0:
            numero = str(opciones['numero'])
            consulta += (" AND numero = %s")
            valores.append(numero.zfill(13))
        if int(opciones['grupo']) > 0:
            consulta += (" AND id_grupo = %s")
            valores.append(opciones['grupo'])
        if int(opciones['marca']) != 9:
            consulta += (" AND marca = %s")
            valores.append(opciones['marca'])
        if int(opciones['tipo'])==1:
            consulta += (" AND estado=1 ORDER BY fecha_mov, numero")
        if int(opciones['tipo'])==2:
            consulta += (" AND estado=1 ORDER BY fecha_valor, numero")
        valor = tuple(valores)
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_conciliar(self, opciones):
        """
        Obtiene los registros activos para conciliar.

        Obtiene los registros activos de la tabla para conciliar
        según el rango y tipo de fechas seleccionado.
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.
        @param tipo: si es la fecha de movimiento o valor.
        @param marca: 0
        @param estado: 1
        @return: datos
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, fecha_mov, fecha_valor, importe, numero, "
                    "concepto "
                    "FROM banco_mov WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_mov >= %s AND fecha_mov <= %s "
                        "AND marca=0 AND estado=1")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_valor >= %s AND fecha_valor <= %s "
                        "AND marca=0 AND estado=1")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos

    def find_all_sin_agrupar(self, opciones):
        """
        Obtiene los registros activos sin agrupar.

        Obtiene los registros activos de la tabla sin grupo asignado
        según el rango y tipo de fechas seleccionado, ordenado por numero.
        @param fecha_d: fecha desde donde comienza la consulta.
        @param fecha_h: fecha máxima de la consulta.
        @param tipo: si es la fecha de movimiento o valor.
        @param id_grupo: 0 sin grupo.
        @return: datos.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT id, fecha_mov, fecha_valor, importe, numero, "
                    "concepto, id_grupo, marca, comentario "
                    "FROM banco_mov WHERE ")
        if int(opciones['tipo'])==1:
            consulta += ("fecha_mov >= %s AND fecha_mov <= %s "
                        "AND id_grupo=0 AND estado=1 "
                        "ORDER BY fecha_mov, numero")
        if int(opciones['tipo'])==2:
            consulta += ("fecha_valor >= %s AND fecha_valor <= %s "
                        "AND id_grupo=0 AND estado=1 "
                        "ORDER BY fecha_valor, numero")
        valor = (opciones['fecha_d'], opciones['fecha_h'])
        cursor.execute(consulta, valor)
        datos = cursor.fetchall()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        return datos
