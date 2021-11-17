# -*- coding: latin-1 -*-
#
# tarjResControl.py
#
# Creado: 13/10/2021
# Versión: 001
# Última modificación:
#
# Copyright 2021 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import os
import socket
import cgi
import locale
from datetime import date
from datetime import datetime
from builtins import int
from decimal import Decimal
# Módulos de la aplicación:
from includes.control.motorVista import MotorVista
from modulos.tarjeta.modelo.tarjProductoModelo import TarjProductoModelo
from modulos.tarjeta.modelo.tarjOperadorModelo import TarjOperadorModelo
from modulos.tarjLiquidacion.modelo.tarjLiqModelo import TarjLiqModelo
from modulos.tarjResumen.includes.tarjResPDF import TarjResPDF
from includes.includes.select import Select

class TarjResControl():
    """
    Clase control del módulo tarjResumen.

    Realiza resumen impositivo con liquidaciones de tarjetas a cobrar
    por ventas realizadas, utilizando el patron MVC.
    """
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR')
        # Instancia las clases del modelo:
        self.tarj_liq = TarjLiqModelo()
        self.tarj_producto = TarjProductoModelo()
        self.tarj_operador = TarjOperadorModelo()
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'tarjResumen'
        self.form = ''
        self.archivo = ''
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
        self.cant_liquidaciones = int(0)
        self.cant_productos = int(0)
        self.linea = []
        # Consulta tablas que se utilizan en el módulo:
        self.tarj_productos = self.tarj_producto.find_all()
        self.cant_productos = self.tarj_producto.get_cantidad()
        self.tarj_operadores = self.tarj_operador.find_all()
        self.cant_operadores = self.tarj_operador.get_cantidad()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.tarj_productos_dicc = {reng[0]: reng[1] for reng in
                               self.tarj_productos}
        self.tarj_operador_dicc = {reng[0]: reng[1] for reng in
                               self.tarj_operadores}

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
        self.datos_pg['tituloBadge'] = "Liquidaciones"
        # Obtiene la cantidad de registros de la tabla para badge:
        self.tarj_liq.count()
        self.datos_pg['cantidad'] = self.tarj_liq.get_cantidad()
        # Agrega los botones de la aplicación:
        self.botones_ac = ["botonBadge", "botonResumen"]
        # Selecciona las acciones:
        if "bt_resumen" in self.form: self.accion = "Resumen"
        elif "bt_conf_resumen" in self.form: self.accion = "ConfResumen"
        elif "bt_descargar_pdf" in self.form: self.accion = "DescargarPDF"
        else: self.accion = "Iniciar"
        # Pone en 0 los acumuladores:
        self.cant_liquidaciones = self.cant_productos = 0

        # Acción para iniciar:
        if self.accion == "Iniciar":
            #print("llegue aca<br>")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tarjetas - Resumen Impositivo")
            self.datos_pg['info'] = ("Permite obtener el Resumen Impositivo "
                        "de tarjetas liquidadas seleccionando los botones.")
            # Agrega las alertas:
            self.alertas.append("alertaInfo")
            self.datos_pg["alertaInfo"] = ("Seleccione una acción con los"
                        " <b>BOTONES</b>.")
            # Muestra la vista:
            self.muestra_vista()
        # Acción para armar el resumen:
        if self.accion == "Resumen":
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tarjetas - Resumen Impositivo")
            self.datos_pg['info'] = ("Realiza el resumen impositivo con datos "
                    "de las liquidaciones de trajetas. "
                    "<br>Seleccione en <b>Opciones para Resumen</b> "
                    "el período y operador.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfResumen",]
            # Arma los datos para la vista:
            self.opciones.append("resumenOpcion")
            # Carga los select para las opciones:
            # Select de operadores:
            datos = self.tarj_operador_dicc
            cantidad = self.cant_operadores
            nombre = 'operador'
            select_operador = Select()
            select_operador.arma_select(datos, cantidad, nombre)
            self.componentes += ["select_operador",]
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar armar resumen:
        if self.accion == "ConfResumen":
            # Recibe datos por POST:
            periodo = self.form.getvalue("periodo")
            id_operador = self.form.getvalue("operador")
            # Verifica las opciones recibidas
            flag = "N"
            if int(id_operador) > 0:
                self.datos_pg["operador"] = self.tarj_operador_dicc[int(id_operador)]
                if periodo != None:
                    flag = "S"
                    self.datos_pg["periodo"] = periodo
                    mes = periodo[4:]
                    ano = periodo[0:4]
                else:
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("Debe ingresar un "
                        "período. <b>VERIFICAR !!!</b>.")
            else:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("Debe seleccionar un "
                    "operador. <b>VERIFICAR !!!</b>.")
            # Si opciones son válidas arma resumen
            if flag == "S":
                # Arma las opciones de búsqueda:
                opciones = {}
                fecha_d = str(ano+"-"+mes+"-01")
                fecha_h = str(ano+"-"+mes+"-31")
                opciones['fecha_d'] = fecha_d
                opciones['fecha_h'] = fecha_h
                opciones['id_operador'] = int(id_operador)
                # Encuentra los datos de la busqueda para listar:
                datos = self.tarj_liq.find_all_resumen(opciones)
                self.datos_pg["cantidad"] = self.tarj_liq.get_cantidad()
                # Arma la vista del resumen:
                if self.tarj_liq.get_cantidad() > 0:
                    # Agrega los botones para la acción:
                    self.botones_ev = ["botonDescargarPDF",]
                    # Pone en cero las variables:
                    cant_liq = 0
                    importe_bruto = importe_desc = importe_neto = float(0)
                    arancel = costo_financiero = otros_debitos = float(0)
                    iva_arancel = iva_costo_financiero = float(0)
                    iva_otros_debitos = impuesto_debcred = float(0)
                    impuesto_interes = retencion_iva = float(0)
                    retencion_imp_gan = retencion_ing_brutos = float(0)
                    percepcion_iva = percepcion_ing_brutos = float(0)
                    # Carga las variables con los datos de la consulta:
                    for dato in datos:
                        cant_liq += 1
                        importe_bruto += float(dato[7])
                        importe_desc += float(dato[8])
                        importe_neto += float(dato[9])
                        arancel += float(dato[16])
                        costo_financiero += float(dato[17])
                        otros_debitos += float(dato[18])
                        iva_arancel += float(dato[19])
                        iva_costo_financiero += float(dato[20])
                        iva_otros_debitos += float(dato[21])
                        impuesto_debcred += float(dato[22])
                        impuesto_interes += float(dato[23])
                        retencion_iva += float(dato[24])
                        retencion_imp_gan += float(dato[25])
                        retencion_ing_brutos += float(dato[26])
                        percepcion_iva += float(dato[27])
                        percepcion_ing_brutos += float(dato[28])
                    # Muestra los datos:
                    self.contenidos.append("resumenDatos")
                    self.datos_pg["cantLiq"] = cant_liq
                    self.datos_pg["importeBruto"] = locale.format(
                                                "%.2f", (importe_bruto), True)
                    self.datos_pg["importeDesc"] = locale.format(
                                                "%.2f", (importe_desc), True)
                    self.datos_pg["importeNeto"] = locale.format(
                                                "%.2f", (importe_neto), True)
                    self.datos_pg["arancel"] = locale.format(
                                                "%.2f", (arancel), True)
                    self.datos_pg["costoFinanciero"] = locale.format(
                                                "%.2f", (costo_financiero), True)
                    self.datos_pg["otrosDebitos"] = locale.format(
                                                "%.2f", (otros_debitos), True)
                    self.datos_pg["ivaArancel"] = locale.format(
                                                "%.2f", (iva_arancel), True)
                    self.datos_pg["ivaCostoFinanciero"] = locale.format(
                                                "%.2f", (iva_costo_financiero), True)
                    self.datos_pg["ivaOtrosDebitos"] = locale.format(
                                                "%.2f", (iva_otros_debitos), True)
                    self.datos_pg["impuestoDebcred"] = locale.format(
                                                "%.2f", (impuesto_debcred), True)
                    self.datos_pg["impuestoInteres"] = locale.format(
                                                "%.2f", (impuesto_interes), True)
                    self.datos_pg["retencionIva"] = locale.format(
                                                "%.2f", (retencion_iva), True)
                    self.datos_pg["retencionImpGan"] = locale.format(
                                                "%.2f", (retencion_imp_gan), True)
                    self.datos_pg["retencionIngBrutos"] = locale.format(
                                            "%.2f", (retencion_ing_brutos), True)
                    self.datos_pg["percepcionIva"] = locale.format(
                                                "%.2f", (percepcion_iva), True)
                    self.datos_pg["percepcionIngBrutos"] = locale.format(
                                                "%.2f", (percepcion_ing_brutos), True)

                    # Muestra mensaje:
                    self.alertas.append("alertaSuceso")
                    self.datos_pg["alertaSuceso"] = ("El Resumen Impositivo "
                        "del operador se armó con <b>EXITO !!!</b>.")
                # Muestra mensaje si no hay liquidaciones:
                else:
                    self.alertas.append("alertaAdvertencia")
                    self.datos_pg["alertaAdvertencia"] = ("No hay liquidaciones"
                        " en el período para el operador. <b>VOLVER A INTENTAR"
                        " !!!</b>.")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Tarjetas - Resumen Impositivo")
            self.datos_pg['info'] = ("Resumen impositivo armado según las "
                                     "opciones ingresadas y seleccionadas.")

            # Muestra la vista:
            self.muestra_vista()
        # Acción para buscar:
        if self.accion == "DescargarPDF":
            # Recibe datos por POST:
            # Arma los datos y el detalle PDF:
            datos = {}

            datos['cant_liq'] = self.form.getvalue("cant_liq")
            datos['importe_bruto'] = self.form.getvalue("importe_bruto")
            datos['importe_desc'] = self.form.getvalue("importe_desc")
            datos['importe_neto'] = self.form.getvalue("importe_neto")
            datos['arancel'] = self.form.getvalue("arancel")
            datos['costo_financiero'] = self.form.getvalue("costo_financiero")
            datos['otros_debitos'] = self.form.getvalue("otros_debitos")
            datos['iva_arancel'] = self.form.getvalue("iva_arancel")
            datos['iva_costo_financiero'] = self.form.getvalue("iva_costo_financiero")
            datos['iva_otros_debitos'] = self.form.getvalue("iva_otros_debitos")
            datos['impuesto_debcred'] = self.form.getvalue("impuesto_debcred")
            datos['impuesto_interes'] = self.form.getvalue("impuesto_interes")
            datos['retencion_iva'] = self.form.getvalue("retencion_iva")
            datos['retencion_imp_gan'] = self.form.getvalue("retencion_imp_gan")
            datos['retencion_ing_brutos'] = self.form.getvalue("retencion_ing_brutos")
            datos['percepcion_iva'] = self.form.getvalue("percepcion_iva")
            datos['percepcion_ing_brutos'] = self.form.getvalue("percepcion_ing_brutos")
            detalle_pdf = ("Operador: "+str(self.form.getvalue("operador"))+" - "
                           "Periodo: "+str(self.form.getvalue("periodo"))+" ")

            # Consulta la tabla:
            self.tarj_liq.count()
            self.datos_pg["cantidad"] = self.tarj_liq.get_cantidad()
            # Escribe y guarda el archivo PDF:
            pdf = TarjResPDF()
            pdf.escribir_pdf(datos, detalle_pdf)

            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Descarga Resumen en PDF")
            self.datos_pg['info'] = ("Realiza la descarga del Resumen"
                        " Impositivo de tarjetas en un archivo PDF en el"
                        " directorio: 'archivos/tarjetas' de la aplicación. <br>"
                        "También lo puede abrir en el navegador con el boton"
                        " 'Abrir PDF'.")
            # Agrega las alertas:
            self.alertas.append("alertaSuceso")
            self.datos_pg["alertaSuceso"] = ("Se descargó el archivo PDF "
                    "con <b>EXITO !!!</b>.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonAbrirTarjResPDF",]
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
