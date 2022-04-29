#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appCargaOS.py
#
# Creado: 05/10/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:
from modulos.provRecibido.control.cargaOSControl import CargaOSControl

print("Content-Type: text/html")

if __name__ == '__main__':
    CargaOSControl().inicio("Iniciar")
