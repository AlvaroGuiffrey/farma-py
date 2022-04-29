#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appAfipRecibidoV.py
#
# Creado: 19/09/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la libreria estandar:
import cgi

# Módulos de la aplicación:
from modulos.afipRecibido.control.afipRecibidoControlV import AfipRecibidoControlV

print("Content-Type: text/html")


if __name__ == '__main__':

    # Recibe los datos enviados:
    form = cgi.FieldStorage()
    accion = form.getvalue("accion")
    id_tabla = form.getvalue("id")
    AfipRecibidoControlV().inicio(accion, id_tabla)
