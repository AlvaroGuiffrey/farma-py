#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# pruebaCSV.py
#
# Creado: 08/08/2019
# Versi�n: 001
# �ltima modificaci�n:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos que se importan
import csv
from builtins import int

print("Content-Type: text/html")
print("""
    <TITLE>KE csv</TITLE>
    """)

with open("./archivos/tarjetas/Ventas.csv", newline="") as csvfile:
    archivo = csv.reader(csvfile, delimiter=";")
    for renglon in archivo:
        print(renglon, "<br>")
        numero = renglon[5][1:5]
        print("Numero ", numero, " -> ")
        importe = renglon[8].replace(".", "")
        importe = importe.replace(",", ".")
        #importe "{0:.2f}".format(float(importe))
        print(importe, "<br>")
