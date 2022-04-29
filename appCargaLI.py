#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appCargaLI.py
#
# Creado: 26/09/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:
from modulos.provRecibido.control.cargaLIControl import CargaLIControl

print("Content-Type: text/html")

if __name__ == '__main__':
    CargaLIControl().inicio("Iniciar")
