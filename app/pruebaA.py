#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaA.py
#
# Creado: 10/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#
import sys
sys.path.append("..")
from includes.control.appPruebaControl import AppPruebaControl

print("Content-Type: text/html")

if __name__ == '__main__':
    AppPruebaControl().muestro()
    