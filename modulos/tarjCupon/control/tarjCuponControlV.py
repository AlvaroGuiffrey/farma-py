#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: latin-1 -*-

# tarjCuponControlV.py
#
# Creado: 10/09/2021
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
from modulos.tarjCupon.modelo.tarjCuponModelo import TarjCuponModelo
from modulos.tarjeta.modelo.tarjProductoModelo import TarjProductoModelo
from includes.includes.selectHtml import SelectHtml

class TarjCuponControlV():
    """
    Clase control del módulo tarjCupon para ventana.

    Realiza operaciones con -Cupones de tarjetas- por
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
        self.tarj_cupon = TarjCuponModelo()
        self.tarj_producto = TarjProductoModelo()
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'ventana'
        self.modulo = 'tarjCupon'
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
        self.error = 0
        self.cupon = 0
        # Consulta tablas que se utilizan en el módulo:
        self.tarj_productos = self.tarj_producto.find_all()
        self.cant_productos = self.tarj_producto.get_cantidad()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.tarj_productos_dicc = {reng[1]: reng[0] for reng in
                               self.tarj_productos}
        self.tarj_productos_listar_dicc = {reng[0]: (reng[1], reng[2])
                            for reng in self.tarj_productos}

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
        self.datos_pg['tituloPagina'] = "Tarjetas"
        self.datos_pg['tituloBadge'] = "Comprobantes"
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
            self.datos_pg['tituloPanel'] = ("Cupón de Tarjeta - Ver")
            self.datos_pg['info'] = ("Permite ver los datos de un renglón"
                        " del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            #Arma los datos para la vista:
            self.contenidos = ["verDato",]
            self.tarj_cupon.set_id(self.id)
            self.tarj_cupon.find()
            self.datos_pg['cantidad'] = self.tarj_cupon.get_cantidad()
            self.datos_pg['id'] = self.tarj_cupon.get_id()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()
        # Acción para agregar
        if self.accion == "Agregar":
            # Recibe datos por POST:
            self.cupon = self.form.getvalue("cupon")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Cupón de Tarjeta - Agregar")
            self.datos_pg['info'] = ("Permite agregar los datos de un renglón"
                        " del listado en la tabla de la DB.")
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfAgregar"]
            #Arma los datos para la vista:
            nombre = "producto"
            datos = self.tarj_productos_listar_dicc
            select = SelectHtml()
            select.arma_select(datos, nombre)
            self.componentes += ["select_producto",]
            self.contenidos = ["agregarDato",]
            self.datos_pg['cantidad'] = 0
            self.datos_pg['cupon'] = self.cupon
            # Muestra la vista:
            self.muestra_vista()
        # Acción para confirmar agregar:
        if self.accion == "ConfAgregar":
            # Recibe datos por POST:

            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Cupón de Tarjeta - Ver Agregado")
            self.datos_pg['info'] = ("Permite ver los datos agregados de "
                        "un renglón del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            # Arma los datos para la vista
            self.contenidos = ["verDato",]
            self.tarj_cupon.set_cupon(self.form.getvalue("cupon"))
            self.tarj_cupon.set_fecha(self.form.getvalue("fecha"))
            self.tarj_cupon.set_numero(self.form.getvalue("numero"))
            self.tarj_cupon.set_id_producto(self.form.getvalue("producto"))
            self.tarj_cupon.set_moneda("ARS")
            self.tarj_cupon.set_importe(float(self.form.getvalue("importe")))
            self.tarj_cupon.set_descuento(float(self.form.getvalue("descuento")))
            self.tarj_cupon.set_neto(float(self.form.getvalue("neto")))
            self.tarj_cupon.set_cuota(self.form.getvalue("cuota"))
            self.tarj_cupon.set_autorizacion(self.form.getvalue("autorizacion"))
            self.tarj_cupon.set_error(self.form.getvalue("error"))
            comentario = self.form.getvalue("comentario")
            if comentario == None: comentario = ""
            self.tarj_cupon.set_comentario(comentario)
            self.tarj_cupon.set_fecha_presentacion(self.form.getvalue("fecha_pre"))
            self.tarj_cupon.set_lote(self.form.getvalue("lote"))
            self.tarj_cupon.set_liquidacion(self.form.getvalue("liquidacion"))
            self.tarj_cupon.set_estado(int(1))
            id_usuario = 1 # Va el id del USUARIO
            self.tarj_cupon.set_id_usuario_act(id_usuario)
            ahora = datetime.now()
            fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
            self.tarj_cupon.set_fecha_act(fecha_act)
            self.tarj_cupon.insert()
            self.datos_pg['cantidad'] = self.tarj_cupon.get_cantidad()
            # Agrega las alertas:
            if int(self.tarj_cupon.get_cantidad()) > 0:
                self.alertas.append("alertaSuceso")
                self.datos_pg["alertaSuceso"] = ("Actualizó el registro "
                    "con <b>EXITO !!!</b>.")
                self.tarj_cupon.set_id(self.tarj_cupon.get_ultimo_id())
                self.tarj_cupon.find()
                #self.datos_pg['cantidad'] = self.tarj_cupon.get_cantidad()
            else:
                self.alertas.append("alertaAdvertencia")
                self.datos_pg["alertaAdvertencia"] = ("No se pudo actualizar "
                    "el registro. <b>VERIFICAR !!!</b>.")
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()
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

    def arma_vista(self):
        self.datos_pg['id'] = self.tarj_cupon.get_id()
        self.datos_pg['cupon'] = self.tarj_cupon.get_cupon()
        # Cambia formato a la fecha de operación:
        fecha = self.tarj_cupon.get_fecha()
        #fecha_ope = date.strftime(fecha, '%d/%m/%Y')
        #self.datos_pg['fecha'] = fecha_ope
        self.datos_pg['fecha'] = fecha
        self.datos_pg['numero'] = self.tarj_cupon.get_numero()
        self.datos_pg['idProducto'] = self.tarj_cupon.get_id_producto()
        id_producto = int(self.tarj_cupon.get_id_producto())
        # Reemplaza el nombre de producto:
        if id_producto in self.tarj_productos_listar_dicc:
            producto = self.tarj_productos_listar_dicc[id_producto][0]
        else:
            producto = "SIN IDENTIFICAR"
        self.datos_pg['producto'] = producto
        # Cambia formatos a importes
        importe = self.tarj_cupon.get_importe()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importe'] = importe
        importe = self.tarj_cupon.get_descuento()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['descuento'] = importe
        importe = self.tarj_cupon.get_neto()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['neto'] = importe
        self.datos_pg['cuota'] = self.tarj_cupon.get_cuota()
        self.datos_pg['autorizacion'] = self.tarj_cupon.get_autorizacion()
        self.datos_pg['error'] = self.tarj_cupon.get_error()
        # Arma el select del error
        self.datos_pg['select0'] = self.datos_pg['select1'] = " "
        self.datos_pg['select2'] = " "
        if int(self.tarj_cupon.get_error()) == 0:
            self.datos_pg['error'] = 0
            self.datos_pg['detalle_error'] = "Aceptada"
            self.datos_pg['select0'] = "selected"
        elif int(self.tarj_cupon.get_error()) == 1:
            self.datos_pg['error'] = 1
            self.datos_pg['detalle_error'] = "Rechazada"
            self.datos_pg['select1'] = "selected"
        elif int(self.tarj_cupon.get_error()) == 2:
            self.datos_pg['error'] = 2
            self.datos_pg['detalle_error'] = "Anula/da"
            self.datos_pg['select2'] = "selected"
        else:
            self.datos_pg['error'] = self.tarj_cupon.get_error()
            self.datos_pg['detalle_error'] = "No Ident."
        # --- fin arma select ---
        comentario = self.tarj_cupon.get_comentario()
        if comentario == None: comentario = ""
        self.datos_pg['comentario'] = comentario
        # Cambia formato a la fecha de presentación:
        fecha = self.tarj_cupon.get_fecha_presentacion()
        if fecha == None: fecha = "0000-00-00"
        #fecha_pre = date.strftime(fecha, '%d/%m/%Y')
        #self.datos_pg['fecha_pre'] = fecha_pre
        self.datos_pg['fecha_pre'] = fecha
        self.datos_pg['lote'] = self.tarj_cupon.get_lote()
        self.datos_pg['liquidacion'] = self.tarj_cupon.get_liquidacion()

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
