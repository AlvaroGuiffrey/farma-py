# -*- coding: utf-8 -*-
# 
# recibidoControl.py
#
# Creado: 19/09/2019
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
from modulos.recibido.modelo.recibidoModelo import RecibidoModelo
from modulos.recibido.includes.recibidoTabla import RecibidoTabla
from modulos.recibidoIva.modelo.recibidoIvaModelo import RecibidoIvaModelo
from modulos.afipRecibido.modelo.afipRecibidoModelo import AfipRecibidoModelo
from modulos.provRecibido.modelo.provRecibidoModelo import ProvRecibidoModelo
from modulos.afipRecibido.includes.afipRecibidoPDF import AfipRecibidoPDF 
from modulos.afip.modelo.afipDocumentoModelo import AfipDocumentoModelo
from modulos.afip.modelo.afipComprobanteModelo import AfipComprobanteModelo
from includes.includes.select import Select


class RecibidoControl():
    """
    Clase control del módulo recibido.
    
    Realiza operaciones con Comprobantes Recibidos por 
    compras realizadas, utilizando el patron MVC.  
    """

    
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia las clases del modelo:
        self.recibido = RecibidoModelo()
        self.recibido_iva = RecibidoIvaModelo()
        self.afip_recibido = AfipRecibidoModelo()
        self.afip_documento = AfipDocumentoModelo()
        self.afip_comprobante = AfipComprobanteModelo()
        self.prov_recibido = ProvRecibidoModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'recibido'
        self.form = ''
        self.archivo = './archivos/IVACompras.csv'
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
        self.cant_conc_afip = int(0) 
        self.cant_conc_prov = int(0)
        self.cant_conc_otro = int(0)
        self.cant_afip = int(0)
        self.cant_prov = int(0)
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
        self.comprobantes_dicc = {reng[2]: reng[0] for reng in 
                                  self.comprobantes}
        self.comprobantes_nro_dicc = {reng[0]: reng[2] for reng in
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
        self.datos_pg['tituloPagina'] = "Compras"
        self.datos_pg['usuario'] = "Alvaro"
        self.datos_pg['tituloBadge'] = "Comprobantes"
        # Obtiene la cantidad de registros de la tabla para badge:
        self.recibido.count()
        self.datos_pg['cantidad'] = self.recibido.get_cantidad()
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar", "botonListar", 
                          "botonBuscar", "botonConciliar"]
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
        elif "bt_conciliar" in self.form: self.accion = "Conciliar"
        elif "bt_conf_conciliar" in self.form: self.accion = "ConfConciliar"
        elif "bt_editar" in self.form: self.accion = "Editar"
        elif "bt_descartar" in self.form: self.accion = "Descartar"
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_agregados = self.cant_cargados = self.cant_repetidos = 0
       
        # Acción para iniciar:
        if self.accion == "Iniciar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tabla de Comprobantes Recibidos")
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
            self.datos_pg['tituloPanel'] = ("Carga Comprobantes Recibidos")
            self.datos_pg['info'] = ("Carga comprobantes recibidos en la"
                                     " tabla desde el archivo IVACompras.csv"
                                     " descargado de PLEX. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Agrega las alertas:
            self.alertas.append("alertaAdvertencia")
            self.datos_pg["alertaAdvertencia"] = ("Carga comprobantes recibi"
                        "dos desde el archivo <b>IVACompras.csv"
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
                self.datos_pg["cantCargados"] = 0
                self.datos_pg["cantRepetidos"] = 0
                self.datos_pg["cantAgregados"] = 0
                self.contenidos.append("periodoOpcion")
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
            self.periodo = self.form.getvalue("periodo")
            cant_csv = self.form.getvalue("cant_csv")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Comprobantes Recibidos")
            self.datos_pg['info'] = ("Carga comprobantes recibidos en la"
                                     " tabla desde el archivo IVACompras.csv"
                                     " descargado de PLEX/Iva Compras. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Carga el CSV:
            csvfile = open(self.archivo, newline="")
            arch = csv.reader(csvfile, delimiter=",")
            next(arch)
            # Busca la primer fecha del CSV y consulta MySQL:
            if self.recibido.get_cantidad() > 0:
                fecha_menor = "2000-01-01"
                for dato in arch:
                    fecha_csv = self.fecha_db(dato[0])
                    if fecha_csv < fecha_menor: fecha_menor = fecha_csv
                                            
                self.recibido.set_fecha(fecha_menor)
                recibidos = self.recibido.find_all_fecha_dic()
            
            # Posiciona en primer registro de datos el CSV:
            csvfile.seek(0)
            arch = csv.reader(csvfile, delimiter=",")
            next(arch)
            
            # Si no hay registros en MySQL con fecha igual o menor a la primera
            # del archivo CSV agrega a todos:
            if self.recibido.get_cantidad() == 0:
                for dato in arch:
                    # Agrega los datos a tabla DB:
                    self.agrega_datos(dato)
                    
            # Hay registros iguales en MySQL y CSV, verifico para agregar:
            else:
                # Arma una lista con datos unidos str() de los registros MySQL:
                compro = []
                for reng in recibidos:
                    compro.append(str(reng[1])+str(reng[2]).zfill(4)
                                  +str(reng[3]).zfill(8)+str(reng[4]))
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
            self.datos_pg["cantAgregados"] = self.cant_agregados
            
            # Cierra el archivo CSV:  
            csvfile.close()
            # Muestra la vista:
            self.muestra_vista() 
        # Acción para listar:    
        if self.accion == "Listar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Comprobantes Recibidos")
            self.datos_pg['info'] = ("Realiza un listado con datos de la " 
                        "tabla.<br>Seleccione en <b>Opciones del listado</b> "
                         "un rango de fechas.")
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
            opciones['periodo'] = self.form.getvalue("periodo")
            opciones['tipo'] = self.form.getvalue("tipo")
            opciones['numero'] = self.form.getvalue("numero")
            opciones['prov'] = self.form.getvalue("prov")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Listado de Comprobantes Recibidos")
            self.datos_pg['info'] = ("Listado de datos de la tabla, dentro "
                                     "del rango de fechas seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la tabla para listar:
            datos = self.recibido.find_listar(opciones)
            self.datos_pg["cantidad"] = self.recibido.get_cantidad()
            # Arma la tabla para listar:
            tabla = RecibidoTabla()
            tabla.arma_tabla(datos, opciones, self.comprobantes_nro_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para buscar:
        if self.accion == "Buscar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Comprobantes Recibidos")
            self.datos_pg['info'] = ("Realiza una busqueda de Comprobantes " 
                        "Recibidos de proveedores.<br>Seleccione en <b>"
                        "Opciones del listado</b> los parámetros para la"
                        " acción.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonBorrar", "botonConfBuscar"]
            # Arma los datos para la vista:
            self.opciones.append("buscarOpcion")
            # Carga los select para las opciones:
            # Select del tipo de comprobante AFIP:
            datos = self.comprobantes_nro_dicc
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
            periodo = self.form.getvalue("periodo")
            if periodo == None: periodo = 0
            tipo = self.form.getvalue("tipo")
            numero = self.form.getvalue("numero")
            if numero == None: numero = 0
            prov = self.form.getvalue("prov")
            # Arma las opciones de búsqueda:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            opciones['periodo'] = periodo
            opciones['numero'] = numero
            opciones['tipo'] = tipo
            opciones['prov'] = prov
            if int(prov) > 0:
                opciones['nombre_prov'] = self.proveedores_dicc[int(prov)]
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Buscar Comprobantes Recibidos")
            self.datos_pg['info'] = ("Comprobantes Recibidos de proveedores "
                                     "encontrados segun las opciones "
                                     "de busqueda seleccionadas.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonDescargarPDF",]
            # Encuentra los datos de la busqueda para listar:
            datos = self.recibido.find_buscar(opciones)
            self.datos_pg["cantidad"] = self.recibido.get_cantidad()
            # Arma la tabla para listar:
            tabla = RecibidoTabla()
            tabla.arma_tabla(datos, opciones, self.comprobantes_nro_dicc)
            self.tablas = ["tabla",]
            # Muestra la vista:
            self.muestra_vista()
            
        # Acción para descargar:
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
        # Acción para conciliar:    
        if self.accion == "Conciliar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Conciliación de Comprobantes"
                                            " Recibidos")
            self.datos_pg['info'] = ("Realiza una conciliación de datos de " 
                        "la tabla con los comprobantes recibidos de AFIP y "
                        "de los proveedores.<br>Seleccione en <b>Opciones "
                        "de fechas</b> el rango a conciliar.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfConciliar",]
            # Arma los datos para la vista:
            self.opciones.append("fechasOpcion")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar el listado:
        if self.accion == "ConfConciliar":
            # Recibe datos por POST:
            fechas = self.form.getvalue("fechas")
            fechas = fechas.split(" - ")
            # Arma las opciones de listar:
            opciones = {}
            opciones['fecha_d'] = fechas[0]
            opciones['fecha_h'] = fechas[1]
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Conciliación de Comprobantes"
                                            " Recibidos")
            self.datos_pg['info'] = ("Realiza una conciliación de datos de " 
                        "la tabla con los comprobantes recibidos de AFIP y "
                        "de los proveedores.<br>Seleccione en <b>Opciones "
                        "de fechas</b> el rango a conciliar.")
            # Encuentra los datos de la tabla para conciliar:
            datos = self.recibido.find_conciliar(opciones)
            self.datos_pg["cantidad"] = self.recibido.get_cantidad()
            # Arma diccionario con datos de tabla afip_recibidos:
            datos_afip = self.afip_recibido.find_conciliar(opciones)
            self.cant_afip = self.afip_recibido.get_cantidad()
            afip_rec_dicc = {str(reng[1])+str(reng[2]).zfill(4)
                             +str(reng[3]).zfill(8)+str(reng[4]): (reng[0],
                             reng[5], reng[6], reng[7], reng[8])
                             for reng in datos_afip}
            # Arma diccionario con datos de tabla prov_recibidos:
            datos_prov = self.prov_recibido.find_conciliar(opciones)
            self.cant_prov = self.prov_recibido.get_cantidad()
            prov_rec_dicc = {str(reng[1])+str(reng[2]).zfill(4)
                             +str(reng[3]).zfill(8)+str(reng[4]): (reng[0],
                             reng[5], reng[6], reng[7], reng[8]) 
                             for reng in datos_prov}
            # Concilia los datos con otras tablas:
            self.cant_conc_afip = self.cant_conc_prov = self.cant_actualizados\
            = self.cant_conc_otro = 0
            # Arma la clave para consultar el diccinario:
            for dato in datos:
                clave_dicc = str(dato[1])+str(dato[2]).zfill(4)\
                             +str(dato[3]).zfill(8)+str(dato[4])
                # Setea valores a indicadores y RecibidoVO:             
                flag_afip = flag_prov = 'no'
                self.recibido.set_afip_rec(dato[7])
                self.recibido.set_prov_rec(dato[8]) 
                # Conculta diccionario AFIP y verifica consistencia datos:
                if clave_dicc in afip_rec_dicc:
                    flag_afip = 'si'
                    self.recibido.set_afip_rec(int(1)) 
                    self.afip_recibido.set_rec(int(1))
                    self.afip_recibido.set_prov_rec(afip_rec_dicc[clave_dicc][4])
                    # Cambio signo a las notas de crédito de afip_recibidos:
                    iva_afip = afip_rec_dicc[clave_dicc][1]
                    total_afip = afip_rec_dicc[clave_dicc][2]
                    if dato[1] == 3 or dato[1] == 13 or dato[1] == 53:
                        iva_afip = iva_afip * -1
                        total_afip = total_afip * -1
                    # Verifica consistencia de los importes iva y total:
                    if dato[5] != iva_afip:
                        self.recibido.set_afip_rec(int(2))
                        self.afip_recibido.set_rec(int(2))
                    if dato[6] != total_afip:
                        self.recibido.set_afip_rec(int(2))
                        self.afip_recibido.set_rec(int(2))
                # Conculta diccionario Prov y verifica consistencia datos:
                if clave_dicc in prov_rec_dicc:
                    flag_prov = 'si'
                    self.recibido.set_prov_rec(int(1))
                    self.prov_recibido.set_rec(int(1))
                    self.prov_recibido.set_afip_rec(prov_rec_dicc[clave_dicc][3])
                    iva_prov = prov_rec_dicc[clave_dicc][1]
                    total_prov = prov_rec_dicc[clave_dicc][2]
                    # Verifica consistencia de los importes iva y total:
                    if dato[5] != iva_prov:
                        self.recibido.set_prov_rec(int(2))
                        self.prov_recibido.set_rec(int(2))
                    if dato[6] != total_prov:
                        self.recibido.set_prov_rec(int(2))
                        self.prov_recibido.set_rec(int(2))
                # Si esta en ambos diccionarios verifica consistencia datos:
                if flag_afip == 'si' and flag_prov == 'si':
                    self.afip_recibido.set_prov_rec(int(1))
                    self.prov_recibido.set_afip_rec(int(1))
                    if iva_afip != iva_prov:
                        self.afip_recibido.set_prov_rec(int(2))
                        self.prov_recibido.set_afip_rec(int(2))
                    if total_afip != total_prov:
                        self.afip_recibido.set_prov_rec(int(2))
                        self.prov_recibido.set_afip_rec(int(2))
                # Persiste sobre las tablas:
                id_usuario = 1 # Va el id del USUARIO logueado
                ahora = datetime.now()
                fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
                
                if flag_afip == 'si' or flag_prov == 'si':
                    self.recibido.set_id(dato[0])
                    self.recibido.set_id_usuario_act(id_usuario)
                    self.recibido.set_fecha_act(fecha_act)
                    self.recibido.update_conciliar()
                    self.cant_actualizados += self.recibido.get_cantidad()
                if flag_afip == 'si':
                    self.afip_recibido.set_id(afip_rec_dicc[clave_dicc][0])
                    self.afip_recibido.set_id_usuario_act(id_usuario)
                    self.afip_recibido.set_fecha_act(fecha_act)    
                    self.afip_recibido.update_conciliar()
                    self.cant_conc_afip += self.afip_recibido.get_cantidad()
                if flag_prov == 'si':
                    self.prov_recibido.set_id(prov_rec_dicc[clave_dicc][0])
                    self.prov_recibido.set_id_usuario_act(id_usuario)
                    self.prov_recibido.set_fecha_act(fecha_act)
                    self.prov_recibido.update_conciliar()
                    self.cant_conc_prov += self.prov_recibido.get_cantidad()
            # Concilia afip_recibidos con prov_recibidos:
            # Arma diccionario con datos de tabla afip_recibidos:
            datos_afip = self.afip_recibido.find_conciliar(opciones)
            afip_rec_dicc = {str(reng[1])+str(reng[2]).zfill(4)
                             +str(reng[3]).zfill(8)+str(reng[4]): (reng[0],
                             reng[5], reng[6], reng[7], reng[8])
                             for reng in datos_afip}
            # Arma diccionario con datos de tabla prov_recibidos:
            datos_prov = self.prov_recibido.find_conciliar(opciones)
            prov_rec_dicc = {str(reng[1])+str(reng[2]).zfill(4)
                             +str(reng[3]).zfill(8)+str(reng[4]): (reng[0],
                             reng[5], reng[6], reng[7], reng[8]) 
                             for reng in datos_prov}
            # Concilia las tablas:
            afip_dicc = afip_rec_dicc.items()
            for clave, valor in afip_dicc:
                # Si no esta conciliado prov_rec, verifica:
                if int(valor[4]) == 0:
                    if clave in prov_rec_dicc:
                        # Cambio signo a las notas de crédito de afip_recibidos:
                        iva_afip = valor[1]
                        total_afip = valor[2]
                        tipo = int(clave[:-23])     
                        if tipo == 3 or tipo == 13 or dato[1] == 53:
                            iva_afip = iva_afip * -1
                            total_afip = total_afip * -1
                        # Verifica los importes de iva y total:
                        iva_prov = prov_rec_dicc[clave][1]
                        total_prov = prov_rec_dicc[clave][2]
                        self.afip_recibido.set_prov_rec(int(1))
                        self.prov_recibido.set_afip_rec(int(1))
                        if iva_afip != iva_prov:
                            self.afip_recibido.set_prov_rec(int(2))
                            self.prov_recibido.set_afip_rec(int(2))
                        if total_afip != total_prov:
                            self.afip_recibido.set_prov_rec(int(2))
                            self.prov_recibido.set_afip_rec(int(2))
                        # Persiste sobre las tablas:
                        id_usuario = 1 # Va el id del USUARIO logueado
                        ahora = datetime.now()
                        fecha_act = datetime.strftime(ahora, 
                                                      '%Y-%m-%d %H:%M:%S')
                        # Tabla afip_recibidos:
                        self.afip_recibido.set_id(valor[0])
                        self.afip_recibido.set_rec(valor[3])
                        self.afip_recibido.set_id_usuario_act(id_usuario)
                        self.afip_recibido.set_fecha_act(fecha_act)
                        self.afip_recibido.update_conciliar()
                        # Tabla prov_recibidos:
                        self.prov_recibido.set_id(prov_rec_dicc[clave][0])
                        self.prov_recibido.set_rec(prov_rec_dicc[clave][4])
                        self.prov_recibido.set_id_usuario_act(id_usuario)
                        self.prov_recibido.set_fecha_act(fecha_act)
                        self.prov_recibido.update_conciliar()
                        self.cant_conc_otro += self.prov_recibido.get_cantidad()
            # Arma los datos para la vista:
            self.contenidos.append("conciliarDatos")
            self.datos_pg["fechaD"] = fechas[0]
            self.datos_pg["fechaH"] = fechas[1]
            self.datos_pg["cantActualizados"] = self.cant_actualizados
            self.datos_pg["cantAfip"] = self.cant_afip
            self.datos_pg["cantProv"] = self.cant_prov
            self.datos_pg["cantConcAfip"] = self.cant_conc_afip
            self.datos_pg["cantConcProv"] = self.cant_conc_prov
            self.datos_pg["cantConcOtro"] = self.cant_conc_otro
            
            # Muestra la vista:
            self.muestra_vista()
                                        
    def agrega_datos(self, dato):
        """
        Agrega datos a las tablas.
        
        Con los datos del archivo IVACompras.csv carga los atributos de las
        clases VO y los agrega en las tablas.
        """
        # Agrega a la tabla recibidos:
        self.carga_datos(dato)
        self.recibido.insert()
        self.cant_cargados += self.recibido.get_cantidad()
        # Agrega a la tabla recibidos_iva:
        if float(self.importe_db(dato[13])) > 0:
            id_condicion = 4 # id tabla afip_condición_iva 10,5%
            self.carga_datos_iva(dato[13], id_condicion) 
            self.recibido_iva.insert()
            self.cant_agregados += self.recibido_iva.get_cantidad()
        if float(self.importe_db(dato[14])) > 0:
            id_condicion = 5 # id tabla afip_condición_iva 21%
            self.carga_datos_iva(dato[14], id_condicion) 
            self.recibido_iva.insert()
            self.cant_agregados += self.recibido_iva.get_cantidad()
        if float(self.importe_db(dato[15])) > 0:
            id_condicion = 6 # id tabla afip_condición_iva 27%
            self.carga_datos_iva(dato[15], id_condicion) 
            self.recibido_iva.insert()
            self.cant_agregados += self.recibido_iva.get_cantidad()
            
    
    def carga_datos(self, dato):
        """
        Carga datos al Value Object de la tabla.
        
        Con los datos del archivo IVACompras.csv carga los atributos de 
        RecibidosVO para persistir en el modelo.
        """
        # Carga el VO con los datos del CSV:
        self.recibido.set_periodo(self.periodo)
        self.recibido.set_fecha(self.fecha_db(dato[0]))
        compro = dato[1].split('-')
        compro_ot = compro[1].split(' ')
        if compro[0] in self.comprobantes_dicc:
            tipo = self.comprobantes_dicc[compro[0]]
        else:
            tipo = 999
        self.recibido.set_tipo(tipo)
        self.recibido.set_punto_venta(compro_ot[0])
        self.recibido.set_numero(compro_ot[1])
        nro_doc = dato[2].replace('-', '')
        self.recibido.set_nro_doc_emisor(nro_doc)
        self.recibido.set_importe_gravado(self.importe_db(dato[5]))
        if dato[4] == "MT":
            self.recibido.set_importe_exento(self.importe_db('0'))
            self.recibido.set_importe_mono(self.importe_db(dato[6]))
        else:
            self.recibido.set_importe_exento(self.importe_db(dato[6]))
            self.recibido.set_importe_mono(self.importe_db('0'))
        self.recibido.set_importe_no_grav(self.importe_db(dato[7]))
        self.recibido.set_perc_gan(self.importe_db(dato[8]))
        self.recibido.set_perc_iva(self.importe_db(dato[9]))
        self.recibido.set_perc_dgr(self.importe_db(dato[10]))
        self.recibido.set_perc_mun(self.importe_db(dato[12]))
        self.recibido.set_impuesto_int(self.importe_db(dato[11]))
        iva = float(self.importe_db(dato[13])) + float(self.importe_db(dato[14])) + float(self.importe_db(dato[15]))
        iva = "{0:.2f}".format(float(iva))
        self.recibido.set_iva(iva)
        self.recibido.set_importe_total(self.importe_db(dato[16]))
        self.recibido.set_comentario('')
        self.recibido.set_estado(int(1))
        self.recibido.set_afip_rec(int(0))
        self.recibido.set_prov_rec(int(0))
        id_usuario = 1 # Va el id del USUARIO logueado
        self.recibido.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.recibido.set_fecha_act(fecha_act) 
        
    def carga_datos_iva(self, dato, id_condicion):
        """
        Carga datos al Value Object de la tabla.
        
        Con algunos datos del archivo IVACompras.csv carga los atributos de 
        RecibidosIvaVO para persistir en el modelo.
        """
        # Carga el VO con los datos del CSV: 
        self.recibido_iva.set_id_recibido(self.recibido.get_id_insert())
        self.recibido_iva.set_condicion(id_condicion)
        self.recibido_iva.set_neto(self.importe_db('0'))
        self.recibido_iva.set_iva(self.importe_db(dato))
        self.recibido_iva.set_estado('1')
        id_usuario = 1 # Va el id del USUARIO logueado
        self.recibido_iva.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.recibido_iva.set_fecha_act(fecha_act)
                        
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
        
        Convierte los importes de IVA Compras PLEX al formato necesario para
        persistir en la tabla de la DB.
        """
        imp = importe_csv.replace(',', '.')
        return "{0:.2f}".format(float(imp))
        
    def datos_csv(self,dato):
        """
        Convierte datos del archivo csv.
        
        Convierte datos del archivo csv para comparar con datos de la tabla
        para persistir en la DB.
        """  
        compro = dato[1].split('-')
        compro_ot = compro[1].split(' ')
        if compro[0] in self.comprobantes_dicc:
            tipo = self.comprobantes_dicc[compro[0]]
        else:
            tipo = 999
        nro_doc = dato[2].replace('-', '')
        datos_csv = str(tipo)+str(compro_ot[0])+str(compro_ot[1])+\
            str(nro_doc)
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
        