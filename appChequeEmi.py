#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# appChequeEmi.py
#
# Creado: 19/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:

from modulos.chequeEmi.control.chequeEmiControl import ChequeEmiControl

print("Content-Type: text/html")

if __name__ == '__main__':
    ChequeEmiControl().inicio("Iniciar")
