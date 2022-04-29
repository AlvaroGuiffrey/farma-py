#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appTarjLiquidacion.py
#
# Creado: 16/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2021 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:

from modulos.tarjLiquidacion.control.tarjLiqControl import TarjLiqControl

print("Content-Type: text/html")

if __name__ == '__main__':
    TarjLiqControl().inicio("Iniciar")
