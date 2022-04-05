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
from datetime import date
from datetime import datetime
from builtins import int
# Módulos de la aplicación:
from includes.control.motorVista import MotorVista
from modulos.bancoMov.modelo.bancoMovModelo import BancoMovModelo
from modulos.bancoMov.includes.bancoMovTabla import BancoMovTabla
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
        self.datos_pg['tituloPagina'] = "Movimientos Banco"
        self.datos_pg['usuario'] = "Alvaro"
        self.datos_pg['tituloBadge'] = "Movim."
        # Obtiene la cantidad de registros de la tabla para badge:
        self.banco_mov.count()
        self.datos_pg['cantidad'] = self.banco_mov.get_cantidad()
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar", 
                          "botonListar", "botonBuscar"]
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
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.banco_mov.find_all_listar(opciones)
            self.datos_pg["cantidad"] = self.banco_mov.get_cantidad()
            if self.banco_mov.get_cantidad() == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay movimientos en "
                    "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Arma la tabla para listar:
            tabla = BancoMovTabla()
            tabla.arma_tabla(datos, opciones)
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
