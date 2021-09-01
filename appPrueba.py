#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# appPrueba.py
#
# Creado: 10/09/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#
# Módulos de la librería estandar:
import sys

# Agrega path:
sys.path.append("..")

# Módulos de la aplicación:
from includes.control.appControl import AppControl

print("Content-Type: text/html")


if __name__ == '__main__':
    AppControl().inicio()
