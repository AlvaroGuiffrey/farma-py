#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# app.py
#
# Creado: 14/09/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la aplicación:
from includes.control.appControl import AppControl

print("Content-Type: text/html")

if __name__ == '__main__':
    AppControl().inicio()
