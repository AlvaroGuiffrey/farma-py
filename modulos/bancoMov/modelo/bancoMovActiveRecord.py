# -*- coding: utf-8 -*-
#
# bancoMovActiveRecord.py
#
# Creado: 30/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.bancoMov.modelo.bancoMovVO import BancoMovVO


class BancoMovActiveRecord(BancoMovVO):
    '''
    Clase que implementa el patrón Active Record en la tabla banco_mov.

    Permite realizar operaciones del tipo CRUD sobre la tabla banco_mov de
    la base de datos farma-py en mysql; hereda los atributos y métodos de la
    clase BancoMovVO; y La conexión a la base de datos se realiza por una
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

        @param id: índice de la tabla desde bancoMovVO.
        @return: bancoMovVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM banco_mov WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
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

    def insert(self):
        """
        Agrega un registro a la tabla.

        @param bancoMovVO: con los datos a insertar en el nuevo registro.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valor = (self.get_fecha_mov(), self.get_fecha_valor(),
                self.get_importe(), self.get_numero(), self.get_concepto(),
                self.get_id_grupo(), self.get_marca(), self.get_comentario(),
                self.get_estado(), self.get_id_usuario_act(),
                self.get_fecha_act())
        query = ("INSERT INTO banco_mov (fecha_mov, fecha_valor, importe, "
                "numero, concepto, id_grupo, marca, comentario, "
                "estado, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, valor)
        self.ultimo_id = cursor.lastrowid
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()

    def update(self):
        """
        Modifica los datos del registro.

        @param bancoMovVO: datos varios.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE banco_mov SET fecha_mov=%s, fecha_valor=%s, "
                "importe=%s, numero=%s, concepto=%s, id_grupo=%s, marca=%s, "
                "comentario=%s, estado=%s, id_usuario_act=%s, "
                "fecha_act=%s WHERE id=%s")
        valor = (self.get_fecha_mov(), self.get_fecha_valor(),
                self.get_importe(), self.get_numero(),
                self.get_concepto(), self.get_id_grupo(), self.get_marca(),
                self.get_comentario(), self.get_estado(),
                self.get_id_usuario_act(), self.get_fecha_act(), self.get_id())
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
        consulta = ("SELECT COUNT(*) FROM banco_mov")
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
