# -*- coding: latin-1 -*-
#
# bancoMovControl.py
#
# Creado: 30/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import os
import socket
import cgi
import calendar
from datetime import date
from datetime import datetime
from builtins import int
# Módulos de la aplicación:
from includes.control.motorVista import MotorVista
from modulos.bancoMov.modelo.bancoMovModelo import BancoMovModelo
from modulos.bancoMov.modelo.bancoMovConcModelo import BancoMovConcModelo
from modulos.bancoMov.modelo.bancoMovGrupoModelo import BancoMovGrupoModelo
from modulos.bancoMov.includes.bancoMovTabla import BancoMovTabla
from modulos.bancoMov.includes.bancoMovAsientos import BancoMovAsientos
from modulos.bancoMov.includes.bancoMovAsientosTabla import BancoMovAsientosTabla
from modulos.chequeEmi.modelo.chequeEmiModelo import ChequeEmiModelo
from modulos.tarjLiquidacion.modelo.tarjLiqModelo import TarjLiqModelo
from modulos.contab.modelo.contabPCtaModelo import ContabPCtaModelo
#from modulos.bancoMov.includes.bancoMovPDF import BancoMovPDF
from includes.includes.select import Select

class BancoMovControl():
    """
    Clase control del módulo bancoMov.

    Realiza operaciones con movimientos del banco, utilizando el patron MVC.
    """
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia las clases del modelo:
        self.banco_mov = BancoMovModelo()
        self.banco_conc = BancoMovConcModelo()
        self.banco_grupo = BancoMovGrupoModelo()
        self.cheque_emi = ChequeEmiModelo()
        self.tarj_liq = TarjLiqModelo()
        self.contab_p_ctas = ContabPCtaModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'bancoMov'
        self.form = ''
        self.archivo = './archivos/banco/Movimientos.txt'
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
        self.periodo = int(0)
        self.cant_grupos = int(0)
        self.cant_agregados = int(0)
        self.cant_actualizados = int(0)
        self.cant_cargados = int(0)
        self.cant_existentes = int(0)
        self.cant_repetidos = int(0)
        self.cant_sin_grupo = int(0)
        self.cant_conc_cargados = int(0)
        self.cant_cheques_conciliados = int(0)
        self.cant_liq_tarj_conciliados = int(0)
        self.linea = []
        # Consulta tablas que se utilizan en el módulo:
        self.banco_conceptos = self.banco_conc.find_all()
        self.banco_grupos = self.banco_grupo.find_all()
        self.p_ctas = self.contab_p_ctas.find_all()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        if int(self.banco_conc.get_cantidad()) > 0:
            self.banco_conceptos_dicc = {reng[1]: (reng[0], reng[3])
                                for reng in self.banco_conceptos}
        else:
            self.banco_conceptos_dicc = {}
        if int(self.banco_grupo.get_cantidad()) > 0:
            self.cant_grupos = self.banco_grupo.get_cantidad()
            self.banco_grupos_dicc = {reng[0]: (reng[1], reng[2])
                                for reng in self.banco_grupos}
            self.banco_grupos_buscar_dicc = {reng[0]: reng[1] for reng in
                                     self.banco_grupos}
        else:
            self.cant_grupos = 0
            self.banco_grupos_dicc = {}
            self.banco_grupos_buscar_dicc = {}
        if int(self.contab_p_ctas.get_cantidad()) > 0:
            self.cant_p_ctas = self.contab_p_ctas.get_cantidad()
            self.p_ctas_dicc = {reng[0]: reng[2] for reng in self.p_ctas}
        else:
            self.cant_p_ctas = 0
            self.p_ctas_dicc = {}

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
        self.datos_pg['tituloPagina'] = "Movimientos Banco"
        self.datos_pg['usuario'] = "Alvaro"
        self.datos_pg['tituloBadge'] = "Movim."
        # Obtiene la cantidad de registros de la tabla para badge:
        self.banco_mov.count()
        self.datos_pg['cantidad'] = self.banco_mov.get_cantidad()
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar",
                          "botonListar", "botonBuscar", "botonActConcGrupo",
                          "botonConciliar", "botonArmarAsiento"]
        # Selecciona las acciones:
        if "bt_agregar" in self.form: self.accion = "Agregar"
        elif "bt_conf_agregar" in self.form: self.accion = "ConfAgregar"
        elif "bt_cargar" in self.form: self.accion = "Cargar"
        elif "bt_conf_cargar" in self.form: self.accion = "ConfCargar"
        elif "bt_listar" in self.form: self.accion = "Listar"
        elif "bt_conf_listar" in self.form: self.accion = "ConfListar"
        elif "bt_buscar" in self.form: self.accion = "Buscar"
        elif "bt_conf_buscar" in self.form: self.accion = "ConfBuscar"
        elif "bt_descargar_pdf" in self.form: self.accion = "DescargarPDF"
        elif "bt_editar" in self.form: self.accion = "Editar"
        elif "bt_actualizar" in self.form: self.accion = "Actualizar"
        elif "bt_conf_actualizar" in self.form: self.accion = "ConfActualizar"
        elif "bt_conciliar" in self.form: self.accion = "Conciliar"
        elif "bt_conf_conciliar" in self.form: self.accion = "ConfConciliar"
        elif "bt_armar_asiento" in self.form: self.accion = "ArmarAsiento"
        elif "bt_conf_armar_asiento" in self.form: self.accion = "ConfArmarAsiento"
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_agregados = self.cant_cargados = self.cant_repetidos = 0

        # Acción para iniciar:
        if self.accion == "Iniciar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tabla de Movimientos Conformados - Banco")
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
            self.datos_pg['tituloPanel'] = ("Carga Movimientos Conformados - "
                                            "Banco")
            self.datos_pg['info'] = ("Carga movimientos conformados en la"
                                     " tabla desde el archivo Movimientos.txt"
                                     " descargado del Banco BERSA. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Agrega las alertas:
            self.alertas.append("alertaInfo")
            self.datos_pg["alertaInfo"] = ("Carga movimientos conformados "
                        "desde el archivo <b>Movimientos.txt"
                        "</b>. Confirme el evento.")
            cant_txt = 0
            # Carga el txt:
            try:
                # Lee el archivo txt
                txtfile = open(self.archivo, "r")
                arch = txtfile.readlines()
                txtfile.close()
                # Extrae los datos retornados del archivo txt
                # ------------------------------------------
                # Contador de movimientos con espacios y otros
                cont = cant_txt = 0
                for dato in arch:
                    cont += 1
                    renglon = dato.split()
                    if cont > 18 and int(len(renglon)) > 1:
                        cant_txt += 1
                # ----------------------------------------
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
                    "Movimientos.txt, <b>VERIFICAR !!!</b>.")
            # Agrega los botones para la acción:
            if cant_txt > 0: self.botones_ev = ["botonConfCargar",]
            # Carga datos de la vista
            self.contenidos.append("cargarDatos")
            self.datos_pg["cantTxt"] = cant_txt
            self.datos_pg["cantCargados"] = self.datos_pg["cantRepetidos"] = 0
            self.datos_pg["cantActualizados"] = 0
            self.datos_pg["cantAgregados"] = self.datos_pg["cantExistentes"] = 0
            self.datos_pg["cantSinGrupo"] = self.datos_pg["cantConcCargados"] = 0
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar cargar:
        if self.accion == "ConfCargar":
            # Recibe datos por POST:
            cant_txt = self.form.getvalue("cant_txt")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Movimientos Conformados - "
                                            "Banco")
            self.datos_pg['info'] = ("Carga movimientos conformados en la"
                                     " tabla desde el archivo Movimientos.txt"
                                     " descargado del Banco BERSA. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Pone en 0 los totalizadores
            self.cant_repetidos = self.cant_faltantes = self.cant_cargados = 0
            self.cant_actualizados = self.cant_existentes = 0
            self.cant_sin_grupo = self.cant_conc_cargados = 0
            # Buscar la fecha de movimiento menor del archivo txt:
            # Lee el archivo txt
            txtfile = open(self.archivo, "r")
            arch = txtfile.readlines()
            txtfile.close()
            # Extrae los datos retornados del archivo txt
            cont = 0
            fecha_menor = "2100-01-01"
            for dato in arch:
                cont += 1
                renglon = dato.split()
                # Verificar renglón para buscar fecha de movimiento menor
                if cont > 18 and int(len(renglon)) > 1:
                    fecha_txt = self.fecha_db(str(dato[0:10]))
                    if fecha_txt < fecha_menor: fecha_menor = fecha_txt
            # Arma diccionario con banco_mov desde fecha_menor:
            self.banco_mov.set_fecha_mov(fecha_menor)
            movimientos = self.banco_mov.find_all_fecha_dic()
            # Si no hay registros en MySQL con fecha igual o menor a la
            # fecha menor del archivo txt agrega a todos:
            if self.banco_mov.get_cantidad() == 0:
                # Lee el archivo txt
                txtfile = open(self.archivo, "r")
                arch = txtfile.readlines()
                txtfile.close()
                cont = 0
                for dato in arch:
                    cont += 1
                    renglon = dato.split()
                    # Verificar renglón para buscar fecha de movimiento menor
                    if cont > 18 and int(len(renglon)) > 1:
                        # Agrega los datos a tabla DB:
                        self.agrega_datos(dato)
            else:
                # Arma una lista con datos unidos str() de los registros MySQL:
                movi = []
                for reng in movimientos:
                    movi.append(str(reng[0])+str(reng[1])+str(reng[2])
                    +str(reng[3])+str(reng[4]))
                # Lee el txt y agrega en tabla si no existe el comprobante:
                txtfile = open(self.archivo, "r")
                arch = txtfile.readlines()
                txtfile.close()
                cont = 0
                for dato in arch:
                    renglon = dato.split()
                    cont +=1
                    # Verificar renglón para buscar fecha de movimiento menor
                    if cont > 18 and int(len(renglon)) > 1:
                        #self.cant_cargados += 1
                        datos = self.datos_txt(dato)
                        if datos in movi:
                            # Existe el comprobante en la tabla de la DB:
                            self.cant_repetidos += 1
                        else:
                            # Agrega los datos a tabla DB:
                            self.agrega_datos(dato)
                            #self.cant_cargados += 1
            # Carga datos de la vista
            self.contenidos.append("cargarDatos")
            self.datos_pg["cantTxt"] = cant_txt
            self.datos_pg["cantCargados"] = self.cant_cargados
            self.datos_pg["cantSinGrupo"] = self.cant_sin_grupo
            self.datos_pg["cantConcCargados"] = self.cant_conc_cargados
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
        # Acción para listar:
        if self.accion == "Listar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Movimientos - Banco")
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
            self.datos_pg['tituloPanel'] = ("Listado de Movimientos - Banco")
            self.datos_pg['info'] = ("Listado de datos de la tabla, dentro "
                                     "del rango y tipo de fechas"
                                     " seleccionadas.")
            # Encuentra los datos de la tabla para listar:
            datos = self.banco_mov.find_all_listar(opciones)
            self.datos_pg["cantidad"] = self.banco_mov.get_cantidad()
            if self.banco_mov.get_cantidad() == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay movimientos en "
                    "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Arma la tabla para listar:
            tabla = BancoMovTabla()
            tabla.arma_tabla(datos, opciones, self.banco_grupos_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para buscar
        if self.accion == "Buscar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Movimientos - Banco")
            self.datos_pg['info'] = ("Realiza una busqueda de movimientos. "
                        "<br>Seleccione en <b>Opciones del listado</b>"
                        " los parámetros para la acción.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfBuscar"]
            # Arma los datos para la vista:
            self.opciones.append("buscarOpcion")
            # Carga los select para las opciones:
            # Select del grupo:
            datos = self.banco_grupos_buscar_dicc
            cantidad = self.cant_grupos
            nombre = 'grupo'
            select_tipo = Select()
            select_tipo.arma_select(datos, cantidad, nombre)
            self.componentes += ["select_grupo",]
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
            opciones['grupo'] = int(self.form.getvalue("grupo"))
            opciones['numero'] = int(self.form.getvalue("numero"))
            opciones['marca'] = int(self.form.getvalue("marca"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Movimientos - Banco")
            self.datos_pg['info'] = ("Movimientos bancarios encontrados segun "
                                     "las opciones de busqueda seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la busqueda para listar:
            datos = self.banco_mov.find_all_buscar(opciones)
            self.datos_pg["cantidad"] = self.banco_mov.get_cantidad()
            if self.banco_mov.get_cantidad() == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay movimientos para "
                    "las fechas y opciones seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Arma la tabla para listar:
            tabla = BancoMovTabla()
            tabla.arma_tabla(datos, opciones, self.banco_grupos_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para Actualizar:
        if self.accion == "Actualizar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Actualiza Movimientos - Banco")
            self.datos_pg['info'] = ("Realiza una actualización de conceptos y "
                    "grupos en las tablas. <br>Seleccione en <b>Opciones de "
                    "Fechas</b> un rango y tipo de fechas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfActualizar",]
            # Arma los datos para la vista:
            self.opciones.append("fechasOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar la actualización:
        if self.accion == "ConfActualizar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de listar:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Actualiza Movimientos - Banco")
            self.datos_pg['info'] = ("Actualiza conceptos y grupos en las "
                                     "tablas, dentro del rango y tipo de fechas"
                                     " seleccionadas.")
            # Pone en 0 los contadores
            cant_tabla = self.cant_actualizados = 0
            self.cant_conc_cargados = self.cant_sin_grupo = 0
            # Encuentra los datos de la tabla para actualizar:
            datos = self.banco_mov.find_all_listar(opciones)
            cant_tabla = self.datos_pg["cantidad"] = self.banco_mov.get_cantidad()
            if self.banco_mov.get_cantidad() > 0:
                # Actualiza grupo y carga conceptos faltantes:
                for dato in datos:
                    conc = dato[5]
                    if int(dato[6]) == 0:
                        if conc in self.banco_conceptos_dicc:
                            self.banco_mov.set_id(int(dato[0]))
                            self.banco_mov.find()
                            id_grupo = self.banco_conceptos_dicc[conc][1]
                            self.banco_mov.set_id_grupo(int(id_grupo))
                            self.banco_mov.update()
                            self.cant_actualizados += self.banco_mov.get_cantidad()
                        else:
                            self.banco_conc.set_concepto(conc)
                            self.banco_conc.find_concepto()
                            if int(self.banco_conc.get_cantidad()) < 1:
                                self.banco_conc.set_concepto(conc)
                                self.banco_conc.set_comentario("")
                                self.banco_conc.set_id_grupo(0)
                                self.banco_conc.set_estado(int(1))
                                id_usuario = 1 # Va el id del USUARIO logueado
                                self.banco_conc.set_id_usuario_act(id_usuario)
                                ahora = datetime.now()
                                fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                                self.banco_conc.set_fecha_act(fecha_act)
                                self.banco_conc.insert()
                                self.cant_conc_cargados += self.banco_conc.get_cantidad()
            else:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay movimientos en "
                    "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Carga datos de la vista
            self.contenidos.append("actualizarDatos")
            self.datos_pg["cantTabla"] = cant_tabla
            self.datos_pg["cantActualizados"] = self.cant_actualizados
            self.datos_pg["cantConcCargados"] = self.cant_conc_cargados
            self.datos_pg["cantSinGrupo"] = self.cant_sin_grupo
            # Carga mensajes de la vista
            if self.cant_actualizados > 0:
                self.alertas.append("alertaSuceso")
                self.datos_pg["alertaSuceso"] = ("Se actualizaron registros en "
                    "la tabla con <b>EXITO !!!</b>.")
            if self.cant_sin_grupo > 0:
                self.alertas.append("alertaPeligro")
                self.datos_pg["alertaPeligro"] = ("El archivo contiene "
                    " registros sin grupos. "
                    "<b>VERIFICAR !!!</b>.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para conciliar:
        if self.accion == "Conciliar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Conciliar Movimientos - Banco")
            self.datos_pg['info'] = ("Realiza conciliación de movimientos con "
                    "cheques emitidos y liquidación de tarjetas."
                    "<br>Seleccione en <b>Opciones de Fechas</b> "
                    "un rango y tipo de fechas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfConciliar",]
            # Arma los datos para la vista:
            self.opciones.append("fechasOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar la conciliación:
        if self.accion == "ConfConciliar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de conciliar:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Conciliación de Movimientos - Banco")
            self.datos_pg['info'] = ("Concilia datos de la tabla con cheques "
                                     "emitidos y liquidación de tarjetas, "
                                     "dentro del rango y tipo de fechas "
                                     "seleccionadas.")
            # Agrega los botones para la acción:

            # Encuentra los datos de la tabla para conciliar:
            datos = self.banco_mov.find_all_conciliar(opciones)
            self.datos_pg["cantidad"] = self.banco_mov.get_cantidad()
            cant_tabla = self.banco_mov.get_cantidad()
            if self.banco_mov.get_cantidad() == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay movimientos en "
                    "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Pone en 0 los contadores:
            self.cant_cheques_conciliados = self.cant_liq_tarj_conciliados = 0
            self.cant_actualizados = 0
            # Recorre los datos para conciliar:
            for dato in datos:
                if dato[5] == "CHEQUE CLEARING":
                    numero = int(dato[4])
                    self.cheque_emi.set_numero(numero)
                    self.cheque_emi.find_numero()
                    if int(self.cheque_emi.get_cantidad()) == 1:
                        # Carga datos a tabla cheque_emi:
                        self.cheque_emi.set_estado_cheque("PAGADO")
                        self.cheque_emi.set_id_mov_banco(int(dato[0]))
                        self.cheque_emi.set_fecha_banco(dato[2])
                        id_usuario = 1 # Va el id del USUARIO logueado
                        self.cheque_emi.set_id_usuario_act(id_usuario)
                        ahora = datetime.now()
                        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                        self.cheque_emi.set_fecha_act(fecha_act)
                        self.cheque_emi.update()
                        self.cant_cheques_conciliados += \
                                self.cheque_emi.get_cantidad()
                        # Carga datos a tabla:
                        self.banco_mov.set_id(int(dato[0]))
                        self.banco_mov.find()
                        self.banco_mov.set_marca(int(1))
                        id_usuario = 1 # Va el id del USUARIO logueado
                        self.banco_mov.set_id_usuario_act(id_usuario)
                        ahora = datetime.now()
                        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                        self.banco_mov.set_fecha_act(fecha_act)
                        self.banco_mov.update()
                        self.cant_actualizados += self.banco_mov.get_cantidad()
                elif (dato[5] == "CREDITO TARJ MASTERCARD" or \
                        dato[5] == "CREDITO TARJETA CABAL") or \
                        dato[5] == "DB COMERCIO MASTER":
                    self.tarj_liq.set_fecha_pago(dato[2])
                    self.tarj_liq.set_importe_neto(float(dato[3]))
                    self.tarj_liq.find_importe_fecha()
                    if int(self.tarj_liq.get_cantidad()) == 1:
                        # Carga datos a tabla tarj_liquidaciones:
                        self.tarj_liq.set_opera_banco(int(dato[0]))
                        self.tarj_liq.set_fecha_banco(dato[2])
                        self.tarj_liq.set_marca_banco(int(1))
                        id_usuario = 1 # Va el id del USUARIO logueado
                        self.tarj_liq.set_id_usuario_act(id_usuario)
                        ahora = datetime.now()
                        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                        self.tarj_liq.set_fecha_act(fecha_act)
                        self.tarj_liq.update_banco()
                        self.cant_liq_tarj_conciliados += self.tarj_liq.get_cantidad()
                        # Carga datos a tabla:
                        self.banco_mov.set_id(int(dato[0]))
                        self.banco_mov.find()
                        self.banco_mov.set_marca(int(1))
                        id_usuario = 1 # Va el id del USUARIO logueado
                        self.banco_mov.set_id_usuario_act(id_usuario)
                        ahora = datetime.now()
                        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                        self.banco_mov.set_fecha_act(fecha_act)
                        self.banco_mov.update()
                        self.cant_actualizados += self.banco_mov.get_cantidad()
            # Carga datos de la vista
            self.contenidos.append("conciliarDatos")
            self.datos_pg["cantTabla"] = cant_tabla
            self.datos_pg["cantActualizados"] = self.cant_actualizados
            self.datos_pg["cantChequesConciliados"] = self.cant_cheques_conciliados
            self.datos_pg["cantLiqTarjConciliados"] = self.cant_liq_tarj_conciliados
            # Muestra la vista:
            self.muestra_vista()
        # Acción para armar asiento:
        if self.accion == "ArmarAsiento":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Asientos Contables de Movimientos"
                                            " - Banco")
            self.datos_pg['info'] = ("Realiza un listado con los asientos "
                    "contables armados con datos de la tabla. "
                    "<br>Seleccione en <b>Opciones de Período</b> "
                    " el mes y año.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfArmarAsiento",]
            # Arma los datos para la vista:
            self.opciones.append("periodoOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar armar asiento:
        if self.accion == "ConfArmarAsiento":
            # Recibe datos por POST:
            self.periodo = self.form.getvalue("periodo")
            # Arma las opciones de listar:
            opciones = {}
            periodo_str = str(self.periodo)
            mes = int(periodo_str[4:])
            anio = int(periodo_str[:4])
            rango_mes = calendar.monthrange(anio, mes)
            dia_h = rango_mes[1]
            opciones['fecha_d'] = date(anio, mes, 1)
            opciones['fecha_h'] = date(anio, mes, dia_h)
            opciones ['tipo'] = 2 # fecha valor
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Asientos Contables de Movimientos"
                                            " - Banco")
            self.datos_pg['info'] = ("Listado asientos contables armados con "
                                     "datos de la tabla, para el período "
                                     "seleccionado.")

            # Verifica si hay movimientos sin agrupar:
            self.banco_mov.find_all_sin_agrupar(opciones)
            if self.banco_mov.get_cantidad() > 0:
                self.alertas.append("alertaPeligro")
                self.datos_pg["alertaPeligro"] = ("Hay "+
                    str(self.banco_mov.get_cantidad())+" movimiento/s sin "
                    "agrupar en el período. <b>REVISAR DATOS TABLA"
                    " !!!</b>.")
            else:
                # Encuentra los datos de la tabla para armar asientos:
                datos = self.banco_mov.find_all_listar(opciones)
                self.datos_pg["cantidad"] = self.banco_mov.get_cantidad()
                if self.banco_mov.get_cantidad() == 0:
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("No hay movimientos en "
                        "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                        " !!!</b>.")
                else:
                    # Agrega los botones para la acción:
                    self.botones_ev = ["botonDescargarPDF",]
                    # Arma diccionario de asientos:
                    mov_asientos = BancoMovAsientos()
                    #print(str(self.p_ctas_dicc['111001']))
                    asientos_dicc = mov_asientos.arma_dicc(datos,
                            self.banco_grupos_dicc, self.p_ctas_dicc)
                    #print(str(asientos_dicc[4]))
                    # Arma la tabla para listar Asientos Contables:
                    tabla = BancoMovAsientosTabla()
                    tabla.arma_tabla(asientos_dicc, opciones)
                    self.tablas = ["tabla",]
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
        return date.strftime(fecha_op, '%Y-%m-%d')

    def importe_db(self, importe_txt):
        """
        Convierte los importes para la tabla de la DB.

        Convierte los importes de archivo txt al formato necesario para
        persistir en la tabla de la DB.
        """
        importe = importe_txt.replace(".", "")
        importe = importe.replace(",", ".")
        return "{0:.2f}".format(float(importe))

    def agrega_datos(self, dato):
        """
        Agrega datos a las tablas.

        Con los datos del archivo Movimientos.txt carga los atributos de la
        clase VO y los agrega en la tabla.
        """
        # Agrega a la tabla recibidos:
        self.carga_datos(dato)
        self.banco_mov.insert()
        self.cant_cargados += self.banco_mov.get_cantidad()
        #self.cant_cargados += 1

    def carga_datos(self, dato):
        """
        Carga datos al Value Object de la tabla.

        Con los datos del archivo Movimientos.txt carga los atributos de
        bancoMovVO para persistir en el modelo.
        """
        # Carga el VO con los datos del txt:
        self.banco_mov.set_fecha_mov(self.fecha_db(str(dato[0:10])))
        self.banco_mov.set_fecha_valor(self.fecha_db(str(dato[30:40])))
        self.banco_mov.set_importe(self.importe_db(str(dato[70:90])))
        self.banco_mov.set_numero(str(dato[90:103]))
        concepto = str(dato[120:170]) # solo 50 caracteres
        self.banco_mov.set_concepto(concepto.strip())
        conc = str(self.banco_mov.get_concepto())
        # Verifica si el concepto está cargado en el diccionario:
        if conc in self.banco_conceptos_dicc:
            id_grupo = self.banco_conceptos_dicc[conc][1]
        # Si no esta lo agrega a la tabla:
        else:
            id_grupo = int(0)
            # Agrega el concepto
            self.banco_conc.set_concepto(conc)
            self.banco_conc.find_concepto()
            if int(self.banco_conc.get_cantidad()) < 1:
                self.banco_conc.set_concepto(conc)
                self.banco_conc.set_comentario("")
                self.banco_conc.set_id_grupo(int(id_grupo))
                self.banco_conc.set_estado(int(1))
                id_usuario = 1 # Va el id del USUARIO logueado
                self.banco_conc.set_id_usuario_act(id_usuario)
                ahora = datetime.now()
                fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                self.banco_conc.set_fecha_act(fecha_act)
                self.banco_conc.insert()
                self.cant_conc_cargados += self.banco_conc.get_cantidad()
                #self.cant_conc_cargados +=1
                id_grupo = self.banco_conc.get_id_grupo()

        if int(id_grupo) == 0: self.cant_sin_grupo +=1
        self.banco_mov.set_id_grupo(int(id_grupo))
        self.banco_mov.set_marca(int(0))
        self.banco_mov.set_comentario(str(""))
        self.banco_mov.set_estado(int(1))
        id_usuario = 1 # Va el id del USUARIO logueado
        self.banco_mov.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.banco_mov.set_fecha_act(fecha_act)

    def datos_txt(self, dato):
        """
        Convierte datos del archivo txt.

        Convierte datos del archivo txt para comparar con datos de la tabla
        para persistir en la DB.
        """
        fecha = self.fecha_db(dato[0:10])
        concepto_txt = str(dato[120:170])
        concepto = concepto_txt.strip()
        datos_txt = str(self.fecha_db(str(dato[0:10])))+\
                str(self.fecha_db(str(dato[30:40])))+\
                str(self.importe_db(str(dato[70:90])))+\
                str(dato[90:103])+str(concepto)
        return datos_txt

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
