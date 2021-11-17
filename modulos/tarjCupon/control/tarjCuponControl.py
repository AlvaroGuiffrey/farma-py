# -*- coding: latin-1 -*-
#
# tarjCuponControl.py
#
# Creado: 02/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2021 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import socket
import cgi
import csv
from datetime import date
from datetime import datetime
from builtins import int
# Módulos de la aplicación:
from includes.control.motorVista import MotorVista
from modulos.tarjeta.modelo.tarjProductoModelo import TarjProductoModelo
from modulos.tarjCupon.modelo.tarjCuponModelo import TarjCuponModelo
from modulos.tarjCupon.includes.tarjCuponTabla import TarjCuponTabla
from modulos.tarjCupon.includes.tarjCorrCuponTabla import TarjCorrCuponTabla
from modulos.tarjLiquidacion.modelo.tarjLiqModelo import TarjLiqModelo
from includes.includes.select import Select

class TarjCuponControl():
    """
    Clase control del módulo tarjCupon.

    Realiza operaciones con cupones de tarjetas por
    ventas realizadas, utilizando el patron MVC.
    """
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia las clases del modelo:
        self.tarj_cupon = TarjCuponModelo()
        self.tarj_producto = TarjProductoModelo()
        self.tarj_liq = TarjLiqModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'tarjCupon'
        self.form = ''
        self.archivo = './archivos/tarjetas/Ventas.csv'
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
        self.cant_agregados = int(0)
        self.cant_actualizados = int(0)
        self.cant_cargados = int(0)
        self.cant_repetidos = int(0)
        self.cant_productos = int(0)
        self.linea = []
        # Consulta tablas que se utilizan en el módulo:
        self.tarj_productos = self.tarj_producto.find_all()
        self.cant_productos = self.tarj_producto.get_cantidad()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.tarj_productos_dicc = {reng[1]: reng[0] for reng in
                               self.tarj_productos}
        self.tarj_productos_listar_dicc = {reng[0]: (reng[1], reng[2])
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
        self.datos_pg['tituloBadge'] = "Cupones"
        # Obtiene la cantidad de registros de la tabla para badge:
        self.tarj_cupon.count()
        self.datos_pg['cantidad'] = self.tarj_cupon.get_cantidad()
        #print("Cupones :", self.tarj_cupon.get_cantidad(), "<br>")
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar", "botonListar",
                          "botonListarInv", "botonBuscar", "botonCorrControlar"]
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
        elif "bt_corr_controlar" in self.form: self.accion = "ControlarCorr"
        elif "bt_conf_corr_controlar" in self.form:
            self.accion = "ConfControlarCorr"
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_agregados = self.cant_cargados = self.cant_repetidos = 0

        # Acción para iniciar:
        if self.accion == "Iniciar":
            #print("llegue aca<br>")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tabla de Tarjetas - Cupones")
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
            self.datos_pg['tituloPanel'] = ("Carga Cupones de Tarjetas")
            self.datos_pg['info'] = ("Carga cupones de tarjetas en la"
                                     " tabla desde el archivo Ventas.csv"
                                     " descargado de FISERV. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Agrega las alertas:
            self.alertas.append("alertaAdvertencia")
            self.datos_pg["alertaAdvertencia"] = ("Carga cupones de tarjetas "
                        "desde el archivo <b>Ventas.csv"
                        "</b>. Confirme el evento.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfCargar",]
            # Carga el CSV:
            csvfile = open(self.archivo, newline="")
            arch = csv.reader(csvfile, delimiter=";")
            next(arch)
            cant_csv = sum(1 for dato in arch)
            csvfile.close()
            # Verifica si existe el CSV:
            if cant_csv > 0:
                self.contenidos.append("cargarDatos")
                self.datos_pg["cantCsv"] = cant_csv
                self.datos_pg["cantCargados"] = 0
                self.datos_pg["cantRepetidos"] = 0
                self.datos_pg["cantAgregados"] = 0
            else:
                # ---- CSV vacio ---- :
                # Agrega las alertas:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("El archivo CSV esta "
                    "vacio. <b>VERIFICAR !!!</b>.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar cargar:
        if self.accion == "ConfCargar":
            # Recibe datos por POST:
            cant_csv = self.form.getvalue("cant_csv")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Cupones de Tarjetas")
            self.datos_pg['info'] = ("Carga cupones de tarjetas en la"
                                     " tabla desde el archivo Ventas.csv"
                                     " descargado de FISERV. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Carga el CSV:
            csvfile = open(self.archivo, newline="")
            arch = csv.reader(csvfile, delimiter=";")
            next(arch)
            # Busca la primer fecha del CSV y consulta MySQL:
            if self.tarj_cupon.get_cantidad() > 0:
                fecha_menor = "2100-01-01"
                for dato in arch:
                    fecha_csv = self.fecha_db(dato[0])
                    if fecha_csv < fecha_menor: fecha_menor = fecha_csv
                self.tarj_cupon.set_fecha(fecha_menor)
                cupones = self.tarj_cupon.find_all_fecha_dic()
                # Posiciona en primer registro de datos el CSV:
            csvfile.seek(0)
            arch = csv.reader(csvfile, delimiter=";")
            next(arch)
            # Si no hay registros en MySQL con fecha igual o menor a la primera
            # del archivo CSV agrega a todos:
            if self.tarj_cupon.get_cantidad() == 0:
                for dato in arch:
                    # Agrega los datos a tabla DB:
                    self.agrega_datos(dato)
            # Hay registros iguales en MySQL y CSV, verifico para agregar:
            else:
                # Arma una lista con datos unidos str() de los registros MySQL:
                compro = []
                for reng in cupones:
                    compro.append(str(reng[1]).zfill(5)+str(reng[2])
                                  +str(reng[3]).zfill(4)+str(reng[4]).zfill(3))
                # Lee el CSV y agrega en tabla si no existe el comprobante:
                for dato in arch:
                    datos_csv = self.datos_csv(dato)
                    if datos_csv in compro:
                        # Existe el comprobante en la tabla de la DB:
                        self.cant_repetidos += 1
                    else:
                        # Agrega los datos a tabla DB:
                        self.agrega_datos(dato)
            # Agrega las alertas:
            if self.cant_cargados > 0:
                self.alertas.append("alertaSuceso")
                self.datos_pg["alertaSuceso"] = ("Se cargaron registros a la "
                    "tabla con <b>EXITO !!!</b>.")

            if self.cant_repetidos > 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("El archivo CSV contiene "
                    "datos ya cargados a la tabla. <b>VERIFICAR !!!</b>.")
            # Arma los datos para la vista:
            self.contenidos.append("cargarDatos")
            self.datos_pg["cantCsv"] = cant_csv
            self.datos_pg["cantCargados"] = self.cant_cargados
            self.datos_pg["cantRepetidos"] = self.cant_repetidos
            # Cierra el archivo CSV:
            csvfile.close()
            # Muestra la vista:
            self.muestra_vista()
        # Acción para listar:
        if self.accion == "Listar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Cupones")
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
            self.datos_pg['tituloPanel'] = ("Listado de Cupones")
            self.datos_pg['info'] = ("Listado de datos de la tabla, dentro "
                                     "del rango y tipo de fechas"
                                     " seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.tarj_cupon.find_all_listar(opciones)
            self.datos_pg["cantidad"] = self.tarj_cupon.get_cantidad()
            if self.tarj_cupon.get_cantidad() == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay cupones en "
                    "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Arma la tabla para listar:
            tabla = TarjCuponTabla()
            tabla.arma_tabla(datos, opciones, self.tarj_productos_listar_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para listar el inventario:
        if self.accion == "ListarInv":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado del Inventario de Cupones")
            self.datos_pg['info'] = ("Realiza un listado del Inventario de "
                    "Cupones con datos de la tabla. "
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
            opciones['fecha'] = fecha
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado del Inventario de Cupones")
            self.datos_pg['info'] = ("Listado del Inventario de Cupones con "
                                     "datos de la tabla, desde la fecha  "
                                     " seleccionada.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            cupones_inv = []

            # 1) BUSCAR LAS LIQUIDACIONES PENDIENTES
            self.tarj_liq.set_fecha_pago(fecha)
            liq_pendi = self.tarj_liq.find_all_pendientes()
            # 2) BUSCAR LOS CUPONES DE LAS LIQUIDACIONES PENDIENTES
            for reng in liq_pendi:
                self.tarj_cupon.set_liquidacion(reng[1])
                self.tarj_cupon.set_id_producto(reng[2])
                cupones = self.tarj_cupon.find_all_liquidacion_producto()
                # 3) UNIENDO LOS DATOS CON lista_cupones.extend(lista_consulta)
                cupones_inv.extend(cupones)
            # 4) BUSCAR CUPONES SIN LIQUIDAR
            self.tarj_cupon.set_fecha(fecha)
            cupones_sin_liq = self.tarj_cupon.find_all_sin_liq()
            # 5) UNIENDO LOS DATOS CON lista_cupones.extend(lista_consulta)
            cupones_inv.extend(cupones_sin_liq)
            # Arma datos para la vista
            self.datos_pg["cantidad"] = len(cupones_inv)
            if int(len(cupones_inv)) == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay cupones para "
                    "la fecha seleccionada. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # 6) ARMAR TABLA INVENTARIO
            # 7) TOTALIZAR Y PONER SUBTITULOS POR LIQUIDADOS Y SIN LIQUIDAR
            # Arma la tabla para listar:
            datos = cupones_inv
            tabla = TarjCuponInvTabla()
            tabla.arma_tabla(datos, opciones, self.tarj_productos_listar_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para buscar
        if self.accion == "Buscar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Cupones")
            self.datos_pg['info'] = ("Realiza una busqueda de Cupones. "
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
            opciones['cupon'] = int(self.form.getvalue("cupon"))
            opciones['lote'] = int(self.form.getvalue("lote"))
            opciones['error'] = int(self.form.getvalue("error"))
            opciones['liquidacion'] = int(self.form.getvalue("liquidacion"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Cupones")
            self.datos_pg['info'] = ("Cupones encontrados segun las opciones "
                                     "de busqueda seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la busqueda para listar:
            datos = self.tarj_cupon.find_all_buscar(opciones)
            self.datos_pg["cantidad"] = self.tarj_cupon.get_cantidad()
            # Arma la tabla para listar:
            tabla = TarjCuponTabla()
            tabla.arma_tabla(datos, opciones, self.tarj_productos_listar_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para Controlar Correlativos:
        if self.accion == "ControlarCorr":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Control de Cupones")
            self.datos_pg['info'] = ("Realiza un listado de cupones NO "
                    "correlativos. <br>Seleccione en <b>Opciones de "
                    "Fechas</b> un rango de fechas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfCorrControlar",]
            # Arma los datos para la vista:
            self.opciones.append("fechasOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para Confirmar Controlar Correlativos:
        if self.accion == "ConfControlarCorr":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de listar:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['tipo'] = int(self.form.getvalue("tipo"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Control de Cupones")
            self.datos_pg['info'] = ("Lista cupones NO correlativos.")

            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.tarj_cupon.find_all_listar(opciones)
            self.datos_pg["cantidad"] = self.tarj_cupon.get_cantidad()
            # Mensaje si no hay Cupones para las fechas seleccionadas
            if self.tarj_cupon.get_cantidad() == 0:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No hay cupones en "
                    "las fechas seleccionadas. <b>VOLVER A INTENTAR"
                    " !!!</b>.")
            # Busca los cupones faltantes
            cont = cupon = 0
            faltantes = []
            # Arma lista con los cupones existentes en la db
            for dato in datos:
                if cont == 0: cupon = int(dato[1])
                if int(dato[1]) == 9999: cupon = int(dato[1])
                if int(dato[1]) == cupon:
                    cont += 1
                    if cupon == 9999: cupon = 0
                    cupon +=1
                else:
                    while int(dato[1]) > cupon:
                        faltantes.append(cupon)
                        cupon +=1
                    cupon +=1
            # Mensaje si no hay cupones Faltantes
            if len(faltantes) == 0:
                self.alertas.append("alertaSuceso")
                self.datos_pg["alertaSuceso"] = ("<b>EXITO !!!</b> No hay "
                    " cupones faltantes en las fechas seleccionadas.")
            # Arma lista
            # Transforma lista de faltantes en una tupla
            cupones_faltan = tuple(faltantes)
            # Arma la tabla para listar:
            tabla = TarjCorrCuponTabla()
            tabla.arma_tabla(cupones_faltan, opciones)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()


    def agrega_datos(self, dato):
        """
        Agrega datos a las tablas.

        Con los datos del archivo Ventas.csv carga los atributos de las
        clases VO y los agrega en las tablas.
        """
        # Agrega a la tabla recibidos:
        self.carga_datos(dato)
        self.tarj_cupon.insert()
        self.cant_cargados += self.tarj_cupon.get_cantidad()
        #self.cant_cargados += 1

    def carga_datos(self, dato):
        """
        Carga datos al Value Object de la tabla.

        Con los datos del archivo Ventas.csv carga los atributos de
        TarjCuponVO para persistir en el modelo.
        """
        # Carga el VO con los datos del CSV:
        self.tarj_cupon.set_cupon(dato[3])
        self.tarj_cupon.set_fecha(self.fecha_db(dato[0]))
        self.tarj_cupon.set_numero(dato[5][1:5]) #elimina un \t
        if dato[18] in self.tarj_productos_dicc:
            id_producto = self.tarj_productos_dicc[dato[18]]
        else:
            id_producto = 0
        self.tarj_cupon.set_id_producto(id_producto)
        #if dato[6] == "ARS":
        #    moneda = "032"
        #else:
        #    moneda = "000"
        self.tarj_cupon.set_moneda(dato[6])
        self.tarj_cupon.set_importe(self.importe_db(dato[7]))
        self.tarj_cupon.set_descuento(self.importe_db(dato[8]))
        self.tarj_cupon.set_neto(self.importe_db(dato[9]))
        self.tarj_cupon.set_cuota(int(dato[16]))
        self.tarj_cupon.set_autorizacion(dato[17])
        self.tarj_cupon.set_error(int(0)) # ponemos 0
        self.tarj_cupon.set_comentario("")
        self.tarj_cupon.set_fecha_presentacion(self.fecha_db(dato[1]))
        self.tarj_cupon.set_lote(dato[13])
        self.tarj_cupon.set_liquidacion(int(0))
        self.tarj_cupon.set_estado(int(1))
        id_usuario = 1 # Va el id del USUARIO logueado
        self.tarj_cupon.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.tarj_cupon.set_fecha_act(fecha_act)

    def fecha_db(self, fecha_csv):
        """
        Convierte la fecha para la tabla de la DB.

        Convierte la fecha de IVA Compras PLEX al formato necesario para
        persistir en la tabla de la DB.
        """
        fecha = fecha_csv.split("/")
        fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
        return date.strftime(fecha_op, '%Y-%m-%d')

    def importe_db(self, importe_csv):
        """
        Convierte los importes para la tabla de la DB.

        Convierte los importes de Ventas.csv al formato necesario para
        persistir en la tabla de la DB.
        """
        importe = importe_csv.replace(".", "")
        imp = importe.replace(",", ".")
        return "{0:.2f}".format(float(imp))

    def datos_csv(self,dato):
        """
        Convierte datos del archivo csv.

        Convierte datos del archivo csv para comparar con datos de la tabla
        para persistir en la DB.
        """
        datos_csv = str(dato[3]).zfill(5)+str(self.fecha_db(dato[0]))+\
                str(dato[5][1:5]).zfill(4)+str(dato[13]).zfill(3)
        return datos_csv

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
