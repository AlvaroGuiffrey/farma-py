# -*- coding: utf-8 -*-
#
# afipRecibidoControl.py
#
# Creado: 27/08/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
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
from modulos.afipRecibido.modelo.afipRecibidoModelo import AfipRecibidoModelo
from modulos.afipRecibido.includes.afipRecibidoTabla import AfipRecibidoTabla
from modulos.afipRecibido.includes.afipRecibidoPDF import AfipRecibidoPDF
from modulos.afip.modelo.afipDocumentoModelo import AfipDocumentoModelo
from modulos.afip.modelo.afipComprobanteModelo import AfipComprobanteModelo
from modulos.provRecibido.modelo.provRecibidoModelo import ProvRecibidoModelo
from includes.includes.select import Select


class AfipRecibidoControl():
    """
    Clase control del módulo afipRecibido.

    Realiza operaciones con -Mis Comprobantes Recibidos (AFIP)- por
    compras realizadas, utilizando el patron MVC.
    """


    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia las clases del modelo:
        self.afip_recibido = AfipRecibidoModelo()
        self.afip_documento = AfipDocumentoModelo()
        self.afip_comprobante = AfipComprobanteModelo()
        self.prov_recibido = ProvRecibidoModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'afipRecibido'
        self.archivo = './archivos/AfipMovRec.csv'
        self.form = ''
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
        self.cant_cargados = int(0)
        self.cant_repetidos = int(0)
        self.linea = []
        # Consulta tablas que se utilizan en el módulo:
        self.documentos = self.afip_documento.find_all()
        self.cant_documentos = self.afip_documento.get_cantidad()
        self.comprobantes = self.afip_comprobante.find_all()
        self.cant_comprobantes = self.afip_comprobante.get_cantidad()
        self.proveedores = self.afip_recibido.find_prov_select()
        self.cant_proveedores = self.afip_recibido.get_cantidad()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.documentos_dicc = {reng[1]: (reng[0], reng[1]) for reng in
                               self.documentos}
        self.comprobantes_dicc = {reng[0]: reng[2] for reng in
                                  self.comprobantes}
        self.proveedores_dicc = {reng[0]: reng[1] for reng in
                                 self.proveedores}
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
        self.datos_pg['tituloPagina'] = "AFIP Compr. Recibidos"
        self.datos_pg['usuario'] = "Alvaro" # Usuario del login
        self.datos_pg['tituloBadge'] = "Comprobantes"
        # Obtiene la cantidad de registros de la tabla para badge:
        self.afip_recibido.count()
        self.datos_pg['cantidad'] = self.afip_recibido.get_cantidad()
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar", "botonListar",
                          "botonBuscar"]
        # Selecciona las acciones:
        if "bt_cargar" in self.form: self.accion = "Cargar"
        elif "bt_conf_cargar" in self.form: self.accion = "ConfCargar"
        elif "bt_listar" in self.form: self.accion = "Listar"
        elif "bt_conf_listar" in self.form: self.accion = "ConfListar"
        elif "bt_buscar" in self.form: self.accion = "Buscar"
        elif "bt_conf_buscar" in self.form: self.accion = "ConfBuscar"
        elif "bt_descargar_pdf" in self.form: self.accion = "DescargarPDF"
        elif "bt_editar" in self.form: self.accion = "Editar"
        elif "bt_descartar" in self.form: self.accion = "Descartar"
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_agregados = self.cant_repetidos = 0

        # Acción para iniciar:
        if self.accion == "Iniciar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tabla de Comprobantes Recibidos"
                                            " AFIP")
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
            self.datos_pg['tituloPanel'] = ("Carga Comprobantes Recibidos"
                                            " AFIP")
            self.datos_pg['info'] = ("Carga comprobantes recibidos de AFIP en"
                                     " la tabla desde el archivo AfipMovRec.csv"
                                     " descargado de AFIP/Mis Comprobantes. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Agrega las alertas:
            self.alertas.append("alertaAdvertencia")
            self.datos_pg["alertaAdvertencia"] = ("Carga comprobantes recibi"
                        "dos de AFIP desde el archivo <b>AfipMovRec.csv"
                        "</b>. Confirme el evento.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfCargar",]
            # Carga el CSV:
            csvfile = open(self.archivo, newline="")
            arch = csv.reader(csvfile, delimiter=",")
            next(arch)
            cant_csv = sum(1 for dato in arch)
            csvfile.close()
            # Verifica si existe el CSV:
            if cant_csv > 0:
                self.contenidos.append("cargarDatos")
                self.datos_pg["cantCsv"] = cant_csv
                self.datos_pg["cantAgregados"] = 0
                self.datos_pg["cantCargados"] = 0
                self.datos_pg["cantRepetidos"] = 0
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
            self.datos_pg['tituloPanel'] = ("Carga Comprobantes Recibidos"
                                            " AFIP")
            self.datos_pg['info'] = ("Carga comprobantes recibidos de AFIP en"
                                     " la tabla desde el archivo AfipMovRec.csv"
                                     " descargado de AFIP/Mis Comprobantes. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Carga el CSV:
            csvfile = open(self.archivo, newline="")
            arch = csv.reader(csvfile, delimiter=",")
            next(arch)
            # Busca la primer fecha del CSV y consulta MySQL:
            fecha_menor = "2000-01-01"
            for dato in arch:
                fecha_csv = self.fecha_db(dato[0])
                if fecha_csv < fecha_menor: fecha_menor = fecha_csv

            self.afip_recibido.set_fecha(fecha_menor)
            recibidos = self.afip_recibido.find_all_fecha_dic()
            # Posiciona en primer registro de datos el CSV:
            csvfile.seek(0)
            arch = csv.reader(csvfile, delimiter=",")
            next(arch)
            # Si no hay registros en MySQL con fecha igual o menor a la primera
            # del archivo CSV agrega a todos:
            if self.afip_recibido.get_cantidad() == 0:
                for dato in arch:
                    # Carga el VO con los datos del CSV y agrega a tabla DB:
                    self.carga_datos(dato)
                    self.afip_recibido.insert()
                    self.cant_cargados += self.afip_recibido.get_cantidad()
            # Hay registros iguales en MySQL y CSV, verifico para agregar:
            else:
                # Arma una lista con datos unidos str() de los registros MySQL:
                compro = []
                for reng in recibidos:
                    compro.append(str(reng[1])+str(reng[2])+str(reng[3])
                                  +str(reng[4]))
                # Lee el CSV y agrega en tabla si no existe el comprobante:
                for dato in arch:
                    if str(self.tipo_db(dato[1]))+str(dato[2])+str(dato[3])\
                        +str(dato[7]) in compro:
                        # Existe el comprobante en la tabla de la DB:
                        self.cant_repetidos += 1
                    else:
                        # Carga el VO con los datos del CSV y agrega a tabla DB:
                        self.carga_datos(dato)
                        self.afip_recibido.insert()
                        self.cant_cargados += self.afip_recibido.get_cantidad()

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
            self.datos_pg['tituloPanel'] = ("Listado de Comprobantes Recibidos"
                                            " AFIP")
            self.datos_pg['info'] = ("Realiza un listado con datos de la "
                        "tabla.<br>Seleccione en <b>Opciones del listado</b> "
                         "un rango de fechas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfListar",]
            # Arma los datos para la vista:
            self.opciones.append("listarOpcion")
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
            opciones['tipo'] = self.form.getvalue("tipo")
            opciones['numero'] = self.form.getvalue("numero")
            opciones['prov'] = self.form.getvalue("prov")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Comprobantes Recibidos"
                                            " AFIP")
            self.datos_pg['info'] = ("Listado con datos de la tabla, dentro "
                                     "del rango de fechas seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.afip_recibido.find_listar(opciones)
            self.datos_pg["cantidad"] = self.afip_recibido.get_cantidad()
            # Encuentra los comentarios de tabla prov_recibidos:
            comentarios_prov = self.prov_recibido.find_all_comentario(opciones)
            # Arma la tabla para listar:
            tabla = AfipRecibidoTabla()
            tabla.arma_tabla(datos, opciones, comentarios_prov,
                             self.comprobantes_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para buscar:
        if self.accion == "Buscar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Comprobantes Recibidos"
                                            " AFIP")
            self.datos_pg['info'] = ("Realiza una busqueda de Comprobantes "
                        "Recibidos de AFIP.<br>Seleccione en <b>Opciones del "
                        "listado</b> los parámetros para la acción.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfBuscar"]
            # Arma los datos para la vista:
            self.opciones.append("buscarOpcion")
            # Carga los select para las opciones:
            # Select del tipo de comprobante AFIP:
            datos = self.comprobantes_dicc
            cantidad = self.cant_comprobantes
            nombre = 'tipo'
            select_tipo = Select()
            select_tipo.arma_select(datos, cantidad, nombre)
            self.componentes += ["select_tipo",]
            # Select del tipo de comprobante AFIP:
            datos = self.proveedores_dicc
            cantidad = self.cant_proveedores
            nombre = 'prov'
            select_tipo = Select()
            select_tipo.arma_select(datos, cantidad, nombre)
            self.componentes += ["select_prov",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar buscar:
        if self.accion == "ConfBuscar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            tipo = self.form.getvalue("tipo")
            numero = self.form.getvalue("numero")
            if numero == None: numero = 0
            prov = self.form.getvalue("prov")
            # Arma las opciones de búsqueda:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['numero'] = numero
            opciones['tipo'] = tipo
            opciones['prov'] = prov
            if int(prov) > 0:
                opciones['nombre_prov'] = self.proveedores_dicc[int(prov)]
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Comprobantes Recibidos"
                                            " AFIP")
            self.datos_pg['info'] = ("Comprobantes Recibidos de AFIP "
                                     "encontrados segun las opciones "
                                     "de busqueda seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la busqueda para listar:
            datos = self.afip_recibido.find_buscar(opciones)
            self.datos_pg["cantidad"] = self.afip_recibido.get_cantidad()
            # Encuentra los comentarios de tabla prov_recibidos:
            comentarios_prov = self.prov_recibido.find_all_comentario(opciones)
            # Arma la tabla para listar:
            tabla = AfipRecibidoTabla()
            tabla.arma_tabla(datos, opciones, comentarios_prov,
                             self.comprobantes_dicc)

            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()

        # Acción para descargar PDF:
        if self.accion == "DescargarPDF":
            # Recibe datos por POST:
            # Arma las opciones de búsqueda y el detalle PDF:
            opciones = {}
            opciones['fecha_d'] = self.form.getvalue("fecha_d")
            opciones['fecha_h'] = self.form.getvalue("fecha_h")
            detalle_pdf = ("Desde: "+str(opciones['fecha_d'])+" - "
                           "Hasta: "+str(opciones['fecha_h'])+" ")
            if self.form.getvalue("tipo"):
                opciones['tipo'] = self.form.getvalue("tipo")
                if int(opciones['tipo']) > 0:
                    tipo = self.comprobantes_dicc[int(opciones['tipo'])]
                    detalle_pdf += ("- Tipo: "+str(tipo)+" ")
            if self.form.getvalue("numero"):
                opciones['numero'] = self.form.getvalue("numero")
                if int(opciones['numero']) > 0:
                    numero = opciones['numero']
                    numero = numero.zfill(8)
                    detalle_pdf += ("- Nro: "+str(numero)+" ")
            if self.form.getvalue("prov"):
                opciones['prov'] = self.form.getvalue("prov")
                if int(opciones['prov']) > 0:
                    opciones['nombre_prov'] = self.proveedores_dicc[
                        int(opciones['prov'])]
                    detalle_pdf += ("- de: "+str(opciones['nombre_prov'])+"")
            # Consulta la tabla:
            datos = self.afip_recibido.find_descargar(opciones)
            self.datos_pg["cantidad"] = self.afip_recibido.get_cantidad()
            # Escribe y guarda el archivo PDF:
            pdf = AfipRecibidoPDF()
            pdf.escribir_pdf(datos, detalle_pdf, self.comprobantes_dicc)

            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Descarga Listado en PDF")
            self.datos_pg['info'] = ("Realiza la descarga del listado de"
                        " Comprobantes Recibidos de AFIP en un archivo PDF "
                        "en el directorio: 'archivos' de la aplicación. <br>"
                        "También lo puede abrir en el navegador con el boton"
                        " 'Abrir PDF'.")
            # Agrega las alertas:
            self.alertas.append("alertaSuceso")
            self.datos_pg["alertaSuceso"] = ("Se descargó el archivo PDF "
                    "con <b>EXITO !!!</b>.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonAbrirRecibidosPDF",]
            # Muestra la vista:
            self.muestra_vista()
                                        
    def carga_datos(self, dato):
        """
        Carga datos al Value Object de la tabla.

        Con los datos del archivo AfipMovRec.csv carga los atributos de
        AfipRecibidosVO para persistir en el modelo.
        """
        # Carga el VO con los datos del CSV:
        self.afip_recibido.set_fecha(self.fecha_db(dato[0]))
        self.afip_recibido.set_tipo(self.tipo_db(dato[1]))
        self.afip_recibido.set_punto_venta(dato[2])
        self.afip_recibido.set_numero_d(dato[3])
        self.afip_recibido.set_numero_h(dato[4])
        self.afip_recibido.set_cai(dato[5])
        self.afip_recibido.set_tipo_doc_emisor(self.tipo_doc_db(dato[6]))
        self.afip_recibido.set_nro_doc_emisor(dato[7])
        self.afip_recibido.set_nombre_emisor(dato[8])
        self.afip_recibido.set_tipo_cambio(dato[9])
        self.afip_recibido.set_moneda(dato[10])
        if dato[11] == "": imp = "{0:.2f}".format(float(0))
        else: imp = "{0:.2f}".format(float(dato[11]))
        self.afip_recibido.set_importe_gravado(imp)
        if dato[12] == "": imp = "{0:.2f}".format(float(0))
        else: imp = "{0:.2f}".format(float(dato[12]))
        self.afip_recibido.set_importe_no_grav(imp)
        if dato[13] == "": imp = "{0:.2f}".format(float(0))
        else: imp = "{0:.2f}".format(float(dato[13]))
        self.afip_recibido.set_importe_exento(imp)
        if dato[14] == "": imp = "{0:.2f}".format(float(0))
        else: imp = "{0:.2f}".format(float(dato[14]))
        self.afip_recibido.set_iva(imp)
        imp = "{0:.2f}".format(float(dato[15]))
        self.afip_recibido.set_importe_total(imp)
        self.afip_recibido.set_comentario('')
        self.afip_recibido.set_estado('1')
        self.afip_recibido.set_rec('0')
        self.afip_recibido.set_prov_rec('0')
        id_usuario = 1 # Va el id del USURIO
        self.afip_recibido.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.afip_recibido.set_fecha_act(fecha_act)

    def fecha_db(self, fecha_afip):
        """
        Convierte la fecha para la tabla de la DB.

        Convierte la fecha de Mis Comprobantes AFIP al formato necesario para
        persistir en la tabla de la DB.
        """
        fecha = fecha_afip.split("/")
        fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
        return date.strftime(fecha_op, '%Y-%m-%d')

    def tipo_db(self, tipo):
        """
        Convierte el tipo de comprobante para la tabla de la DB.

        Convierte el tipo de Mis Comprobantes AFIP al formato necesario
        para persistir en la tabla de la DB.
        """
        tipo_db = tipo.split("-")
        return int(tipo_db[0])

    def tipo_doc_db(self, tipo_doc):
        """
        Convierte el tipo de documento para la tabla de la DB.

        Convierte el tipo de documento de Mis Comprobantes AFIP al
        formato necesario para persistir en la tabla de la DB.
        """
        if tipo_doc in self.documentos_dicc:
            return self.documentos_dicc[tipo_doc][0]
        else:
            return int(99)

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
