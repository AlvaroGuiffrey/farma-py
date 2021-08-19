#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaVista.py
#
# Creado: 19/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos que se importan de la librería estandar
from string import Template

with open('includes/vista/pagina.html', 'r') as archivo: 
    pagina = archivo.read()

with open('includes/vista/botonBadge.html', 'r') as archivo:
    botones = archivo.read()
    
with open('includes/vista/botonAgregar.html', 'r') as archivo:
    botones += archivo.read()
    
with open('includes/vista/botonEditar.html', 'r') as archivo:
    botones += archivo.read()
    
with open('includes/vista/botonDescartar.html', 'r') as archivo:
    botones += archivo.read()   
    

tituloPagina = 'P&#225;gina MVC' 
tituloBadge = 'Art&#237;culos'

diccionario = dict(
    TITULO = tituloPagina,
    BOTONES = botones,
    )

diccionario1 = dict(
    tituloBadge = tituloBadge,
    cantidad = '154',
    )

pagina = Template(pagina).safe_substitute(diccionario)
pagina = Template(pagina).safe_substitute(diccionario1)
print(pagina)
