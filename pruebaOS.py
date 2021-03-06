#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# pruebaOS.py
#
# Creado: 07/06/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Modulos que se importan
from datetime import date
import os

from builtins import int

from modulos.tarjeta.modelo.tarjProductoModelo import TarjProductoModelo
from modulos.tarjLiquidacion.modelo.tarjLiqModelo import TarjLiqModelo
tarj_producto = TarjProductoModelo()
productos = tarj_producto.find_all()
#tarj_producto.set_id(1)
#tarj_producto.find()
cant_producto = tarj_producto.get_cantidad()
tarj_liq = TarjLiqModelo()
tarj_liq.set_id(1234)
tarj_liq.set_liquidacion(1234)
tarj_liq.find_liquidacion()
cant_liquidaciones = tarj_liq.get_cantidad()

print("Content-Type: text/html")
print("""
    <TITLE>Prueba OS</TITLE>
    """)

print("Cantidad de tarjetas: ", cant_producto, "<br>")
print("Cantidad de liquidaciones: ", cant_liquidaciones, "<br>")
#print(os.ctermid(), "<br")
print("Directorio actual: ", os.getcwd(), "<br>")
path = os.getcwd() + "/archivos/tarjetas"
archivos = os.listdir(path)
print("Archivos del directorio: ", archivos, "<br>")
cant_archivos = len(archivos)
print("Cantidad de Archivos: ", cant_archivos, "<br>")
for arch in archivos:
    print("-> ", arch, "<br>")
    if "Liquidación" in arch:
        print("Existe!!! <br>")
    else:
        print(":-( no existe. <br>")

buscar = ["pruebaPDF.py", "app.py", "elchoto.py", "Ventas.csv",
          "select_tipo.html", "Liquidación diaria.csv"]

# utilizo not in o in de acuerdo a la finalidad.
encontrados = [item for item in archivos if item not in buscar]

print(encontrados, "<br>")

for liq in encontrados:
    dato = "./archivos/tarjetas/" + liq
    print(dato, "<br>")

    with open(dato, "r") as archivo:
        # print(archivo.red())
        contenido = archivo.readlines()

    print("FirstData - Prueba de lectura - ", liq, " <br>")

    for linea in contenido:
        if linea[0] == "1":
            fecha_txt = str(linea[24:32])
            anio = fecha_txt[0:4]
            mes = fecha_txt[4:6]
            dia = fecha_txt[6:]
            fecha_op = date(int(anio), int(mes), int(dia))
            fecha_proceso = date.strftime(fecha_op, '%Y-%m-%d')

            print(linea[0], "Proceso del :", fecha_proceso, "<br>")
            total = total_arancel = total_iva_arancel = int(0)

        if linea[0] == "2":
            print(linea[0], "Liquidación N° ", int(linea[54:61]), "<br>")

        if linea[0] == "3":
            # Obtiene el importe total
            importe_total = round(int(linea[103:116])/100, 2)
            if linea[116] == "2":
                importe_total = importe_total * -1

            # Obtiene el importe del arancel
            importe_arancel = round(int(linea[202:211])/100, 2)
            if linea[211] == "2":
                importe_arancel = importe_arancel * -1

            # Obtiene el iva del arancel
            iva_arancel = round(int(linea[212:221])/100, 2)
            if linea[221] == "2":
                iva_arancel = iva_arancel * -1

            # Suma totales para control
            total = round(total + importe_total, 2)
            total_arancel = round(total_arancel + importe_arancel, 2)
            total_iva_arancel = round(total_iva_arancel + iva_arancel, 2)
            print(linea[0], linea[15], linea[61:69], "Lote: ", int(linea[91:94]),
                  "Cupón: ", int(linea[94:99]), "$ ", importe_total, "Arancel $ ",
                  importe_arancel, "Iva Ar. $ ", iva_arancel, "Liq.: ",
                  int(linea[54:61]), "Tarj.: ", linea[152:171], "Aut.: ",
                  int(linea[273:281]), "<br>")

        if linea[0] == "7":
            total_7 = round(int(linea[61:74])/100, 2)
            if linea[74] == "2":
                total_7 = total_7 * -1
            total_7_arancel = round(int(linea[103:116])/100, 2)
            if linea[116] == "2":
                total_7_arancel = total_7_arancel * -1
            print("Total de la liquidación Reng.7:$ ", total_7, "Arancel/Financ. $",
                  total_7_arancel, " Iva Arancel $ ", total_iva_arancel, "<br>")

        if linea[0] == "8":
            total_8_iva = round(int(linea[63:76])/100, 2)
            if linea[76] == "2":
                total_8_iva = total_8_iva * -1
            print("Total suma cupones (1x1) $ ", total, "Arancel $ ", total_arancel,
                  " Iva Arancel $ ", total_8_iva, "<br>")
