#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# appCargaDS.py
#
# Creado: 26/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos de la aplicación:
from modulos.provRecibido.control.cargaDSControl import CargaDSControl

print("Content-Type: text/html")

if __name__ == '__main__':
    CargaDSControl().inicio("Iniciar")
