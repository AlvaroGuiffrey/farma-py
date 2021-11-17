#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# appTarjResumen.py
#
# Creado: 13/10/2021
# Versión: 001
# Última modificación:
#
# Copyright 2021 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:

from modulos.tarjResumen.control.tarjResControl import TarjResControl

print("Content-Type: text/html")

if __name__ == '__main__':
    TarjResControl().inicio("Iniciar")
