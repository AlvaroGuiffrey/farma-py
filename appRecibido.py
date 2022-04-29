#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appRecibido.py
#
# Creado: 19/09/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:
from modulos.recibido.control.recibidoControl import RecibidoControl

print("Content-Type: text/html")

if __name__ == '__main__':
    RecibidoControl().inicio("Iniciar")
