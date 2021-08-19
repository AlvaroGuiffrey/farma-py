#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# pruebaTXT.py
#
# Creado: 08/08/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos que se importan
from datetime import date

print("Content-Type: text/html")
print("""
    <TITLE>DS txt</TITLE>
    """)

with open("DSObrasSociales.txt", "r") as archivo:
    contenido = archivo.readlines()

for linea in contenido:
    print("..........> línea con {} caracteres.<br>".format(len(linea)))
    print(linea, "<br>")
    

    fecha_op = date(int(linea[95:99]), int(linea[92:94]), int(linea[89:91]))
    fecha = date.strftime(fecha_op, '%Y-%m-%d')
    print("Fecha: {} - Tipo: {} - Comprobante: {}-{}-{} - Concepto: {}".format(
                                                                 fecha,
                                                                 linea[86:88],
                                                                 linea[228],
                                                                 linea[224:228],
                                                                 linea[229:237],
                                                                 linea[141:162]))
    print("<br>")
    renglon = linea.split()
    print("---------> renglón con {} elementos.<br>".format(len(renglon)))
    print(renglon, "<br>")

    print(renglon[8], " $ ", renglon[9], "<br>")
