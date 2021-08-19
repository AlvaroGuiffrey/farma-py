#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# appCargaKE.py
#
# Creado: 25/09/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Módulos de la aplicación:
from modulos.provRecibido.control.cargaKEControl import CargaKEControl

print("Content-Type: text/html")

if __name__ == '__main__':
    CargaKEControl().inicio("Iniciar")
    