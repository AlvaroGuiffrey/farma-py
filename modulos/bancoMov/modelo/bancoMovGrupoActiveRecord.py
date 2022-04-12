# -*- coding: utf-8 -*-
#
# bancoMovGrupoActiveRecord.py
#
# Creado: 06/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.bancoMov.modelo.bancoMovGrupoVO import BancoMovGrupoVO


class BancoMovGrupoActiveRecord(BancoMovGrupoVO):
    '''
    Clase que implementa el patrón Active Record en la tabla banco_mov_grupo.

    Permite realizar operaciones del tipo CRUD sobre la tabla banco_mov_grupo de
    la base de datos farma-py en mysql; hereda los atributos y métodos de la
    clase BancoMovGrupoVO; y La conexión a la base de datos se realiza por una
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

        @param id: índice de la tabla desde bancoMovGrupoVO.
        @return: bancoMovGrupoVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM banco_mov_grupo WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_nombre(dato[1])
            self.set_orden(dato[2])
            self.set_estado(dato[3])
            self.set_id_usuario_act(dato[4])
            self.set_fecha_act(dato[5])
            return dato
        else:
            return None

    def insert(self):
        """
        Agrega un registro a la tabla.

        @param bancoMovGrupoVO: con los datos a insertar en el nuevo registro.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valor = (self.get_nombre(), self.get_orden(), self.get_estado(),
                self.get_id_usuario_act(), self.get_fecha_act())
        query = ("INSERT INTO banco_mov_grupo (nombre, orden, "
                "estado, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query, valor)
        self.ultimo_id = cursor.lastrowid
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()

    def update(self):
        """
        Modifica los datos del registro.

        @param bancoMovGrupoVO: datos varios.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE banco_mov_grupo SET nombre=%s, orden=%s, "
                "estado=%s, id_usuario_act=%s, fecha_act=%s WHERE id=%s")
        valor = (self.get_nombre(), self.get_orden(), self.get_estado(),
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
        consulta = ("SELECT COUNT(*) FROM banco_mov_grupo")
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
