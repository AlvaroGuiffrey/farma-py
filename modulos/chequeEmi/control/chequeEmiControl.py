# -*- coding: latin-1 -*-
#
# chequeEmiControl.py
#
# Creado: 19/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import os
import socket
import cgi
import csv
from datetime import date
from datetime import datetime
from builtins import int
# Módulos de la aplicación:
from includes.control.motorVista import MotorVista
from modulos.chequeEmi.modelo.chequeEmiModelo import ChequeEmiModelo
from modulos.chequeEmi.includes.chequeEmiTabla import ChequeEmiTabla
from modulos.chequeEmi.includes.chequeEmiPDF import ChequeEmiPDF
from includes.includes.select import Select

class ChequeEmiControl():
    """
    Clase control del módulo chequeEmi.

    Realiza operaciones con cheques emitidos, utilizando el patron MVC.
    """
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia las clases del modelo:
        self.cheque_emi = ChequeEmiModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'chequeEmi'
        self.form = ''
        self.archivo = './archivos/banco/cheques.txt'
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
        self.cant_agregados = int(0)
        self.cant_actualizados = int(0)
        self.cant_cargados = int(0)
        self.cant_existentes = int(0)
        self.cant_repetidos = int(0)
        self.linea = []
        # Consulta tablas que se utilizan en el módulo:

        # Arma diccionarios que se utilizan en el módulo con datos de tablas:

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
        self.datos_pg['tituloPagina'] = "Cheques Emitidos"
        self.datos_pg['usuario'] = "Alvaro"
        self.datos_pg['tituloBadge'] = "Cheques"
        # Obtiene la cantidad de registros de la tabla para badge:
        self.cheque_emi.count()
        self.datos_pg['cantidad'] = self.cheque_emi.get_cantidad()
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar", "botonAgregar",
                          "botonListar", "botonListarInv", "botonBuscar"]
        # Selecciona las acciones:
        if "bt_agregar" in self.form: self.accion = "Agregar"
        elif "bt_conf_agregar" in self.form: self.accion = "ConfAgregar"
        elif "bt_cargar" in self.form: self.accion = "Cargar"
        elif "bt_conf_cargar" in self.form: self.accion = "ConfCargar"
        elif "bt_listar" in self.form: self.accion = "Listar"
        elif "bt_conf_listar" in self.form: self.accion = "ConfListar"
        elif "bt_listar_inv" in self.form: self.accion = "ListarInv"
        elif "bt_conf_listar_inv" in self.form: self.accion = "ConfListarInv"
        elif "bt_buscar" in self.form: self.accion = "Buscar"
        elif "bt_conf_buscar" in self.form: self.accion = "ConfBuscar"
        elif "bt_descargar_pdf" in self.form: self.accion = "DescargarPDF"
        elif "bt_editar" in self.form: self.accion = "Editar"
        elif "bt_descartar" in self.form: self.accion = "Descartar"
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_agregados = self.cant_cargados = self.cant_repetidos = 0

        # Acción para iniciar:
        if self.accion == "Iniciar":
            #print("llegue aca<br>")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tabla de Cheques Emitidos")
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
            self.datos_pg['tituloPanel'] = ("Carga Cheques Emitidos")
            self.datos_pg['info'] = ("Carga cheques emitidos en la"
                                     " tabla desde el archivo cheques.txt"
                                     " descargado del BERSA. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Agrega las alertas:
            self.alertas.append("alertaInfo")
            self.datos_pg["alertaInfo"] = ("Carga cheques emitidos "
                        "desde el archivo <b>cheques.txt"
                        "</b>. Confirme el evento.")
            # Carga el txt:
            # Abre el archivo txt
            try:
                txtfile = open(self.archivo, "r")
                arch = txtfile.readlines()
                cant_txt = sum(1 for dato in arch)
                txtfile.close()
                # Archivo txt vacio
                if cant_txt == 0:
                    # Agrega las alertas:
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("El archivo TXT esta "
                        "vacio. <b>VERIFICAR !!!</b>.")

            except FileNotFoundError:
                # No existe el archivo TXT
                cant_txt = 0
                # Agrega las alertas:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No existe el archivo: "
                    "cheques.txt, <b>VERIFICAR !!!</b>.")
            # Agrega los botones para la acción:
            if cant_txt > 0: self.botones_ev = ["botonConfCargar",]
            # Carga datos de la vista
            self.contenidos.append("cargarDatos")
            self.datos_pg["cantTxt"] = cant_txt
            self.datos_pg["cantCargados"] = self.datos_pg["cantRepetidos"] = 0
            self.datos_pg["cantActualizados"] = 0
            self.datos_pg["cantAgregados"] = self.datos_pg["cantExistentes"] = 0
            # Muestra la vista:
            self.muestra_vista()

        # Acción para confirmar cargar:
        if self.accion == "ConfCargar":
            # Recibe datos por POST:
            cant_txt = self.form.getvalue("cant_txt")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Cheques Emitidos")
            self.datos_pg['info'] = ("Carga cheques emitidos en la"
                                     " tabla desde el archivo cheques.txt"
                                     " descargado del BERSA. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Pone en 0 los totalizadores
            self.cant_repetidos = self.cant_faltantes = self.cant_cargados = 0
            self.cant_actualizados = self.cant_existentes = 0
            # Abre el archivo txt
            txtfile = open(self.archivo, "r")
            arch = txtfile.readlines()
            txtfile.close()
            # Extrae los datos del archivo txt
            for dato in arch:
                self.cheque_emi.set_id_cheque(str(dato[0:15]))
                self.cheque_emi.set_numero(int(dato[15:27]))
                # Consulta en DB si existe el cheque
                cheques = self.cheque_emi.find_all_id_cheque_numero()
                if self.cheque_emi.get_cantidad() > 1:
                    self.cant_repetidos += self.cheque_emi.get_cantidad()
                elif self.cheque_emi.get_cantidad() == 1:
                    self.cant_existentes += 1
                    for cheque in cheques:
                        if str(cheque[4]) != str(dato[339:359]):
                            self.cheque_emi.set_id(int(cheque[0]))
                            self.cheque_emi.find()
                            self.cheque_emi.set_estado_cheque(str(dato[339:359]))
                            id_usuario = 1 # Va el id del USUARIO logueado
                            self.cheque_emi.set_id_usuario_act(id_usuario)
                            ahora = datetime.now()
                            fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                            self.cheque_emi.set_fecha_act(fecha_act)
                            self.cheque_emi.update()
                            self.cant_actualizados += self.cheque_emi.get_cantidad()
                else:
                    self.cheque_emi.set_fecha_emi(self.fecha_db(str(dato[359:369])))
                    self.cheque_emi.set_fecha_pago(self.fecha_db(str(dato[309:319])))
                    self.cheque_emi.set_importe(self.importe_db(str(dato[280:298])))
                    self.cheque_emi.set_cuit_emi(str(dato[78:89]))
                    self.cheque_emi.set_nombre_emi(str(dato[89:120])) # solo 30 caracteres
                    self.cheque_emi.set_cmc7(str(dato[49:78]))
                    self.cheque_emi.set_tipo(str(dato[375:378]))
                    self.cheque_emi.set_caracter(str(dato[378:393]))
                    self.cheque_emi.set_concepto(str(dato[319:339]))
                    self.cheque_emi.set_referencia(str(dato[403:434])) # solo 30 caracteres
                    self.cheque_emi.set_valor_ref(str(dato[503:519])) # solo 15 caracteres
                    self.cheque_emi.set_estado_cheque(str(dato[339:359]))
                    self.cheque_emi.set_id_mov_banco(int(0))
                    self.cheque_emi.set_fecha_banco("0000-00-00")
                    self.cheque_emi.set_estado(int(1))
                    id_usuario = 1 # Va el id del USUARIO logueado
                    self.cheque_emi.set_id_usuario_act(id_usuario)
                    ahora = datetime.now()
                    fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                    self.cheque_emi.set_fecha_act(fecha_act)
                    self.cheque_emi.insert()
                    self.cant_cargados += self.cheque_emi.get_cantidad()

            # Carga datos de la vista
            self.contenidos.append("cargarDatos")
            self.datos_pg["cantTxt"] = cant_txt
            self.datos_pg["cantCargados"] = self.cant_cargados
            self.datos_pg["cantExistentes"] = self.cant_existentes
            self.datos_pg["cantActualizados"] = self.cant_actualizados
            self.datos_pg["cantRepetidos"] = self.cant_repetidos
            self.datos_pg["cantAgregados"] = 0
            # Carga mensajes de la vista
            if self.cant_cargados > 0:
                self.alertas.append("alertaSuceso")
                self.datos_pg["alertaSuceso"] = ("Se cargaron registros a la "
                    "tabla con <b>EXITO !!!</b>.")
            if self.cant_repetidos > 0:
                self.alertas.append("alertaPeligro")
                self.datos_pg["alertaPeligro"] = ("El archivo contiene "
                    "datos de registros repetidos en la tabla. "
                    "<b>VERIFICAR !!!</b>.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para agregar
        if self.accion == "Agregar":
            # Recibe datos por POST:

            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Cheques Emitidos - Agregar")
            self.datos_pg['info'] = ("Permite agregar los datos de un cheque"
                        " emitido en la tabla de la DB.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfAgregar"]
            #Arma los datos para la vista:
            self.contenidos = ["agregarDato",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar agregar:
        if self.accion == "ConfAgregar":
            # Recibe datos por POST:
            self.cheque_emi.set_numero(int(self.form.getvalue("numero")))
            self.cheque_emi.set_importe(float(self.form.getvalue("importe")))
            self.cheque_emi.set_fecha_emi(str(self.form.getvalue("fecha_emi")))
            self.cheque_emi.set_fecha_pago(str(self.form.getvalue("fecha_pago")))
            self.cheque_emi.set_cuit_emi(int(self.form.getvalue("cuit_emi")))
            self.cheque_emi.set_nombre_emi(str(self.form.getvalue("nombre_emi")))
            self.cheque_emi.set_caracter(str(self.form.getvalue("caracter")))
            self.cheque_emi.set_concepto(str(self.form.getvalue("concepto")))
            self.cheque_emi.set_referencia(str(self.form.getvalue("referencia")))
            self.cheque_emi.set_valor_ref(str(self.form.getvalue("valor_ref")))
            self.cheque_emi.set_estado_cheque(str(self.form.getvalue("estado_cheque")))
            # Datos no recibidos por POST:
            self.cheque_emi.set_id_cheque(str(""))
            self.cheque_emi.set_cmc7(int(0))
            self.cheque_emi.set_tipo(str("CPD"))
            self.cheque_emi.set_id_mov_banco(int(0))
            self.cheque_emi.set_fecha_banco("0000-00-00")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Cheques Emitidos - Ver Agregado")
            self.datos_pg['info'] = ("Permite ver los datos agregados de "
                        "un renglón en la DB.")
            # Busca cheque por el número
            self.cheque_emi.find_numero()
            # Existe el cheque, arma alerta y modifica el flag de agrega
            flag = "S"
            if int(self.cheque_emi.get_cantidad()) > 0:
                flag = "N"
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("Existe el cheque "
                    " emitido Nro: "+str(self.cheque_emi.get_numero())+". "
                    "<b>VERIFICAR !!!</b>.")
            # Agrega si no existe el cheque
            if flag == "S":
                # Carga datos faltantes para agregar
                self.cheque_emi.set_estado(int(1))
                id_usuario = 1 # Va el id del USUARIO logueado
                self.cheque_emi.set_id_usuario_act(id_usuario)
                ahora = datetime.now()
                fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                self.cheque_emi.set_fecha_act(fecha_act)
                self.cheque_emi.insert()
                self.datos_pg['cantidad'] = self.cheque_emi.get_cantidad()
                # Agrega las alertas:
                if int(self.cheque_emi.get_cantidad()) > 0:
                    self.alertas.append("alertaSuceso")
                    self.datos_pg["alertaSuceso"] = ("Agregó el registro del "
                        " cheque Nro: "+str(self.cheque_emi.get_numero())+" "
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
            self.datos_pg['tituloPanel'] = ("Listado de Cheques Emitidos")
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
            opciones['accion'] = self.accion
            opciones['fecha'] = fechas[0]
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            opciones['nombre_emi'] = "0"
            opciones['estado_cheque'] = "TODOS"
            #print(str(opciones['fecha_d'])+" / "+str(opciones['fecha_h'])+" / "+
            #        str(opciones['tipo']))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Cheques Emitidos")
            self.datos_pg['info'] = ("Listado de datos de la tabla, dentro "
                                     "del rango y tipo de fechas"
                                     " seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.cheque_emi.find_all_listar(opciones)
            self.datos_pg["cantidad"] = self.cheque_emi.get_cantidad()
            if int(self.cheque_emi.get_cantidad()) == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay Cheques Emitidos "
                    "en las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Arma la tabla para listar:
            tabla = ChequeEmiTabla()
            tabla.arma_tabla(datos, opciones)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para listar el inventario:
        if self.accion == "ListarInv":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado del Inventario de Cheques "
                                                "Emitidos")
            self.datos_pg['info'] = ("Realiza un listado del Inventario de "
                    "cheques emitidos con datos de la tabla. "
                    "<br>Seleccione en <b>Opciones de fecha</b>.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfListarInv",]
            # Arma los datos para la vista:
            self.opciones.append("fechaOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar el listado del inventario:
        if self.accion == "ConfListarInv":
            # Recibe datos por POST:
            fecha = self.form.getvalue("fecha")
            # Arma las opciones de listar:
            opciones = {}
            opciones['accion'] = self.accion
            opciones['fecha'] = fecha
            opciones['fecha_d'] = fecha
            opciones['fecha_h'] = fecha
            opciones['tipo'] = 0
            opciones['nombre_emi'] = "0"
            opciones['estado_cheque'] = "TODOS"
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado del Inventario de Cheques "
                                            "Emitidos")
            self.datos_pg['info'] = ("Listado del Inventario de Cheques "
                                     "emitidos con datos de la tabla, desde "
                                     "la fecha seleccionada.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.cheque_emi.find_all_inventario(opciones)
            # Arma datos para la vista
            self.datos_pg["cantidad"] = self.cheque_emi.get_cantidad()
            if int(self.cheque_emi.get_cantidad()) == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay cheques emitidos "
                    "para la fecha seleccionada. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Arma la tabla para listar:
            tabla = ChequeEmiTabla()
            tabla.arma_tabla(datos, opciones)
            self.tablas = ["tabla",]

            # Muestra la vista:
            self.muestra_vista()
        # Acción para buscar
        if self.accion == "Buscar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Cheques Emitidos")
            self.datos_pg['info'] = ("Realiza una busqueda de cheques emitidos. "
                        "<br>Seleccione en <b>Opciones del listado</b>"
                        " los parámetros para la acción.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfBuscar"]
            # Arma los datos para la vista:
            self.opciones.append("buscarOpcion")
            # Carga los select para las opciones:
            # Select de nombres:
            nombres_emi = self.cheque_emi.find_all_nombre_emi_dic()
            cantidad = self.cheque_emi.get_cantidad()
            nombres_emi_dicc = {reng[0]: reng[0] for reng in nombres_emi}
            datos = nombres_emi_dicc
            nombre = 'nombre'
            select_tipo = Select()
            select_tipo.arma_select(datos, cantidad, nombre)
            self.componentes += ["select_nombre",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar buscar
        if self.accion == "ConfBuscar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de búsqueda:
            opciones = {}
            opciones['accion'] = self.accion
            opciones['fecha'] = fechas[0]
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            opciones['numero'] = int(self.form.getvalue("numero"))
            opciones['nombre_emi'] = str(self.form.getvalue("nombre"))
            opciones['estado_cheque'] = str(self.form.getvalue("estado_cheque"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Cheques Emitidos")
            self.datos_pg['info'] = ("Cheques emitidos encontrados segun las "
                                     "opciones de busqueda seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la busqueda para listar:
            datos = self.cheque_emi.find_all_buscar(opciones)
            self.datos_pg["cantidad"] = self.cheque_emi.get_cantidad()
            # Arma la tabla para listar:
            tabla = ChequeEmiTabla()
            tabla.arma_tabla(datos, opciones)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para descargar PDF:
        if self.accion == "DescargarPDF":
            # Recibe datos por POST:
            # Carga las opciones de búsqueda con datos recibidos:
            opciones = {}
            opciones['fecha'] = self.form.getvalue("fecha")
            opciones['fecha_d'] = self.form.getvalue("fecha_d")
            opciones['fecha_h'] = self.form.getvalue("fecha_h")
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            tipo_fecha = self.form.getvalue("tipo_fecha")
            # OJO con número ------------
            opciones['numero'] = 0
            # -------------------------------
            opciones['nombre_emi'] = self.form.getvalue("nombre_emi")
            opciones['estado_cheque'] = self.form.getvalue("estado_cheque")
            opciones['accion'] = self.form.getvalue("accion")
            # Cambia formato:
            fecha_r = opciones['fecha'].split("-")
            fecha = (fecha_r[2]+"/"+fecha_r[1]+"/"+fecha_r[0])
            fecha_r = opciones['fecha_d'].split("-")
            fecha_d = (fecha_r[2]+"/"+fecha_r[1]+"/"+fecha_r[0])
            fecha_r = opciones['fecha_h'].split("-")
            fecha_h = (fecha_r[2]+"/"+fecha_r[1]+"/"+fecha_r[0])
            # Arma titulo y detalle del PDF
            if opciones['accion'] == "ConfListarInv":
                titulo_pdf = ("Listado del Inventario de Cheques Emitidos")
                detalle_pdf = ("Pendientes de Pago al: "+fecha)
            else:
                titulo_pdf = ("Listado de Cheques Emitidos")
                detalle_pdf = ("Fecha de "+tipo_fecha+" desde: "+fecha_d+
                " - hasta: "+fecha_h+" ")
                if opciones['nombre_emi'] != "0":
                    detalle_pdf += (" a: "+opciones['nombre_emi'])
                if opciones['estado_cheque'] != "TODOS":
                    detalle_pdf += (" c/estado: "+opciones['estado_cheque'])
            # Consulta la tabla:
            if opciones['accion'] == "ConfListarInv":
                datos = self.cheque_emi.find_all_inventario(opciones)
            elif opciones['accion'] == "ConfListar":
                datos = self.cheque_emi.find_all_listar(opciones)
            else:
                datos = self.cheque_emi.find_all_buscar(opciones)
            self.datos_pg["cantidad"] = self.cheque_emi.get_cantidad()
            # Escribe y guarda el archivo PDF:
            pdf = ChequeEmiPDF()
            pdf.escribir_pdf(datos, titulo_pdf, detalle_pdf, opciones)
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Descarga Listado en PDF")
            self.datos_pg['info'] = ("Realiza la descarga del listado de "
                        "cheques emitidos en un archivo PDF "
                        "en el directorio: 'archivos/banco' de la aplicación."
                        "<br>También lo puede abrir en el navegador con el "
                        "botón 'Abrir PDF'.")
            # Agrega las alertas:
            self.alertas.append("alertaSuceso")
            self.datos_pg["alertaSuceso"] = ("Se descargó el archivo PDF "
                    "con <b>EXITO !!!</b>.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonAbrirChequeEmiPDF",]
            # Muestra la vista:
            self.muestra_vista()


    def fecha_db(self, fecha_txt):
        """
        Convierte la fecha para la tabla de la DB.

        Convierte la fecha del txt al formato necesario para
        persistir en la tabla de la DB.
        """
        fecha_r = fecha_txt.split("/")
        fecha_op = date(int(fecha_r[2]), int(fecha_r[1]), int(fecha_r[0]))
        #print(str(date.strftime(fecha_op, '%Y-%m-%d')))
        return date.strftime(fecha_op, '%Y-%m-%d')

    def importe_db(self, importe_txt):
        """
        Convierte los importes para la tabla de la DB.

        Convierte los importes de archivo txt al formato necesario para
        persistir en la tabla de la DB.
        """
        importe = importe_txt.replace(",", ".")
        #print("{0:.2f}".format(float(importe)))
        return "{0:.2f}".format(float(importe))


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
