#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaLeeAFIP.py
#
# Creado: 08/08/2019
# Versi�n: 001
# �ltima modificaci�n: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la biblioteca estandar:
import csv
from datetime import date
from time import time

# Módulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL

print("Content-Type: text/html")
print("""
    <TITLE>AFIP Lee DB</TITLE>
    """)

start = time()
ccnx = ConexionMySQL().conectar()
cursor = ccnx.cursor()
cont = agregados = repetidos = 0
query = ("SELECT id, tipo, punto_venta, numero_d, nro_doc_emisor "
         "FROM afip_recibidos")
cursor.execute(query)
recibidos = cursor.fetchall()
cursor.close()

#print(recibidos, "<br>")
leyo1 = time() - start
print("----------------------------------------------------<br>")
print("Leyó tabla afip_recibidos (MySQL) en: %.10f segundos." % leyo1)
print("<br>")
print("----------------------------------------------------<br>")

# Arma un diccionario con los registros
compro = {}
for reng in recibidos:
    compro[reng[3]] = (reng[0], reng[1], reng[2], reng[3], reng[4])
    
print(compro, "<br>")
armo1 = (time() - start)- leyo1
print("-------------------------------------------------<br>")
print("Leyó recibidos en: %.10f segundos." % armo1)
print("<br>")
print("-------------------------------------------------<br>")

with open("AfipMovRec.csv", newline="") as csvfile:
    archivo = csv.reader(csvfile, delimiter=",")
    cursor = ccnx.cursor()
    print(archivo, "<br>")
    for dato in archivo:
        
        if cont > 0:
            
            fecha = dato[0].split("/")
            fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
            fecha_emi = date.strftime(fecha_op, '%Y-%m-%d')
            tipo = dato[1]
            punto_venta = dato[2]
            nro = dato[3]
            cuit = dato[7]
            print("-> ", cont, " - ", nro, " -", fecha_emi, "<br>")
            query = ("SELECT * FROM afip_recibidos WHERE "
                     "tipo=%s AND punto_venta=%s AND numero_d=%s"
                     " AND nro_doc_emisor=%s")
            cursor.execute(query, (tipo, punto_venta, nro, cuit))
            renglones = cursor.fetchall()
            
            for reng in renglones:
                print(reng[1], " - ", reng[4], " - ", reng[8],"<br>")
            
        cont = cont + 1   
     
cursor.close()        
print(agregados, "Registros agregados <br>") 
print(repetidos, "Registro repetidos <br>")
print(cont, "Registros leidos <br>") 
elapsed = (time() - start) - leyo1 - armo1 
print("Ejecutó SQL en: %.10f segundos." % elapsed)
print("============================= <br>")
 
csvfile = open("AfipMovRec.csv", newline="")
arch = csv.reader(csvfile, delimiter=",")

cont = 0
print(arch, "<br>") 
for dato in arch:
        
    if cont > 0:
        fecha = dato[0].split("/")
        fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
        fecha_emi = date.strftime(fecha_op, '%Y-%m-%d')
        tipo = dato[1]
        punto_venta = dato[2]
        nro = dato[3]
        cuit = dato[7]
        print("-> ", cont, " - ", nro, " -", fecha_emi, "<br>")
            
        existe = int(nro) in compro
        if existe == False:
            print("No existe comprobante lo agrego<br>")
        else:
            ren = compro[int(nro)]
            print("Existe: ", ren[3], " - ", ren[4], " SIGOOOO <br>")
           
        
    cont +=1

comparo1 = (time() - start) - leyo1 - armo1 - elapsed
print("-------------------------------------------------<br>")
print("Comparó CSV con Dicc en: %.10f segundos." % comparo1)
print("<br>")
print("-------------------------------------------------<br>") 

csvfile.seek(0)
arch = csv.reader(csvfile, delimiter=",")  
next(arch)  
cont = 1
for line in arch:
    if cont == 1: break

print(line, "<br>") 
csvfile.close()   