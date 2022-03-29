# -*- coding: latin-1 -*-
#
# tarjCuponControl.py
#
# Creado: 02/09/2021
# Versión: 001
# Modificaciones a la versión:
# Date: 10/03/2022
# Modificaciones para tomar débitos de terceros (QR - Debin PCT)
#
# Copyright 2021 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import os
import socket
import cgi
import csv
from datetime import date
from datetime import datetime
from builtins import int
from decimal import Decimal
# Módulos de la aplicación:
from includes.control.motorVista import MotorVista
from modulos.tarjeta.modelo.tarjProductoModelo import TarjProductoModelo
from modulos.tarjLiquidacion.modelo.tarjLiqModelo import TarjLiqModelo
from modulos.tarjCupon.modelo.tarjCuponModelo import TarjCuponModelo
from modulos.tarjLiquidacion.includes.tarjLiqTabla import TarjLiqTabla
from includes.includes.select import Select

class TarjLiqControl():
    """
    Clase control del módulo tarjLiquidacion.

    Realiza operaciones con liquidaciones de tarjetas a cobrar
    por ventas realizadas, utilizando el patron MVC.
    """
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia las clases del modelo:
        self.tarj_liq = TarjLiqModelo()
        self.tarj_cupon = TarjCuponModelo()
        self.tarj_producto = TarjProductoModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Busca todos los archivos del directorio tarjetas:
        self.directorio = os.getcwd() + "/archivos/tarjetas/"
        self.archivos = os.listdir(self.directorio)
        self.archNoActualiza = ["Ventas.csv", "tarjResImp.pdf", ]
        self.archivos_txt = [item for item in self.archivos
                            if item not in self.archNoActualiza]
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'tarjLiquidacion'
        self.form = ''
        self.archivo = ''
        self.datos_pg = {}
        self.alertas = []
        self.opciones = []
        self.contenidos = []
        self.tablas = []
        self.componentes = []
        self.botones_ac = []
        self.botones_ev = []
        self.botones_aux = []
        self.accion = ''
        self.texto_alerta_cupon = str()
        self.texto_alerta_liquidacion = str()
        self.cant_liquidaciones = int(0)
        self.cant_cupones = int(0)
        self.cant_debitos = int(0)
        self.cant_cupones_liq = int(0)
        self.cant_agregados = int(0)
        self.cant_actualizados = int(0)
        self.cant_cargados = int(0)
        self.cant_repetidos = int(0)
        self.cant_faltantes = int(0)
        self.cant_productos = int(0)
        self.cant_conciliados = int(0)
        self.cant_sin_conciliar = int(0)
        self.cant_con_diferencias = int(0)
        self.retencion_iva = float(0)
        self.retencion_imp_gan = float(0)
        self.retencion_ing_brutos = float(0)
        self.linea = []
        # Consulta tablas que se utilizan en el módulo:
        self.tarj_productos = self.tarj_producto.find_all()
        self.cant_productos = self.tarj_producto.get_cantidad()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.tarj_productos_dicc = {reng[1]: reng[0] for reng in
                               self.tarj_productos}
        self.tarj_productos_codigo_dicc = {reng[3]: reng[0] for reng in
                               self.tarj_productos}
        self.tarj_productos_operador_dicc = {reng[3]: reng[4] for reng in
                               self.tarj_productos}
        self.tarj_productos_listar_dicc = {reng[0]: (reng[1], reng[2], reng[4])
                            for reng in self.tarj_productos}
        self.tarj_productos_buscar_dicc = {reng[0]: reng[1] for reng in
                                 self.tarj_productos}
    # Métodos:
    def inicio(self, accion):
        """
        Inicio de la clase control.

        Verifica el login del usuario y nos envía al método que ejecuta las
        acciones del módulo.
        """
        self.accion = accion
        self.accion_control()

    def accion_control(self):
        """
        Ejecuta las acciones del módulo.

        Ejecuta las acciones de acuerdo a las opciones seleccionadas con los
        botones de la vista.
        """
        # Recibe los datos enviados del formulario por metodo POST:
        self.form = cgi.FieldStorage()
        # Vacía diccionario y listas que escriben datos en la vista:
        self.datos_pg.clear()
        self.alertas.clear()
        self.opciones.clear()
        self.contenidos.clear()
        self.tablas.clear()
        self.botones_ac.clear()
        self.botones_ev.clear()
        self.botones_aux.clear()
        # Agrega datos del IP para el menú de la página:
        self.datos_pg['ip'] = self.ip
        # Agrega datos para titulos y usuario de la página:
        self.datos_pg['tituloPagina'] = "Tarjetas"
        self.datos_pg['usuario'] = "Alvaro"
        self.datos_pg['tituloBadge'] = "Liquidaciones"
        # Obtiene la cantidad de registros de la tabla para badge:
        self.tarj_liq.count()
        self.datos_pg['cantidad'] = self.tarj_liq.get_cantidad()
        #self.datos_pg['cantidad'] = 0
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar", "botonAgregar",
                          "botonListar", "botonBuscar",
                          "botonConciliarCupon"]
        # Selecciona las acciones:
        if "bt_agregar" in self.form: self.accion = "Agregar"
        elif "bt_conf_agregar" in self.form: self.accion = "ConfAgregar"
        elif "bt_cargar" in self.form: self.accion = "Cargar"
        elif "bt_conf_cargar" in self.form: self.accion = "ConfCargar"
        elif "bt_listar" in self.form: self.accion = "Listar"
        elif "bt_conf_listar" in self.form: self.accion = "ConfListar"
        elif "bt_buscar" in self.form: self.accion = "Buscar"
        elif "bt_conf_buscar" in self.form: self.accion = "ConfBuscar"
        elif "bt_conciliar" in self.form: self.accion = "Conciliar"
        elif "bt_conf_conciliar" in self.form: self.accion = "ConfConciliar"
        elif "bt_descargar_pdf" in self.form: self.accion = "DescargarPDF"
        elif "bt_editar" in self.form: self.accion = "Editar"
        elif "bt_descartar" in self.form: self.accion = "Descartar"
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_agregados = self.cant_cargados = self.cant_repetidos = 0
        self.cant_liquidaciones = self.cant_actualizados = 0
        self.cant_cupones = self.cant_cupones_liq = self.cant_faltantes = 0

        # Acción para iniciar:
        if self.accion == "Iniciar":
            #print("llegue aca<br>")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tabla de Tarjetas - Liquidaciones")
            self.datos_pg['info'] = ("Permite realizar acciones en la tabla"
                        " seleccionando con los botones.")
            # Agrega las alertas:
            self.alertas.append("alertaInfo")
            self.datos_pg["alertaInfo"] = ("Seleccione una acción con los"
                        " <b>BOTONES</b>.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para cargar:
        if self.accion == "Cargar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Liquidaciones de Tarjetas")
            self.datos_pg['info'] = ("Carga liquidaciones de tarjetas en la"
                                     " tabla desde los <b>archivos txt</b> "
                                     " descargados de -Liquidación Electrónica- "
                                     " de FISERV. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Agrega las alertas:
            self.alertas.append("alertaAdvertencia")
            self.datos_pg["alertaAdvertencia"] = ("Carga liquidaciones de "
                        "tarjetas desde los archivos <b>txt"
                        "</b> -Liquidaciones Electrónicas-. Confirme el "
                        "evento.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfCargar",]
            # Carga cantidad de archivos txt de liquidaciones:
            cant_archivos = len(self.archivos_txt)
            # Verifica si existe el txt:
            if cant_archivos > 0:
                self.contenidos.append("cargarDatos")
                self.datos_pg["cantArchivos"] = cant_archivos
                self.datos_pg["cantLiquidaciones"] = 0
                self.datos_pg["cantCargados"] = 0
                self.datos_pg["cantRepetidos"] = 0
                self.datos_pg["cantAgregados"] = 0
                self.datos_pg["cantCupones"] = 0
                self.datos_pg["cantOtrosDeb"] = 0
                self.datos_pg["cantActualizados"] = 0
                self.datos_pg["cantFaltantes"] = 0
            else:
                # ---- txt vacio ---- :
                # Agrega las alertas:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay archivos de  "
                    "Liquidaciones Electrónicas. <b>VERIFICAR !!!</b>.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar cargar:
        if self.accion == "ConfCargar":
            # Recibe datos por POST:
            cant_archivos = self.form.getvalue("cant_archivos")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Liquidaciones de Tarjetas")
            self.datos_pg['info'] = ("Carga liquidaciones de tarjetas en la"
                                    " tabla desde los <b>archivos txt</b> "
                                    " descargados de -Liquidación Electrónica- "
                                    " de FISERV. "
                                    "Puede seleccionar otras acciones con los"
                                    " botones.")
            # Pone en blanco textos de mensajes
            self.texto_alerta_cupon = self.texto_alerta_liquidacion = ""
            self.cant_repetidos = self.cant_faltantes = self.cant_cargados = 0
            # Recorre los archivos que actualizan
            for liq in self.archivos_txt:
                self.archivo = self.directorio + liq
                # Abre el archivo
                txtfile = open(self.archivo, "r")
                arch = txtfile.readlines()
                # Extrae los datos del archivo txt
                for dato in arch:
                    # Carga datos si es renglón 1 del archivo TXT
                    if int(dato[0]) == 1:
                        fecha_proceso = self.fecha_db(str(dato[24:32]))
                        flag = "" # Pone en blanco la bandera al inicio del TXT
                        #print("Fecha: "+str(fecha_proceso)+"<br>")
                    # Carga datos si es renglón 2 del archivo TXT
                    if int(dato[0]) == 2:
                        self.tarj_liq.set_marca_cupones(int(0))
                        self.cant_cupones_liq = 0
                        self.cant_liquidaciones += 1 # Acumula todas las liq.
                        self.tarj_liq.set_liquidacion(int(dato[54:61]))
                        # Verifica si existe la liquidación y cambia flag
                        self.tarj_liq.find_liquidacion()
                        if self.tarj_liq.get_cantidad() == 1:
                            flag = ""
                            self.cant_repetidos += 1 # Suma Liq. repedidas
                        else:
                            flag = "S"
                            # Carga el índice del producto
                            if dato[15] in self.tarj_productos_codigo_dicc:
                                id_producto = \
                                    self.tarj_productos_codigo_dicc[dato[15]]
                            else:
                                id_producto = 0
                            # Carga el índice del operador
                            if dato[15] in self.tarj_productos_operador_dicc:
                                id_operador = \
                                    self.tarj_productos_operador_dicc[dato[15]]
                            else:
                                id_operador = 0
                            self.tarj_liq.set_id_producto(id_producto)
                            self.tarj_liq.set_id_operador(id_operador)
                            fecha_pago = self.fecha_db(str(dato[32:40]))
                            self.tarj_liq.set_fecha_pago(self.fecha_db(
                                                        str(dato[32:40])))
                            self.tarj_liq.set_banco_suc(str(dato[48:54]))
                            self.tarj_liq.set_moneda(str(dato[16:19]))
                            self.tarj_liq.set_fecha_proceso(fecha_proceso)
                            self.tarj_liq.set_marca_banco(int(0))
                            self.tarj_liq.set_fecha_banco(self.fecha_db(
                                                        str(dato[32:40])))
                            self.tarj_liq.set_opera_banco(int(0))
                            self.tarj_liq.set_otros_deb(0)
                            self.tarj_liq.set_iva_otros_deb(0)
                            self.retencion_iva = float(0)
                            self.retencion_imp_gan = float(0)
                            self.retencion_ing_brutos = float(0)
                    # Carga datos del archivo TXT si es renglón 3 y flag "S"
                    # liquidación no repetida
                    if int(dato[0]) == 3:
                        codigo = int(dato[69:72])
                        #print("Flag -> "+str(flag)+"<br>")
                        #print("Fecha -> "+str(fecha_proceso)+"<br>")
                        #print("Codigo -> "+str(codigo)+"<br>")

                    # Cupón por ventas o cobranza
                    if int(dato[0]) == 3 and int(codigo) == 861:
                        self.cant_cupones += 1
                    if int(dato[0]) == 3 and int(codigo) == 861 and flag == "S":
                        flag_cupon = ""
                        # Busca el cupón para verificar y completar datos
                        #print("cupon -> "+str(dato[94:99])+"<br>")
                        self.tarj_cupon.set_cupon(int(dato[94:99]))
                        self.tarj_cupon.set_fecha(self.fecha_db(
                                                            str(dato[61:69])))
                        self.tarj_cupon.find_cupon_fecha()
                        # Si existe cupón
                        if self.tarj_cupon.get_cantidad() == 1:
                            # Controla y agrega datos al cupón
                            self.cant_cupones_liq += 1
                            importe = self.tarj_cupon.get_importe()
                            # Si descuento en cupón es 0
                            if self.tarj_cupon.get_descuento() == 0:
                                self.tarj_cupon.set_descuento(
                                                self.importe_db(dato[202:211]))
                                flag_cupon = "S"
                            # Si neto en cupón es 0
                            if self.tarj_cupon.get_neto() == 0:
                                neto = float(importe) - float(
                                            self.tarj_cupon.get_descuento())
                                self.tarj_cupon.set_neto(neto)
                                flag_cupon = "S"
                            # Si cambia el error en cupón
                            if int(dato[150:151]) != \
                                int(self.tarj_cupon.get_error()):
                                self.tarj_cupon.set_error(int(dato[150:151]))
                                if int(dato[150:151]) == 1:
                                    self.tarj_cupon.set_comentario("Cod: "
                                        +str(dato[171:174])+"/"
                                        +str(dato[174:177])+"/"
                                        +str(dato[177:180])+"/"
                                        +str(dato[180:183]))
                                flag_cupon = "S"
                            # Si cambia número de liquidación en cupón
                            if self.tarj_liq.get_liquidacion() != \
                                        self.tarj_cupon.get_liquidacion():
                                self.tarj_cupon.set_liquidacion(
                                        self.tarj_liq.get_liquidacion())
                                flag_cupon = "S"
                            # Si flag del cupón es "S" actualiza el registro
                            if flag_cupon == "S":
                                self.actualiza_cupon()
                                flag_cupon = ""
                        # Falta el cupón
                        else:
                            self.texto_alerta_cupon = ("Falta/n cupón/es de "
                                                    " la/s liquidación/es.")
                            self.cant_faltantes += 1

                    # Cargos - Código de movimiento: 892
                    if int(dato[0]) == 3 and int(codigo) == 892 and flag == "S":
                        flag_cupon = ""
                        tipo_op = str(dato[193:195])
                        codigo_cargo = int(dato[196:199])
                        #print("Cod.Cargo--> "+str(codigo_cargo)+"<br>")
                        # Si es Otro Débito
                        # Cargo Cuotas: tipo_op = "CC" y codigo_cargo = 80
                        # Iva Cargo Cuotas: tipo_op = "IC" y codigo_cargo = 81
                        # Cargo Liq.Elect. tipo_op = "LE" y codigo_cargo = 96
                        # Iva Cargo Liq.Elect. tipo_op = "IE" y codigo_cargo = 97
                        if int(codigo_cargo) == 80 or int(codigo_cargo) == 96:
                            self.cant_debitos += 1
                            self.tarj_liq.set_otros_deb(
                                            self.importe_db(dato[103:116])
                                            )
                        elif int(codigo_cargo) == 81 or int(codigo_cargo) == 97:
                            self.tarj_liq.set_iva_otros_deb(
                                            self.importe_db(dato[103:116])
                                            )
                        # Si es Débito por QR - PCT
                        # Retención IVA: codigo_cargo = 454
                        # Retención I.Gan.: codigo_cargo = 455
                        # Nota: códigos sin verificar
                        elif int(codigo_cargo) == 454:
                            self.cant_debitos += 1
                            self.retencion_iva = float(self.retencion_iva) +\
                                        float(self.importe_db(dato[103:116]))

                        elif int(codigo_cargo) == 455:
                            self.cant_debitos += 1
                            self.retencion_imp_gan = \
                                    float(self.retencion_imp_gan) +\
                                    float(self.importe_db(dato[103:116]))

                        else:
                            pass

                    # Carga datos del archivo TXT si es renglón 7 y flag "S"
                    # liquidación no repetida
                    if int(dato[0]) == 7 and flag == "S":
                        #print("LLEGUE AL 7")
                        self.tarj_liq.set_importe_bruto(
                                            self.importe_db(dato[61:74]))
                        gastos = float(self.importe_db(dato[103:116]))
                        impuestos = float(self.importe_db(dato[117:130]))
                        debitos = float(self.importe_db(dato[131:144]))
                        descuento = gastos + impuestos + debitos
                        self.tarj_liq.set_importe_desc(descuento)
                        #print("SIGNO "+str(dato[172]))
                        if int(dato[172]) == 1:
                            self.tarj_liq.set_importe_neto(
                                            self.importe_db(dato[159:172]))
                        else:
                            self.tarj_liq.set_importe_neto(
                                            self.importe_db_n(dato[159:172]))
                        self.tarj_liq.set_cupones(self.cant_cupones_liq)
                        #print("PASE RENGLON 7")
                    # Carga datos del archivo TXT si es renglón 8 y flag "S"
                    # liquidación no repetida
                    if int(dato[0]) == 8 and flag == "S":
                        self.tarj_liq.set_arancel(
                                            self.importe_db(dato[200:211]))
                        self.tarj_liq.set_costo_financiero(
                                            self.importe_db(dato[212:223]))
                        self.tarj_liq.set_iva_arancel(
                                            self.importe_db(dato[63:76]))
                        self.tarj_liq.set_iva_costo_financiero(
                                            self.importe_db(dato[91:104]))
                        self.tarj_liq.set_impuesto_debcred(
                                            self.importe_db(dato[77:90]))
                        self.tarj_liq.set_impuesto_interes(
                                            self.importe_db(dato[190:199]))
                        # RETENCIONES
                        # Suma por si agregó valores en renglones 3
                        self.retencion_iva =\
                                float(self.retencion_iva) +\
                                float(self.importe_db(dato[105:118]))
                        self.tarj_liq.set_retencion_iva(self.retencion_iva)
                        self.retencion_imp_gan =\
                                float(self.retencion_imp_gan) +\
                                float(self.importe_db(dato[133:146]))
                        self.tarj_liq.set_retencion_imp_gan(self.retencion_imp_gan)
                        self.retencion_ing_brutos =\
                                float(self.retencion_ing_brutos) +\
                                float(self.importe_db(dato[147:160]))
                        self.tarj_liq.set_retencion_ing_brutos(
                                            self.retencion_ing_brutos)
                        # PERCEPCIONES
                        self.tarj_liq.set_percepcion_iva(
                                            self.importe_db(dato[119:132]))
                        self.tarj_liq.set_percepcion_ing_brutos(
                                            self.importe_db(dato[161:174]))
                        # Verifica cantidad de cupones de la liquidación
                        if int(self.tarj_liq.get_cupones()) == \
                            int(self.cant_cupones_liq):
                            self.tarj_liq.set_marca_cupones(int(1))
                        else:
                            self.tarj_liq.set_marca_cupones(int(2))
                        # Carga la liquidación a la DB
                        self.carga_liquidacion()
                        flag = ""
                # Cierra el archivo TXT:
                txtfile.close()
            # Agrega las alertas:
            if self.cant_cargados > 0:
                self.alertas.append("alertaSuceso")
                self.datos_pg["alertaSuceso"] = ("Se cargaron registros a la "
                    "tabla con <b>EXITO !!!</b>.")
            if self.cant_repetidos > 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("Algún archivo contiene "
                    "datos ya cargados a la tabla. <b>VERIFICAR !!!</b>.")
            if self.cant_faltantes > 0:
                self.alertas.append("alertaPeligro")
                self.datos_pg["alertaPeligro"] = self.texto_alerta_cupon
            # Arma los datos para la vista:
            self.contenidos.append("cargarDatos")
            self.datos_pg["cantArchivos"] = cant_archivos
            self.datos_pg["cantLiquidaciones"] = self.cant_liquidaciones
            self.datos_pg["cantCargados"] = self.cant_cargados
            self.datos_pg["cantRepetidos"] = self.cant_repetidos
            self.datos_pg["cantAgregados"] = 0
            self.datos_pg["cantCupones"] = self.cant_cupones
            self.datos_pg["cantOtrosDeb"] = self.cant_debitos
            self.datos_pg["cantActualizados"] = self.cant_actualizados
            self.datos_pg["cantFaltantes"] = self.cant_faltantes
            # Muestra la vista:
            self.muestra_vista()
        # Acción para agregar
        if self.accion == "Agregar":
            # Recibe datos por POST:

            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Liquidación de Tarjeta - Agregar")
            self.datos_pg['info'] = ("Permite agregar los datos de un renglón"
                        " del listado en la tabla de la DB.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfAgregar"]
            #Arma los datos para la vista:
            datos = self.tarj_productos_buscar_dicc
            cantidad = self.cant_productos
            nombre = 'producto'
            select_tipo = Select()
            select_tipo.arma_select(datos, cantidad, nombre)
            self.componentes += ["select_producto",]
            self.contenidos = ["agregarDato",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar agregar:
        if self.accion == "ConfAgregar":
            # Recibe datos por POST:
            self.tarj_liq.set_liquidacion(int(self.form.getvalue("liquidacion")))
            self.tarj_liq.set_cupones(int(self.form.getvalue("cupones")))
            self.tarj_liq.set_id_producto(int(self.form.getvalue("producto")))
            self.tarj_liq.set_fecha_pago(str(self.form.getvalue("fecha_pago")))
            self.tarj_liq.set_fecha_banco(str(self.form.getvalue("fecha_pago")))
            self.tarj_liq.set_fecha_proceso(str(self.form.getvalue("fecha_proceso")))
            self.tarj_liq.set_importe_bruto(float(self.form.getvalue("importe_bruto")))
            self.tarj_liq.set_importe_desc(float(self.form.getvalue("importe_desc")))
            self.tarj_liq.set_importe_neto(float(self.form.getvalue("importe_neto")))
            self.tarj_liq.set_arancel(float(self.form.getvalue("arancel")))
            self.tarj_liq.set_costo_financiero(float(self.form.getvalue("costo_financiero")))
            self.tarj_liq.set_otros_deb(float(self.form.getvalue("otros_deb")))
            self.tarj_liq.set_iva_arancel(float(self.form.getvalue("iva_arancel")))
            self.tarj_liq.set_iva_costo_financiero(float(self.form.getvalue("iva_costo_financiero")))
            self.tarj_liq.set_iva_otros_deb(float(self.form.getvalue("iva_otros_deb")))
            self.tarj_liq.set_impuesto_debcred(float(self.form.getvalue("impuesto_debcred")))
            self.tarj_liq.set_impuesto_interes(float(self.form.getvalue("impuesto_interes")))
            self.tarj_liq.set_retencion_iva(float(self.form.getvalue("retencion_iva")))
            self.tarj_liq.set_retencion_imp_gan(float(self.form.getvalue("retencion_imp_gan")))
            self.tarj_liq.set_retencion_ing_brutos(float(self.form.getvalue("retencion_ing_brutos")))
            self.tarj_liq.set_percepcion_iva(float(self.form.getvalue("percepcion_iva")))
            self.tarj_liq.set_percepcion_ing_brutos(float(self.form.getvalue("percepcion_ing_brutos")))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Liquidación de Tarjeta - Ver Agregado")
            self.datos_pg['info'] = ("Permite ver los datos agregados de "
                        "un renglón del listado.")
            # Busca liquidación
            self.tarj_liq.find_liquidacion()
            # Existe la liquidación, arma alerta y modifica el flag de agrega
            flag = "S"
            if int(self.tarj_liq.get_cantidad()) > 0:
                flag = "N"
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("Existe el registro de "
                    " liquidación Nro: "+str(self.tarj_liq.get_liquidacion())+". "
                    "<b>VERIFICAR !!!</b>.")
            # Verifica consistencia de datos si no existe la liquidación
            if flag == "S":
                # Verifica si seleccionó un producto
                if int(self.tarj_liq.get_id_producto()) == 0:
                    flag = "N"
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("Debe seleccionar un"
                        " producto (tarjeta) para la liquidación Nro: "
                        +str(self.tarj_liq.get_liquidacion())+". "
                        "<b>VERIFICAR !!!</b>.")
            if flag == "S":
                # Verifica si seleccionó un producto
                if int(self.tarj_liq.get_cupones()) == 0:
                    flag = "N"
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("Debe ingresar la"
                        " cantidad de cupones de la liquidación Nro: "
                        +str(self.tarj_liq.get_liquidacion())+". "
                        "<b>VERIFICAR !!!</b>.")
            if flag == "S":
                # Verifica los importes
                bruto = round(self.tarj_liq.get_importe_neto()+self.tarj_liq.get_importe_desc(), 2)
                if bruto != self.tarj_liq.get_importe_bruto():
                    flag = "N"
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("Los importes de la"
                        " liquidación Nro: "+str(self.tarj_liq.get_liquidacion())+" "
                        " son inconsistentes. <b>VERIFICAR !!!</b>.<br>"
                        " Importes: "+str(self.tarj_liq.get_importe_bruto())+" suma "
                        " -> "+str(bruto))
            if flag == "S":
                # Verifica los Descuentos
                descuentos = round(self.tarj_liq.get_arancel()+self.tarj_liq.get_costo_financiero()+\
                    self.tarj_liq.get_otros_deb()+self.tarj_liq.get_iva_arancel()+\
                    self.tarj_liq.get_iva_costo_financiero()+self.tarj_liq.get_iva_otros_deb()+\
                    self.tarj_liq.get_impuesto_debcred()+self.tarj_liq.get_impuesto_interes()+\
                    self.tarj_liq.get_retencion_iva()+self.tarj_liq.get_retencion_imp_gan()+\
                    self.tarj_liq.get_retencion_ing_brutos()+self.tarj_liq.get_percepcion_iva()+\
                    self.tarj_liq.get_percepcion_ing_brutos(), 2)
                if descuentos != self.tarj_liq.get_importe_desc():
                    flag = "N"
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("Los descuentos de la"
                        " liquidación Nro: "+str(self.tarj_liq.get_liquidacion())+" "
                        " son inconsistentes. <b>VERIFICAR !!!</b>.")
            # Agrega si las verificaciones fueron positivas
            if flag == "S":
                # Carga datos faltantes para agregar
                id_producto = int(self.tarj_liq.get_id_producto())
                if id_producto in self.tarj_productos_listar_dicc:
                    id_operador = \
                        self.tarj_productos_listar_dicc[id_producto][2]
                else:
                    id_operador = 0
                self.tarj_liq.set_id_operador(id_operador)
                self.tarj_liq.set_banco_suc('023035')
                self.tarj_liq.set_moneda('032')
                self.tarj_liq.set_marca_cupones(int(0))
                self.tarj_liq.set_marca_banco(int(0))
                self.tarj_liq.set_opera_banco(int(0))
                self.tarj_liq.set_estado(int(1))
                id_usuario = 1 # Va el id del USUARIO logueado
                self.tarj_liq.set_id_usuario_act(id_usuario)
                ahora = datetime.now()
                fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                self.tarj_liq.set_fecha_act(fecha_act)
                self.tarj_liq.insert()
                self.datos_pg['cantidad'] = self.tarj_liq.get_cantidad()
                # Agrega las alertas:
                if int(self.tarj_liq.get_cantidad()) > 0:
                    self.alertas.append("alertaSuceso")
                    self.datos_pg["alertaSuceso"] = ("Agregó el registro de "
                        " liquidación Nro: "+str(self.tarj_liq.get_liquidacion())+" "
                        "con <b>EXITO !!!</b>.")
                else:
                    self.alertas.append("alertaPeligro")
                    self.datos_pg["alertaPeligro"] = ("No se pudo agregar "
                        "el registro de liquidación. <b>VERIFICAR !!!</b>.")
            else:
                self.alertas.append("alertaPeligro")
                self.datos_pg["alertaPeligro"] = ("No se agrega "
                    "el registro de la liquidación.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para listar:
        if self.accion == "Listar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Liquidaciones")
            self.datos_pg['info'] = ("Realiza un listado con datos de la "
                    "tabla.<br>Seleccione en <b>Opciones de Fechas</b> "
                    "un rango y tipo de fechas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfListar",]
            # Arma los datos para la vista:
            self.opciones.append("fechasOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar el listado:
        if self.accion == "ConfListar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de listar:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Liquidaciones")
            self.datos_pg['info'] = ("Listado de datos de la tabla, dentro "
                                     "del rango y tipo de fechas"
                                     " seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.tarj_liq.find_all_listar(opciones)
            self.datos_pg["cantidad"] = self.tarj_liq.get_cantidad()
            if self.tarj_liq.get_cantidad() == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay liquidaciones en "
                    "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Arma la tabla para listar:
            tabla = TarjLiqTabla()
            tabla.arma_tabla(datos, opciones, self.tarj_productos_listar_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para buscar
        if self.accion == "Buscar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Liquidaciones")
            self.datos_pg['info'] = ("Realiza una busqueda de Liquidaciones. "
                        "<br>Seleccione en <b>Opciones del listado</b>"
                        " los parámetros para la acción.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfBuscar"]
            # Arma los datos para la vista:
            self.opciones.append("buscarOpcion")
            # Carga los select para las opciones:
            # Select del producto:
            datos = self.tarj_productos_buscar_dicc
            cantidad = self.cant_productos
            nombre = 'producto'
            select_tipo = Select()
            select_tipo.arma_select(datos, cantidad, nombre)
            self.componentes += ["select_producto",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar buscar
        if self.accion == "ConfBuscar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de búsqueda:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            opciones['id_producto'] = int(self.form.getvalue("producto"))
            opciones['liquidacion'] = int(self.form.getvalue("liquidacion"))
            opciones['marca_cupones'] = int(self.form.getvalue("marca_cupones"))
            opciones['marca_banco'] = int(self.form.getvalue("marca_banco"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Liquidaciones")
            self.datos_pg['info'] = ("Liquidaciones encontrados segun las "
                                     "opciones de busqueda seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la busqueda para listar:
            datos = self.tarj_liq.find_all_buscar(opciones)
            self.datos_pg["cantidad"] = self.tarj_liq.get_cantidad()
            # Arma la tabla para listar:
            tabla = TarjLiqTabla()
            tabla.arma_tabla(datos, opciones, self.tarj_productos_listar_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para conciliar
        if self.accion == "Conciliar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Conciliar Liquidaciones")
            self.datos_pg['info'] = ("Concilia los cupones con Liquidaciones. "
                        "<br>Seleccione en <b>Opciones de fechas</b>"
                        " los parámetros para la acción.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfConciliar"]
            # Arma los datos para la vista:
            self.opciones.append("fechasOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar conciliar
        if self.accion == "ConfConciliar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de búsqueda:
            opciones = {}
            opciones['fecha_d'] = self.datos_pg["fecha_d"] = fechas[0]
            opciones['fecha_h'] = self.datos_pg["fecha_h"] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            if int(self.form.getvalue("tipo")) == 1:
                self.datos_pg["tipo"] = "Proceso"
            else:
                self.datos_pg["tipo"] = "Pago"
            # Agrega titulo e  información al panel:
            self.datos_pg['tituloPanel'] = ("Conciliar Liquidaciones")
            self.datos_pg['info'] = ("Liquidaciones conciliadas segun las "
                                     "opciones de busqueda seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la busqueda para conciliar:
            datos = self.tarj_liq.find_all_conciliar(opciones)
            self.cant_liquidaciones = self.tarj_liq.get_cantidad()
            # Recorre las liquidaciones y busca los cupones
            for dato in datos:
                cantCupones = int(0)
                self.tarj_cupon.set_liquidacion(int(dato[1]))
                self.tarj_cupon.set_id_producto(int(dato[4]))
                self.tarj_cupon.find_all_liquidacion_producto()
                cantCupones = int(self.tarj_cupon.get_cantidad())
                if cantCupones == int(dato[8]):
                    self.tarj_liq.set_id(int(dato[0]))
                    self.tarj_liq.find()
                    self.tarj_liq.set_marca_cupones(int(1))
                    id_usuario = 1 # Va el id del USUARIO logueado
                    self.tarj_liq.set_id_usuario_act(id_usuario)
                    ahora = datetime.now()
                    fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                    self.tarj_liq.set_fecha_act(fecha_act)
                    #self.tarj_liq.update()
                    #self.cant_conciliados += self.tarj_liq.get_cantidad()
                    self.cant_conciliados += 1
                elif cantCupones != int(dato[8]):
                    self.tarj_liq.set_id(int(dato[0]))
                    self.tarj_liq.find()
                    self.tarj_liq.set_marca_cupones(int(2))
                    id_usuario = 1 # Va el id del USUARIO logueado
                    self.tarj_liq.set_id_usuario_act(id_usuario)
                    ahora = datetime.now()
                    fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                    self.tarj_liq.set_fecha_act(fecha_act)
                    #self.tarj_liq.update()
                    #self.cant_conciliados += self.tarj_liq.get_cantidad()
                    self.cant_con_diferencias += 1
                else:
                    self.cant_sin_conciliar += 1

            # Arma los datos para la vista:
            self.contenidos.append("conciliarDatos")
            self.datos_pg["cantLiquidaciones"] = self.cant_liquidaciones
            self.datos_pg["cantConciliados"] = self.cant_conciliados
            self.datos_pg["cantConDiferencias"] = self.cant_con_diferencias
            self.datos_pg["cantSinConciliar"] = self.cant_sin_conciliar
            # Muestra la vista:
            self.muestra_vista()

    def fecha_db(self, fecha_txt):
        """
        Convierte la fecha para la tabla de la DB.

        Convierte la fecha del txt al formato necesario para
        persistir en la tabla de la DB.
        """
        dia = fecha_txt[6:]
        mes = fecha_txt[4:6]
        ano = fecha_txt[0:4]
        fecha_op = date(int(ano), int(mes), int(dia))
        return date.strftime(fecha_op, '%Y-%m-%d')

    def importe_db(self, importe_txt):
        """
        Convierte los importes para la tabla de la DB.

        Convierte los importes de archivo txt FIVSER al formato necesario para
        persistir en la tabla de la DB.
        """
        #print("{0:.2f}".format(float(importe_txt)/100))
        return "{0:.2f}".format(float(importe_txt)/100)

    def importe_db_n(self, importe_txt):
        """
        Convierte los importes negativos para la tabla de la DB.

        Convierte los importes negativos de archivo txt FIVSER al formato
        necesario para persistir en la tabla de la DB.
        """
        return "{0:.2f}".format(float(importe_txt) / 100 * -1)
        #return "{0:.2f}".format(float(importe_txt)/100)

    def actualiza_cupon(self):
        id_usuario = 1 # Va el id del USUARIO logueado
        self.tarj_cupon.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.tarj_cupon.set_fecha_act(fecha_act)
        self.tarj_cupon.update()
        self.cant_actualizados += self.tarj_cupon.get_cantidad()

    def carga_liquidacion(self):
        self.tarj_liq.set_estado(int(1))
        id_usuario = 1 # Va el id del USUARIO logueado
        self.tarj_liq.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.tarj_liq.set_fecha_act(fecha_act)
        self.tarj_liq.insert()
        self.cant_cargados += self.tarj_liq.get_cantidad()
        #self.cant_cargados +=1

    def muestra_vista(self):
        """
        Muestra la vista de la aplicación.

        Muestra pagina.html luego de renderizar los datos.
        """
        # Instancia la clase MotorVista y escribe el html:
        print(MotorVista().arma_vista(self.tipo, self.botones_ac,
                                      self.botones_ev, self.botones_aux,
                                      self.alertas, self.opciones,
                                      self.contenidos, self.tablas,
                                      self.componentes, self.datos_pg,
                                      self.modulo))
