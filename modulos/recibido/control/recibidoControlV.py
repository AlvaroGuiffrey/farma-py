#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# recibidoControlV.py
#
# Creado: 21/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos de la librería estandar:
import cgi
import locale
from datetime import date

# Módulos de la aplicación:
from includes.control.motorVista import MotorVista 
from modulos.recibido.modelo.recibidoModelo import RecibidoModelo
from modulos.afipRecibido.modelo.afipRecibidoModelo import AfipRecibidoModelo
from modulos.afip.modelo.afipDocumentoModelo import AfipDocumentoModelo
from modulos.afip.modelo.afipComprobanteModelo import AfipComprobanteModelo


class RecibidoControlV():
    """
    Clase control del módulo recibido para ventana.
    
    Realiza operaciones con -Comprobantes Recibidos de Proveedores- por 
    compras realizadas, utilizando el patron MVC en una ventana pop-up.  
    """

    
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
        # Instancia las clases del modelo:
        self.recibido = RecibidoModelo()
        self.afip_recibido = AfipRecibidoModelo()
        self.afip_documento = AfipDocumentoModelo()
        self.afip_comprobante = AfipComprobanteModelo()
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'ventana'
        self.modulo = 'recibido'
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
        self.id = 0
        # Consulta tablas que se utilizan en el módulo:
        self.documentos = self.afip_documento.find_all()
        self.cant_documentos = self.afip_documento.get_cantidad()
        self.comprobantes = self.afip_comprobante.find_all()
        self.cant_comprobantes = self.afip_comprobante.get_cantidad()
        self.proveedores = self.afip_recibido.find_prov_select()
        self.cant_proveedores = self.afip_recibido.get_cantidad()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.documentos_dicc = {reng[0]: reng[1] for reng in
                               self.documentos}
        self.comprobantes_dicc = {reng[0]: reng[2] for reng in 
                                  self.comprobantes}
        self.proveedores_dicc = {reng[0]: reng[1] for reng in
                                 self.proveedores}
    # Métodos:
    def inicio(self, accion, id_tabla):
        """ 
        Inicio de la clase control para ventana.
        
        Verifica el login del usuario y nos envía al método que ejecuta las
        acciones del módulo.
        """
        self.accion = accion
        self.id = id_tabla
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
        # Agrega datos para titulos y usuario de la página:
        self.datos_pg['tituloPagina'] = "Compr. Recibidos de Prov."
        self.datos_pg['tituloBadge'] = "Comprobantes"
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge",]
        # Selecciona las acciones:
        if "bt_ver" in self.form: self.accion = "Ver"
        else: self.accion = "Ver"
              
        # Acción para Ver:
        if self.accion == "Ver":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Comprobante Recibido")
            self.datos_pg['info'] = ("Permite ver los datos de un renglón" 
                        " del listado.")
            #Arma los datos para la vista:
            self.contenidos = ["verDato",] 
            self.recibido.set_id(self.id)
            self.recibido.find()
            self.datos_pg['cantidad'] = self.recibido.get_cantidad()
            self.datos_pg['id'] = self.recibido.get_id()
            self.datos_pg['periodo'] = self.recibido.get_periodo()
            # Cambia formato a la fecha:
            fecha = self.recibido.get_fecha()
            fecha_emi = date.strftime(fecha, '%d/%m/%Y')
            self.datos_pg['fecha'] = fecha_emi
            # Reemplaza el tipo de comprobante:
            if self.recibido.get_tipo() in self.comprobantes_dicc: 
                tipo = self.comprobantes_dicc[self.recibido.get_tipo()]
            else: 
                tipo = "OTRO"
            compro = (
                tipo+"-"+str(self.recibido.get_punto_venta()).zfill(4)+"-"
                ""+str(self.recibido.get_numero()).zfill(8)
                )
            self.datos_pg['comprobante'] = compro 
            # Reemplaza el tipo de documento:
            documento = self.recibido.get_nro_doc_emisor()
            self.datos_pg['documento'] = documento
            prov = self.recibido.get_nro_doc_emisor()
            self.datos_pg['nombre'] = self.proveedores_dicc[prov]
            importe = self.recibido.get_importe_gravado()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['importeGravado'] = importe
            importe = self.recibido.get_importe_no_grav()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['importeNoGRav'] = importe
            importe = self.recibido.get_importe_exento()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['importeExento'] = importe
            importe = self.recibido.get_importe_mono()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['importeMono'] = importe
            importe = self.recibido.get_perc_gan()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['percGan'] = importe
            importe = self.recibido.get_perc_iva()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['percIva'] = importe
            importe = self.recibido.get_perc_dgr()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['percDgr'] = importe
            importe = self.recibido.get_perc_mun()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['percMun'] = importe
            importe = self.recibido.get_impuesto_int()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['impuestoInt'] = importe
            importe = self.recibido.get_iva()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['importeIva'] = importe
            importe = self.recibido.get_importe_total()
            importe = locale.format("%.2f", (importe), True)
            self.datos_pg['importeTotal'] = importe
            
            # Muestra la vista:
            self.muestra_vista()
                                            
       
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