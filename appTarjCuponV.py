#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# appTarjCuponV.py
#
# Creado: 10/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import cgi

# Módulos de la aplicación:
from modulos.tarjCupon.control.tarjCuponControlV import TarjCuponControlV

print("Content-Type: text/html")


if __name__ == '__main__':

    # Recibe los datos enviados:
    form = cgi.FieldStorage()
    accion = form.getvalue("accion")
    id_tabla = form.getvalue("id")
    TarjCuponControlV().inicio(accion, id_tabla)
