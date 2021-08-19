#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# motorVista.py
#
# Creado: 21/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos que se importan de la librería estandar
from string import Template


class MotorVista:
    
    
    def __init__(self):
        self.html = ''
        self.archivo = ''
        self.elementos = {}
        self.comp = {}
        self.botones_aux = {} 
        
    def arma_vista(self, tipo, botones_ac, botones_ev, botones_aux, alertas,  
                   opciones, contenidos, tablas, componentes, datos_pg, modulo):
        
        if tipo == "ventana":
            with open('includes/vista/paginaV.html', 'r') as self.archivo: 
                self.html = self.archivo.read()
                
        else:    
            with open('includes/vista/pagina.html', 'r') as self.archivo: 
                self.html = self.archivo.read()
            
            with open('includes/vista/menu.html', 'r') as self.archivo:
                self.elementos['MENU'] = self.archivo.read()
            
        if botones_ac:
            datos = ''
            for dato in botones_ac:
                rutaDato = 'includes/vista/'+dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
            
            self.elementos['BOTONES_AC'] = datos
        else:
            self.elementos['BOTONES_AC'] = ''  
            
        if botones_ev:
            datos = ''
            for dato in botones_ev:
                rutaDato = 'includes/vista/'+dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
            
            self.elementos['BOTONES_EV'] = datos
        else:
            self.elementos['BOTONES_EV'] = '' 
            
        if alertas:
            datos = ''
            for dato in alertas:
                rutaDato = 'includes/vista/'+dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
            
            self.elementos['ALERTAS'] = datos
        else:
            self.elementos['ALERTAS'] = ''
        
        if opciones:
            datos = ''
            for dato in opciones:
                rutaDato = 'modulos/'+modulo+'/vista/'+dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
                    
            self.elementos['OPCIONES'] = datos
        else:
            self.elementos['OPCIONES'] = '' 
        
        if contenidos:
            datos = ''
            for dato in contenidos:
                rutaDato = 'modulos/'+modulo+'/vista/'+dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
                    
            self.elementos['CONTENIDOS'] = datos
        else:
            self.elementos['CONTENIDOS'] = ''
            
        if tablas:
            datos = ''
            for dato in tablas:
                rutaDato = dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
                    
            self.elementos['TABLAS'] = datos
        else:
            self.elementos['TABLAS'] = '' 
            
        if componentes:
            # Arma cada componente en forma individual:
            self.comp['COMPONENTES'] =''
            for dato in componentes:
                datos = ''
                rutaDato = dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
                self.comp[str(dato)] = datos
                
        else:
            self.comp['COMPONENTES'] = '' 
            
        if botones_aux:
            datos = ''
            for dato in botones_aux:
                rutaDato = 'includes/vista/'+dato+'.html'
                with open(rutaDato, 'r') as archivo:
                    datos += archivo.read()
                self.botones_aux[str(dato)] = datos
            
                    
                  
        self.html = Template(self.html).safe_substitute(self.elementos)
        self.html = Template(self.html).safe_substitute(self.comp)
        self.html = Template(self.html).safe_substitute(self.botones_aux) 
        self.html = Template(self.html).safe_substitute(datos_pg)
        return self.html
