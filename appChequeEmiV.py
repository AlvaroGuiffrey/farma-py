#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# appChequeEmiV.py
#
# Creado: 29/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import cgi

# Módulos de la aplicación:
from modulos.chequeEmi.control.chequeEmiControlV import ChequeEmiControlV

print("Content-Type: text/html")


if __name__ == '__main__':

    # Recibe los datos enviados:
    form = cgi.FieldStorage()
    accion = form.getvalue("accion")
    id_tabla = form.getvalue("id")
    ChequeEmiControlV().inicio(accion, id_tabla)
