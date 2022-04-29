#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# appBancoMov.py
#
# Creado: 30/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:

from modulos.bancoMov.control.bancoMovControl import BancoMovControl

print("Content-Type: text/html")

if __name__ == '__main__':
    BancoMovControl().inicio("Iniciar")
