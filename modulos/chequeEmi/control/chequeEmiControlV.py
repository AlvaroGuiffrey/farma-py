#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: latin-1 -*-

# chequeEmiControlV.py
#
# Creado: 29/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import cgi
import locale
from datetime import date
from datetime import datetime

# Módulos de la aplicación:
from includes.control.motorVista import MotorVista
from modulos.chequeEmi.modelo.chequeEmiModelo import ChequeEmiModelo
from includes.includes.selectHtml import SelectHtml

class ChequeEmiControlV():
    """
    Clase control del módulo chequeEmi para ventana.

    Realiza operaciones con -Cheques Emitidos- utilizando el patron MVC
    en una ventana pop-up.
    """


    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
        # Instancia las clases del modelo:
        self.cheque_emi = ChequeEmiModelo()
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'ventana'
        self.modulo = 'chequeEmi'
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
        self.numero = 0
        # Consulta tablas que se utilizan en el módulo:

        # Arma diccionarios que se utilizan en el módulo con datos de tablas:


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
        self.datos_pg['tituloPagina'] = "Cheques Emitidos"
        self.datos_pg['tituloBadge'] = "Cheques"
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge"]
        # Selecciona las acciones:
        if "bt_ver" in self.form: self.accion = "Ver"
        elif "bt_agregar" in self.form:
            self.accion = self.form.getvalue('bt_agregar')
        elif "bt_conf_agregar" in self.form:
            self.accion = self.form.getvalue('bt_conf_agregar')
        elif "bt_editar" in self.form:
            self.accion = self.form.getvalue('bt_editar')
        elif "bt_conf_editar" in self.form:
            self.accion = self.form.getvalue('bt_conf_editar')
        elif "bt_volver" in self.form:
            self.accion = "Ver"
        # else: self.accion = "Ver" #Anule para que pase agregar

        # Acción para Ver:
        if self.accion == "Ver":
            # Recibe los datos enviados del formulario por metodo POST:
            self.form = cgi.FieldStorage()
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Cheque Emitido - Ver")
            self.datos_pg['info'] = ("Permite ver los datos de un renglón"
                        " del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            #Arma los datos para la vista:
            self.contenidos = ["verDato",]
            self.cheque_emi.set_id(self.id)
            self.cheque_emi.find()
            self.datos_pg['cantidad'] = self.cheque_emi.get_cantidad()
            self.datos_pg['id'] = self.cheque_emi.get_id()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()
        """
        # Acción para editar
        if self.accion == "Editar":
            # Recibe datos por POST:
            self.id = self.form.getvalue("id")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Cupón de Tarjeta - Editar")
            self.datos_pg['info'] = ("Permite editar los datos de un renglón"
                        " del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfEditar", "botonVolver"]
            #Arma los datos para la vista:
            self.contenidos = ["editarDato",]
            self.tarj_cupon.set_id(self.id)
            self.tarj_cupon.find()
            self.datos_pg['cantidad'] = self.tarj_cupon.get_cantidad()
            self.datos_pg['id'] = self.tarj_cupon.get_id()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar editar:
        if self.accion == "ConfEditar":
            # Recibe datos por POST:
            self.id = self.form.getvalue("id")
            comentario = self.form.getvalue("comentario")
            self.error = int(self.form.getvalue("error"))
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Cupón de Tarjeta - Ver Edición")
            self.datos_pg['info'] = ("Permite ver los datos editados de "
                        "un renglón del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            #Actualiza los datos en la tabla:
            self.tarj_cupon.set_id(self.id)
            self.tarj_cupon.set_error(self.error)
            self.tarj_cupon.set_comentario(comentario)
            id_usuario = 1 # Va el id del USUARIO
            self.tarj_cupon.set_id_usuario_act(id_usuario)
            ahora = datetime.now()
            fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
            self.tarj_cupon.set_fecha_act(fecha_act)
            self.tarj_cupon.update_editar()
            self.datos_pg['cantidad'] = self.tarj_cupon.get_cantidad()
            # Agrega las alertas:
            if int(self.tarj_cupon.get_cantidad()) > 0:
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
            self.tarj_cupon.find()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()
        """
    def arma_vista(self):
        self.datos_pg['id'] = self.cheque_emi.get_id()
        self.datos_pg['numero'] = self.cheque_emi.get_numero()
        # Cambia formato a las fechas:
        fecha_emi = date.strftime(self.cheque_emi.get_fecha_emi(), '%d/%m/%Y')
        self.datos_pg['fecha_emi'] = fecha_emi
        fecha_pago = date.strftime(self.cheque_emi.get_fecha_pago(), '%d/%m/%Y')
        self.datos_pg['fecha_pago'] = fecha_pago
        # Cambia formato a importe
        importe = self.cheque_emi.get_importe()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importe'] = importe
        self.datos_pg['cuit_emi'] = self.cheque_emi.get_cuit_emi()
        self.datos_pg['nombre_emi'] = self.cheque_emi.get_nombre_emi()
        self.datos_pg['tipo'] = self.cheque_emi.get_tipo()
        self.datos_pg['caracter'] = self.cheque_emi.get_caracter()
        self.datos_pg['concepto'] = self.cheque_emi.get_concepto()
        # Revisa valor de las referencias
        referencia = self.cheque_emi.get_referencia()
        if str(referencia) == "None":
            referencia = ""
        self.datos_pg['referencia'] = referencia
        valor_ref = self.cheque_emi.get_valor_ref()
        if str(valor_ref) == "None":
            valor_ref = ""
        self.datos_pg['valor_ref'] = valor_ref

        self.datos_pg['estado_cheque'] = self.cheque_emi.get_estado_cheque()
        self.datos_pg['id_mov_banco'] = self.cheque_emi.get_id_mov_banco()
        # Cambia formato a la fecha de presentación:
        fecha_banco = self.cheque_emi.get_fecha_banco()
        if str(fecha_banco) == "None": fecha_banco = "00-00-0000"
        else:
            fecha_banco = date.strftime(self.cheque_emi.get_fecha_banco(), '%d/%m/%Y')
        self.datos_pg['fecha_banco'] = fecha_banco

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
