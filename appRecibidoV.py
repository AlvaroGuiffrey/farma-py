#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# appRecibidoV.py
#
# Creado: 21/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos de la librería estandar:
import cgi

# Módulos de la aplicación:
from modulos.recibido.control.recibidoControlV import RecibidoControlV

print("Content-Type: text/html")


if __name__ == '__main__':
    
    # Recibe los datos enviados:
    form = cgi.FieldStorage()
    accion = form.getvalue("accion")
    id_tabla = form.getvalue("id")
    RecibidoControlV().inicio(accion, id_tabla)