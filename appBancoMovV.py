#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appBancoMovV.py
#
# Creado: 02/05/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
import cgi

# Módulos de la aplicación:
from modulos.bancoMov.control.bancoMovControlV import BancoMovControlV

print("Content-Type: text/html")


if __name__ == '__main__':

    # Recibe los datos enviados:
    form = cgi.FieldStorage()
    accion = form.getvalue("accion")
    id_tabla = form.getvalue("id")
    BancoMovControlV().inicio(accion, id_tabla)
