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
    <TITLE>BERSA - eCheques</TITLE>
    """)

with open("eCheques.txt", "r") as archivo:
    contenido = archivo.readlines()

for linea in contenido:
    print("..........> línea con {} caracteres.<br>".format(len(linea)))
    print(linea, "<br>")


    fecha_op = date(int(linea[365:369]), int(linea[362:364]), int(linea[359:361]))
    fecha_emi = date.strftime(fecha_op, '%Y-%m-%d')

    #fecha_emi = linea[359:369]

    fecha_op = date(int(linea[315:319]), int(linea[312:314]), int(linea[309:311]))
    fecha_pago = date.strftime(fecha_op, '%Y-%m-%d')

    #fecha_pago = linea[309:319]

    numero = int(linea[15:27])

    nombre = linea[89:280]
    nombre = nombre.strip()

    importe = linea[280:298]
    importe = float(importe.replace(",", "."))

    id = linea[0:15]

    print("Fecha Emi.: {} - Fecha Pago: {} - Número: {} - ".format(
                                                            fecha_emi,
                                                            fecha_pago,
                                                            numero))

    print("Orden de: {} - Importe $ {} - ID: {}".format(
                                    nombre,
                                    importe,
                                    id))

    print("<br>")
    renglon = linea.split()
    print("---------> renglón con {} elementos.<br>".format(len(renglon)))
    print(renglon, "<br>")
