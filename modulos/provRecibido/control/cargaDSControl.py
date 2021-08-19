#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# cargaDSControl.py
#
# Creado: 26/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos de la librería estandar:
import socket
import cgi
from datetime import date
from datetime import datetime
from builtins import int

# Módulos de la aplicación:
from includes.control.motorVista import MotorVista 
from modulos.provRecibido.modelo.provRecibidoModelo import ProvRecibidoModelo
from modulos.afip.modelo.afipDocumentoModelo import AfipDocumentoModelo
from modulos.afip.modelo.afipComprobanteModelo import AfipComprobanteModelo


class CargaDSControl():
    """
    Clase control del módulo provRecibido.
    
    Realiza operaciones con Comprobantes Recibidos descargados de  
    las aplicaciones de los proveedores, utilizando el patron MVC.  
    """

    
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia las clases del modelo:
        self.prov_recibido = ProvRecibidoModelo()
        self.afip_documento = AfipDocumentoModelo()
        self.afip_comprobante = AfipComprobanteModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'provRecibido'
        self.proveedor = 'DROG. DEL SUD SA'
        self.nro_doc = 30538880627
        self.archivo = './archivos/DSMovimientos.txt'
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
        self.periodo = int(0)
        self.cant_agregados = int(0)
        self.cant_actualizados = int(0)
        self.cant_cargados = int(0)
        self.cant_repetidos = int(0)
        self.linea = []
        # Consulta tablas que se utilizan en el módulo:
        self.documentos = self.afip_documento.find_all()
        self.cant_documentos = self.afip_documento.get_cantidad()
        self.comprobantes = self.afip_comprobante.find_all()
        self.cant_comprobantes = self.afip_comprobante.get_cantidad()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.documentos_dicc = {reng[1]: (reng[0], reng[1]) for reng in
                               self.documentos}
        self.comprobantes_dicc = {reng[2]: reng[0] for reng in 
                                  self.comprobantes}
        self.comprobantes_nro_dicc = {reng[0]: reng[2] for reng in
                                      self.comprobantes}
       
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
        self.datos_pg['tituloPagina'] = "Proveedores"
        self.datos_pg['usuario'] = "Alvaro"
        self.datos_pg['tituloBadge'] = "Comprobantes"
        # Obtiene la cantidad de registros de la tabla para badge:
        self.prov_recibido.count()
        self.datos_pg['cantidad'] = self.prov_recibido.get_cantidad()
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonCargar"]
        # Selecciona las acciones:
        if "bt_cargar" in self.form: self.accion = "Cargar"
        elif "bt_conf_cargar" in self.form: self.accion = "ConfCargar" 
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_agregados = self.cant_cargados = self.cant_repetidos = 0
       
        # Acción para iniciar:
        if self.accion == "Iniciar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Comprobantes de Proveedores")
            self.datos_pg['info'] = ("Permite cargar datos desde un archivo, "
                        "descargado de la app del proveedor, en la tabla " 
                        "seleccionando con los botones.")
            # Agrega las alertas:
            self.alertas.append("alertaInfo")
            self.datos_pg["alertaInfo"] = ("Carga datos de "+self.proveedor+". "
                        "Seleccione una acción con los <b>BOTONES</b>.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para cargar:
        if self.accion == "Cargar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Comprobantes de Proveedores")
            self.datos_pg['info'] = ("Carga comprobantes de proveedores en la"
                                     " tabla desde el archivo csv descargado"
                                     " de la aplicación del proveedor. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Agrega las alertas:
            self.alertas.append("alertaAdvertencia")
            self.datos_pg["alertaAdvertencia"] = ("Carga comprobantes de "
                        +self.proveedor+" desde el archivo <b>"
                        +self.archivo+"</b>. Confirme el evento.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfCargar",]
            # Carga el TXT:
            txtfile = open(self.archivo, "r")
            arch = txtfile.readlines()
            cant_reg = sum(1 for dato in arch)
            txtfile.close()
            # Verifica si existe el CSV:
            if cant_reg > 0:
                # Arma los datos para la vista:
                self.contenidos.append("cargarDatos")
                self.datos_pg["cantReg"] = cant_reg
                self.datos_pg["cantCargados"] = 0
                self.datos_pg["cantRepetidos"] = 0
                self.datos_pg["cantAgregados"] = 0
                self.datos_pg["proveedor"] = self.proveedor
            else:
                # ---- CSV vacio ---- :
                # Agrega las alertas:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("El archivo "
                    +self.archivo+" esta vacio. <b>VERIFICAR !!!</b>.") 
            # Muestra la vista:
            self.muestra_vista()            
        # Acción para confirmar cargar:
        if self.accion == "ConfCargar":
            # Recibe datos por POST:
            cant_reg = self.form.getvalue("cant_reg")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Carga Comprobantes de Proveedores")
            self.datos_pg['info'] = ("Carga comprobantes de proveedores en la"
                                     " tabla desde el archivo csv descargado"
                                     " de la aplicación del proveedor. "
                                     "Puede seleccionar otras acciones con los"
                                     " botones.")
            # Carga el TXT:
            txtfile = open(self.archivo, "r")
            arch = txtfile.readlines()
            # Busca la primer fecha del TXT y consulta MySQL:
            if self.prov_recibido.get_cantidad() > 0:
                fecha_menor = "2000-01-01"
                for dato in arch:
                    linea = dato.split()
                    fecha_txt = self.fecha_db(linea[14])
                    if fecha_txt < fecha_menor: fecha_menor = fecha_txt
                                            
                self.prov_recibido.set_fecha(fecha_menor)
                prov_recibidos = self.prov_recibido.find_all_fecha_dic()
            # Posiciona en primer registro de datos el TXT:
            txtfile.seek(0)
            arch = txtfile.readlines()
            # Si no hay registros en MySQL con fecha igual o menor a la primera
            # del archivo TXT agrega a todos:
            if self.prov_recibido.get_cantidad() == 0:
                for dato in arch:
                    linea = dato.split()
                    # Agrega los datos a tabla DB:
                    self.agrega_datos(linea)
            # Hay registros iguales en MySQL y CSV, verifico para agregar:
            else:
                # Arma una lista con datos unidos str() de los registros MySQL:
                compro = []
                for reng in prov_recibidos:
                    compro.append(str(reng[1])+str(reng[2]).zfill(4)
                                  +str(reng[3]).zfill(8)+str(reng[4]))
                # Lee el CSV y agrega en tabla si no existe el comprobante:
                for dato in arch:
                    linea = dato.split()
                    datos_csv = self.datos_csv(linea)
                    if datos_csv in compro:
                        # Existe el comprobante en la tabla de la DB:
                        self.cant_repetidos += 1
                    else:
                        # Agrega los datos a tabla DB:
                        self.agrega_datos(linea)
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
            self.datos_pg["cantReg"] = cant_reg
            self.datos_pg["cantCargados"] = self.cant_cargados
            self.datos_pg["cantRepetidos"] = self.cant_repetidos
            self.datos_pg["cantAgregados"] = self.cant_agregados
            self.datos_pg["proveedor"] = self.proveedor 
            
            # Cierra el archivo CSV:  
            txtfile.close()
            # Muestra la vista:
            self.muestra_vista() 
        
                                        
    def agrega_datos(self, dato):
        """
        Agrega datos a las tablas.
        
        Con los datos del archivo KEMovimientos.csv carga los atributos de las
        clases VO y los agrega en las tablas.
        """
        # Agrega a la tabla recibidos:
        self.carga_datos(dato)
        self.prov_recibido.insert()
        self.cant_cargados += self.prov_recibido.get_cantidad()
           
    def carga_datos(self, dato):
        """
        Carga datos al Value Object de la tabla.
        
        Con los datos del archivo DSMvimientos.txt carga los atributos de 
        ProvRecibidosVO para persistir en el modelo.
        """
        # Carga el VO con los datos del TXT:
        self.prov_recibido.set_fecha(self.fecha_db(dato[14]))
        if dato[2] == "A": tipo = 1
        elif dato[2] == "D": tipo = 2    
        elif dato[2] == "C": tipo = 3
        else: tipo = 999
        self.prov_recibido.set_tipo(tipo)
        self.prov_recibido.set_punto_venta(dato[3][:4])
        self.prov_recibido.set_numero(dato[3][5:])
        nro_doc = self.nro_doc
        self.prov_recibido.set_nro_doc_emisor(nro_doc)
        self.prov_recibido.set_importe_gravado(self.importe_db(dato[8], tipo))
        self.prov_recibido.set_importe_exento(self.importe_db(dato[9], tipo))
        self.prov_recibido.set_importe_mono(self.importe_db('0', tipo))
        self.prov_recibido.set_importe_no_grav(self.importe_db('0', tipo))
        self.prov_recibido.set_perc_gan(self.importe_db('0', tipo))
        self.prov_recibido.set_perc_iva(self.importe_db(dato[11], tipo))
        self.prov_recibido.set_perc_dgr(self.importe_db(dato[12], tipo))
        self.prov_recibido.set_perc_mun(self.importe_db('0', tipo))
        self.prov_recibido.set_impuesto_int(self.importe_db('0', tipo))
        self.prov_recibido.set_iva(self.importe_db(dato[10], tipo))
        self.prov_recibido.set_importe_total(self.importe_db(dato[13], tipo))
        self.prov_recibido.set_comentario('')
        self.prov_recibido.set_estado(int(1))
        self.prov_recibido.set_afip_rec(int(0))
        self.prov_recibido.set_rec(int(0))
        id_usuario = 1 # Va el id del USUARIO logueado
        self.prov_recibido.set_id_usuario_act(id_usuario)
        ahora = datetime.now()
        fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
        self.prov_recibido.set_fecha_act(fecha_act)
        
    def fecha_db(self, fecha_txt):
        """
        Convierte la fecha para la tabla de la DB.
        
        Convierte la fecha del csv al formato necesario para
        persistir en la tabla de la DB.
        """
        dia = fecha_txt[0:2]
        mes = fecha_txt[2:4]
        ano = fecha_txt[4:]
        fecha_op = date(int(ano), int(mes), int(dia))
        return date.strftime(fecha_op, '%Y-%m-%d')
                       
    def importe_db(self, importe_txt, tipo):
        """
        Convierte los importes para la tabla de la DB.
        
        Convierte los importes de IVA Compras PLEX al formato necesario para
        persistir en la tabla de la DB.
        """
        if tipo == 3: 
            #importe = "{0:.2f}".format(float(importe_txt))
            if int(importe_txt) > 0:
                importe = int(importe_txt) * -1
                return "{0:.2f}".format(float(importe)/100)
            else:
                return "{0:.2f}".format(float(importe_txt)/100)
        else:
            return "{0:.2f}".format(float(importe_txt)/100)
                
    def datos_csv(self,dato):
        """
        Convierte datos del archivo csv.
        
        Convierte datos del archivo csv para comparar con datos de la tabla
        para persistir en la DB.
        """  
        if dato[2] == "A": tipo = 1
        elif dato[2] == "D": tipo = 2    
        elif dato[2] == "C": tipo = 3
        else: tipo = 999
        punto_venta = dato[3][:4]
        numero = dato[3][5:]
        nro_doc = str(self.nro_doc) 
        datos_csv = str(tipo)+str(punto_venta)+str(numero)+str(nro_doc)
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