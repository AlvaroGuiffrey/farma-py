# -*- coding: utf-8 -*-
# 
# afipRecibidoControlV.py
#
# Creado: 13/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos de la librería estandar:
import cgi
import locale
from datetime import date
from datetime import datetime

# Módulos de la aplicación:
from includes.control.motorVista import MotorVista 
from modulos.afipRecibido.modelo.afipRecibidoModelo import AfipRecibidoModelo
from modulos.afip.modelo.afipDocumentoModelo import AfipDocumentoModelo
from modulos.afip.modelo.afipComprobanteModelo import AfipComprobanteModelo
from modulos.provRecibido.modelo.provRecibidoModelo import ProvRecibidoModelo


class AfipRecibidoControlV():
    """
    Clase control del módulo afipRecibido para ventana.
    
    Realiza operaciones con -Mis Comprobantes Recibidos (AFIP)- por 
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
        self.afip_recibido = AfipRecibidoModelo()
        self.afip_documento = AfipDocumentoModelo()
        self.afip_comprobante = AfipComprobanteModelo()
        self.prov_recibido = ProvRecibidoModelo()
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'ventana'
        self.modulo = 'afipRecibido'
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
        self.id = self.form.getvalue('id')
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
        self.datos_pg['tituloPagina'] = "AFIP Compr. Recibidos"
        self.datos_pg['tituloBadge'] = "Comprobantes"
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonEditar"]
        # Selecciona las acciones:
        if "bt_ver" in self.form: self.accion = "Ver"
        elif "bt_editar" in self.form: 
            self.accion = self.form.getvalue('bt_editar') 
        elif "bt_conf_editar" in self.form: 
            self.accion = self.form.getvalue('bt_conf_editar')
        elif "bt_volver" in self.form: 
            self.accion = "Ver"
        else: self.accion = "Ver"
              
        # Acción para Ver:
        if self.accion == "Ver":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Comprobante Recibido"
                                            " AFIP")
            self.datos_pg['info'] = ("Permite ver los datos de un renglón" 
                        " del listado.")
            #Arma los datos para la vista:
            self.contenidos = ["verDato",] 
            self.afip_recibido.set_id(self.id)
            self.afip_recibido.find()
            self.datos_pg['cantidad'] = self.afip_recibido.get_cantidad()
            self.datos_pg['id'] = self.afip_recibido.get_id()
            self.arma_vista() 
            # Muestra la vista:
            self.muestra_vista()
            
        # Acción para Editar:
        if self.accion == "Editar":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Comprobante Recibido"
                                            " AFIP")
            self.datos_pg['info'] = ("Permite editar los datos de un renglón" 
                        " del listado.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfEditar", "botonVolver"]
            #Arma los datos para la vista:
            self.contenidos = ["editarDato",] 
            self.afip_recibido.set_id(self.id)
            self.afip_recibido.find()
            self.datos_pg['cantidad'] = self.afip_recibido.get_cantidad()
            self.datos_pg['id'] = self.afip_recibido.get_id()
            self.arma_vista() 
            # Muestra la vista:
            self.muestra_vista()
            
        # Acción para confirmar editar:
        if self.accion == "ConfEditar":
            # Recibe datos por POST:
            comentario = self.form.getvalue("comentario")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Comprobante Recibido"
                                            " AFIP")
            self.datos_pg['info'] = ("Permite ver los datos editados de " 
                        "un renglón del listado.")
            #Actualiza los datos en la tabla:
            self.afip_recibido.set_id(self.id)
            self.afip_recibido.set_comentario(comentario)
            id_usuario = 1 # Va el id del USURIO
            self.afip_recibido.set_id_usuario_act(id_usuario)
            ahora = datetime.now()
            fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
            self.afip_recibido.set_fecha_act(fecha_act)
            self.afip_recibido.update_comentario()
            self.datos_pg['cantidad'] = self.afip_recibido.get_cantidad()
            # Agrega las alertas:
            if self.afip_recibido.get_cantidad() > 0:
                self.alertas.append("alertaSuceso")
                self.datos_pg["alertaSuceso"] = ("Actualizó el registro "
                    "con <b>EXITO !!!</b>.")
            else:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No se pudo actualizar "
                    "el registro. <b>VERIFICAR !!!</b>.")
            #Arma los datos para la vista:
            self.contenidos = ["verDato",]
            self.datos_pg['id'] = self.id
            self.afip_recibido.find()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()
                                             
    def arma_vista(self):
        # Cambia formato a la fecha:
        fecha = self.afip_recibido.get_fecha()
        fecha_emi = date.strftime(fecha, '%d/%m/%Y')
        self.datos_pg['fecha'] = fecha_emi
        # Reemplaza el tipo de comprobante:
        if self.afip_recibido.get_tipo() in self.comprobantes_dicc: 
            tipo = self.comprobantes_dicc[self.afip_recibido.get_tipo()]
        else: 
            tipo = "OTRO"
        compro = (
            tipo+"-"+str(self.afip_recibido.get_punto_venta()).zfill(4)+"-"
            ""+str(self.afip_recibido.get_numero_d()).zfill(8)
            )
        self.datos_pg['comprobante'] = compro 
        # Reemplaza el tipo de documento:
        documento = "NO IDENTIFICADO"
        tipo_doc = self.afip_recibido.get_tipo_doc_emisor()
        if tipo_doc in self.documentos_dicc:
            tipo = self.documentos_dicc[tipo_doc]
            documento = (
                "("+str(tipo)+") - "+str(self.afip_recibido.get_nro_doc_emisor())+""
                )
        self.datos_pg['documento'] = documento
        prov = self.afip_recibido.get_nro_doc_emisor()
        self.datos_pg['nombre'] = self.proveedores_dicc[prov]
        importe = self.afip_recibido.get_importe_gravado()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importeGravado'] = importe
        importe = self.afip_recibido.get_importe_no_grav()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importeNoGRav'] = importe
        importe = self.afip_recibido.get_importe_exento()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importeExento'] = importe
        importe = self.afip_recibido.get_iva()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importeIva'] = importe
        importe = self.afip_recibido.get_importe_total()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importeTotal'] = importe
        self.datos_pg['cai'] = self.afip_recibido.get_cai()
        self.datos_pg['comentario'] = self.afip_recibido.get_comentario()
        # Representa las conciliaciones con iconos:
        if int(self.afip_recibido.get_rec()) == 1:
            self.datos_pg['recObs'] = ("<i class='fas fa-check' "
                "style='color:green' title='Conciliado con Recibidos'></i>")
        elif int(self.afip_recibido.get_rec()) == 2:
            self.datos_pg['recObs'] = ("<i class='fas "
                    "fa-exclamation-triangle' style='color:yellow' "
                    "title='Diferencia en importes con Recibidos'></i>")
        else:
            self.datos_pg['recObs'] = ("<i class='fas fa-ban' "
                "style='color:red' title='No registrado en Recibidos'></i>")
        if int(self.afip_recibido.get_prov_rec()) == 1:
            self.datos_pg['provObs'] = ("<i class='fas fa-check' "
                "style='color:green' title='Conciliado con Recibidos'></i>")
        elif int(self.afip_recibido.get_prov_rec()) == 2:
            self.datos_pg['provObs'] = ("<i class='fas "
                    "fa-exclamation-triangle' style='color:yellow' "
                    "title='Diferencia en importes con Recibidos'></i>")
        else:
            self.datos_pg['provObs'] = ("<i class='fas fa-ban' "
                "style='color:red' title='No registrado en Recibidos'></i>")
            
        # Busca comentarios de proveedores:
        if self.afip_recibido.get_prov_rec() > 0:
            opciones = {}
            fecha = self.afip_recibido.get_fecha()
            fecha_db = date.strftime(fecha, '%Y-%m-%d')
            opciones['fecha_d'] = fecha_db
            opciones['tipo'] = self.afip_recibido.get_tipo()
            opciones['numero'] = self.afip_recibido.get_numero_d()
            opciones['prov'] = self.afip_recibido.get_nro_doc_emisor() 
            datos = self.prov_recibido.find_comentario(opciones)
            self.datos_pg['provCom'] = datos[0][1]
        else:
            self.datos_pg['provCom'] = " "
          
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