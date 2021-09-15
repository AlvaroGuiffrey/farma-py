# -*- coding: utf-8 -*-
#
# tarjLiqActiveRecord.py
#
# Creado: 13/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.tarjLiquidacion.modelo.tarjLiqVO import TarjLiqVO


class TarjLiqActiveRecord(TarjLiqVO):
    '''
    Clase que implementa el patrón Active Record en la tabla tarj_liquidaciones.

    Permite realizar operaciones del tipo CRUD sobre la tabla tarj_liquidaciones
    de la base de datos farma-py en mysql; hereda los atributos y métodos de
    la clase TarjLiqVO; y La conexión a la base de datos se realiza por una
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

        @param id: índice de la tabla desde TarjLiqVO.
        @return: TarjLiqVO con los datos del renglón.
        @return: por el método get_cantidad() se obtiene la cantidad de filas
                afectadas.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        consulta = ("SELECT * FROM tarj_liquidaciones WHERE id = %s")
        cursor.execute(consulta, (self.get_id(),))
        dato = cursor.fetchone()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()
        if self.cantidad == 1:
            self.set_id(dato[0])
            self.set_liquidacion(dato[1])
            self.set_fecha_pago(dato[2])
            self.set_ban_suc(dato[3])
            self.set_moneda(dato[4])
            self.set_importe_bruto(dato[5])
            self.set_importe_desc(dato[6])
            self.set_importe_neto(dato[7])
            self.set_cupones(dato[8])
            self.set_fecha_proceso(dato[9])
            self.set_marca_banco(dato[10])
            self.set_fecha_banco(dato[11])
            self.set_opera_banco(dato[12])
            self.set_arancel(dato[13])
            self.set_costo_financiero(dato[14])
            self.set_iva_arancel(dato[15])
            self.set_iva_costo_financiero(dato[16])
            self.set_impuesto_debcred(dato[17])
            self.set_impuesto_interes(dato[18])
            self.set_retencion_iva(dato[19])
            self.set_retencion_imp_gan(dato[20])
            self.set_retencion_ing_brutos(dato[21])
            self.set_percepcion_iva(dato[22])
            self.set_percepcion_ing_brutos(dato[23])
            self.set_estado(dato[24])
            self.set_id_usuario_act(dato[25])
            self.set_fecha_act(dato[26])
            return dato
        else:
            return None
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def insert(self):
        """
        Agrega un registro a la tabla.

        @param TarjliqVO: con los datos a insertar en el nuevo registro.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        valor = (self.get_cupon(), self.get_fecha(), self.get_numero(),
                self.get_id_producto(), self.get_moneda(), self.get_importe(),
                self.get_descuento(), self.get_neto(), self.get_cuota(),
                self.get_autorizacion(), self.get_error(),
                self.get_comentario(), self.get_fecha_presentacion(),
                self.get_lote(), self.get_liquidacion(), self.get_estado(),
                self.get_id_usuario_act(), self.get_fecha_act())
        query = ("INSERT INTO tarj_cupones (cupon, fecha, numero, id_producto, "
                "moneda, importe, descuento, neto, cuota, autorizacion, "
                "error, comentario, fecha_pre, lote, liquidacion, "
                "estado, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s)")

        cursor.execute(query, valor)
        self.ultimo_id = cursor.lastrowid
        ccnx.commit()
        self.cantidad = cursor.rowcount
        cursor.close()
        ccnx.close()

    def update(self):
        """
        Modifica los datos del registro.

        @param TarjCuponVO: datos varios.
        """
        ccnx = ConexionMySQL().conectar()
        cursor = ccnx.cursor()
        query = ("UPDATE tarj_cupones SET cupon=%s, fecha=%s, numero=%s,"
                "id_producto=%s, moneda=%s, importe=%s, descuento=%s, neto=%s,"
                "cuota=%s, autorizacion=%s, error=%s, comentario=%s,"
                "fecha_pre=%s, lote=%s, liquidacion=%s, estado=%s,"
                "id_usuario_act=%s, fecha_act=%s WHERE id=%s")
        valor = (self.get_cupon(), self.get_fecha(), self.get_numero(),
                 self.get_id_producto(), self.get_moneda(), self.get_importe(),
                 self.get_descuento(), self.get_neto(), self.get_cuota(),
                 self.get_autorizacion(), self.get_error(),
                 self.get_comentario(), self.get_fecha_presentacion(),
                 self.get_lote(), self.get_liquidacion(), self.get_estado(),
                 self.get_id_usuario_act(), self.get_fecha_act(),
                 self.get_id())
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
        consulta = ("SELECT COUNT(*) FROM tarj_cupones")
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
