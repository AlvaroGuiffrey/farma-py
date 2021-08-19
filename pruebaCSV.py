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

print("Content-Type: text/html")
print("""
    <TITLE>KE csv</TITLE>
    """)

with open("KEMovimientos.csv", newline="") as csvfile:
    archivo = csv.reader(csvfile, delimiter=";")
    for renglon in archivo:
        print(renglon, "<br>")
        importe = renglon[3].replace(".", "")
        importe = importe.replace(",", ".")
        print(importe, "<br>")
