#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# pruebaLI.py
#
# Creado: 08/08/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos que se importan
import sys
sys.path.append("..")

from modulos.afipRecibido.control.afipRecibidoControl import AfipRecibidoControl

print("Content-Type: text/html")

if __name__ == '__main__':
    AfipRecibidoControl().inicio("Iniciar")
