# -*- coding: latin-1 -*-

# bancoMovControlV.py
#
# Creado: 02/05/2021
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
from modulos.bancoMov.modelo.bancoMovModelo import BancoMovModelo
from modulos.bancoMov.modelo.bancoMovConcModelo import BancoMovConcModelo
from modulos.bancoMov.modelo.bancoMovGrupoModelo import BancoMovGrupoModelo
from includes.includes.selectHtml import SelectHtml

class BancoMovControlV():
    """
    Clase control del módulo bancoMov para ventana.

    Realiza operaciones con -Movimientos del BERSA- por
    operaciones varias, utilizando el patron MVC en una ventana pop-up.
    """

    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
        # Instancia las clases del modelo:
        self.banco_mov = BancoMovModelo()
        self.banco_conc = BancoMovConcModelo()
        self.banco_grupo = BancoMovGrupoModelo()
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'ventana'
        self.modulo = 'bancoMov'
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
        self.id_grupo = 0
        self.error = 0
        self.error_carga = 0
        self.cupon = 0
        # Consulta tablas que se utilizan en el módulo:
        self.banco_conceptos = self.banco_conc.find_all()
        self.banco_grupos = self.banco_grupo.find_all()
        # Arma diccionarios que se utilizan en el módulo con datos de tablas:
        self.banco_conceptos_dicc = {reng[1]: (reng[0], reng[3])
                            for reng in self.banco_conceptos}
        self.banco_grupos_dicc = {reng[0]: (reng[1], reng[2])
                            for reng in self.banco_grupos}
        self.banco_grupos_buscar_dicc = {reng[0]: reng[1] for reng in
                                 self.banco_grupos}

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
        self.datos_pg['tituloPagina'] = "Movimientos Banco"
        self.datos_pg['usuario'] = "Alvaro"
        self.datos_pg['tituloBadge'] = "Movim."
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
        else: self.accion = "Ver" #Anule para que pase agregar

        # Acción para Ver:
        if self.accion == "Ver":
            # Recibe los datos enviados del formulario por metodo POST:
            self.form = cgi.FieldStorage()
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Movimientos Conformados - Banco - "
                                            "Ver")
            self.datos_pg['info'] = ("Permite ver los datos de un renglón"
                        " del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            #Arma los datos para la vista:
            self.contenidos = ["verDato",]
            self.banco_mov.set_id(self.id)
            self.banco_mov.find()
            self.datos_pg['cantidad'] = self.banco_mov.get_cantidad()
            self.datos_pg['id'] = self.banco_mov.get_id()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()
        # Acción para editar
        if self.accion == "Editar":
            # Recibe datos por POST:
            self.id = self.form.getvalue("id")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Movimientos Conformados - Banco - "
                                            "Editar")
            self.datos_pg['info'] = ("Permite editar los datos de un renglón"
                        " del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            # Agrega los botones para la acción:
            self.botones_ev = ["botonConfEditar", "botonVolver"]
            #Arma los datos para la vista:
            self.contenidos = ["editarDato",]
            self.banco_mov.set_id(self.id)
            self.banco_mov.find()
            self.datos_pg['cantidad'] = self.banco_mov.get_cantidad()
            self.datos_pg['id'] = self.banco_mov.get_id()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()

        # Acción para confirmar editar:
        if self.accion == "ConfEditar":
            # Recibe datos por POST:
            self.id = self.form.getvalue("id")
            comentario = self.form.getvalue("comentario")
            # Agrega titulo e información al panel:
            self.datos_pg['tituloPanel'] = ("Movimientos Conformados - Banco - Ver Edición")
            self.datos_pg['info'] = ("Permite ver los datos editados de "
                        "un renglón del listado.")
            # Agrega los botones de la aplicación:
            self.botones_ac.append('botonEditar')
            #Actualiza los datos en la tabla:
            self.banco_mov.set_id(self.id)
            self.banco_mov.set_comentario(comentario)
            id_usuario = 1 # Va el id del USUARIO
            self.banco_mov.set_id_usuario_act(id_usuario)
            ahora = datetime.now()
            fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
            self.banco_mov.set_fecha_act(fecha_act)
            self.banco_mov.update_editar()
            self.datos_pg['cantidad'] = self.banco_mov.get_cantidad()
            # Agrega las alertas:
            if int(self.banco_mov.get_cantidad()) > 0:
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
            self.banco_mov.find()
            self.arma_vista()
            # Muestra la vista:
            self.muestra_vista()


    def arma_vista(self):
        self.datos_pg['id'] = self.banco_mov.get_id()
        # Cambia formato a las fechas de operación:
        #fecha_ope = date.strftime(fecha, '%d/%m/%Y')
        self.datos_pg['fechaMov'] = self.banco_mov.get_fecha_mov()
        self.datos_pg['fechaValor'] = self.banco_mov.get_fecha_valor()
        # Cambia formatos a importes
        importe = self.banco_mov.get_importe()
        importe = locale.format("%.2f", (importe), True)
        self.datos_pg['importe'] = importe
        self.datos_pg['numero'] = self.banco_mov.get_numero()
        self.datos_pg['concepto'] = self.banco_mov.get_concepto()
        self.datos_pg['idGrupo'] = self.banco_mov.get_id_grupo()
        # Reemplaza el nombre del grupo:
        if int(self.banco_mov.get_id_grupo()) in self.banco_grupos_dicc:
            grupo = self.banco_grupos_dicc[int(self.banco_mov.get_id_grupo())][0]
        else:
            grupo = "SIN AGRUPAR"
        self.datos_pg['grupo'] = grupo
        # Arma las marcas:
        if int(self.banco_mov.get_marca()) == 0:
            self.datos_pg['marca'] = self.banco_mov.get_marca()
            self.datos_pg['detalle_marca'] = "Sin Conciliar"
        elif int(self.banco_mov.get_marca()) == 1:
            self.datos_pg['marca'] = self.banco_mov.get_marca()
            self.datos_pg['detalle_marca'] = "Conciliado"
        else:
            self.datos_pg['marca'] = self.banco_mov.get_marca()
            self.datos_pg['detalle_marca'] = "No Ident."
        comentario = self.banco_mov.get_comentario()
        if comentario == None: comentario = ""
        self.datos_pg['comentario'] = comentario

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
