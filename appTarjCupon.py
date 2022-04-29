#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appTarjCupon.py
#
# Creado: 02/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2021 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:

from modulos.tarjCupon.control.tarjCuponControl import TarjCuponControl

print("Content-Type: text/html")

if __name__ == '__main__':
    TarjCuponControl().inicio("Iniciar")
