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
    <TITLE>BERSA - Movimientos</TITLE>
    """)

with open("Movimientos.txt", "r") as archivo:
    contenido = archivo.readlines()

cont = 0
#contenido.seek(18)
for linea in contenido:
    cont += 1
    print("{}...> línea con {} caracteres.<br>".format(cont, len(linea)))
    print(linea, "<br>")

    renglon = linea.split()
    print("{}--> renglón con {} elementos.<br>".format(cont, len(renglon)))
    print(renglon, "<br>")
    if cont > 18 and int(len(renglon)) > 1:
        # Cambio formato a las fechas
        fecha_op = date(int(linea[6:10]), int(linea[3:5]), int(linea[0:2]))
        fecha_mov = date.strftime(fecha_op, '%Y-%m-%d')
        #fecha_mov = linea[0:10]
        fecha_op = date(int(linea[36:40]), int(linea[33:35]), int(linea[30:32]))
        fecha_val = date.strftime(fecha_op, '%Y-%m-%d')
        #fecha_val = linea[30:40]

        importe = linea[70:90]
        importe = importe.replace(".", "")
        importe = float(importe.replace(",", "."))

        referencia = int(linea[90:103])

        concepto = linea[120:170]
        concepto = concepto.strip()

        print("<br>Fecha Mov.: {} - Fecha Valor: {} - Importe $ {} - ".format(
                                                            fecha_mov,
                                                            fecha_val,
                                                            importe))

        print("Referncia: {} - Concepto: {} ".format(
                                    referencia,
                                    concepto))

        print("<br>")


    print(".......................................................<br>")
