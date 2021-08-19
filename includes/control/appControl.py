#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# appControl.py
#
# Creado: 28/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos de la librería estandar:
import socket
# Módulos de la aplicación:
from includes.control.motorVista import MotorVista


class AppControl(object):
    """
    Clase para iniciar la aplicación.
    
    """
    # Atributos de la instancia:
    def __init__(self):
        """
        Inicializa los atributos de la instancia.
        """
        # Busca el ip para el menú:
        self.nombre_equipo = socket.gethostname()
        self.ip = socket.gethostbyname(self.nombre_equipo)
        # Inicializa datos que utilizan en el módulo:
        self.tipo = 'pagina'
        self.modulo = 'includes'
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
    
    def inicio(self):
        """ 
        Inicio de la clase control.
        
        Realiza el login del usuario y nos carga la aplicación para acceder
        al menú.
        """
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
        self.datos_pg['tituloPagina'] = "Inicio App"
        self.datos_pg['usuario'] = "Login"
        # Agrega titulo e información al panel:
        self.datos_pg['tituloPanel'] = ("Inicio de la Aplicación")
        self.datos_pg['info'] = ("Permite realizar acciones de " 
                        " inicio de la aplicación.")
        # Agrega las alertas:
        self.alertas.append("alertaInfo")
        self.datos_pg["alertaInfo"] = ("Seleccione una tabla o tarea con"
                        " el <b>MENU</b> de la aplicación.")
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