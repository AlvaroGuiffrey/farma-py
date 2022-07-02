#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
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

with open("./archivos/LIMovimientos.csv", newline="") as csvfile:
    archivo = csv.reader(csvfile, delimiter=";")
    for renglon in archivo:
        print(renglon, "<br>")
        numero = renglon[0]
        cupon = renglon[1]
        lote = renglon[2]
        print("Numero ", numero, " / Cupon ", cupon, " / Lote ", lote, " -> ")
        importe = renglon[3]
        #importe = renglon[3].replace(".", ",")
        #importe = importe.replace(",", ".")
        #importe "{0:.2f}".format(float(importe))
        print(importe, "<br>")
