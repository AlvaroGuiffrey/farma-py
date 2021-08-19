#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaAlexis.py
#
# Creado: 30/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos de la librería estandar:
import csv
from datetime import date
from time import time

# Módulos de la aplicación:
from includes.modelo.conexionMySQL import ConexionMySQL
from pruebaMenu import nombre_equipo
from pruebaVista import diccionario

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

# Arma un diccionario con los registros:
compro = {reng[3]: (reng[0], reng[1], reng[2], reng[3], reng[4]) 
          for reng in recibidos}
    
print(compro, "<br>")
armo1 = (time() - start)- leyo1
print("-------------------------------------------------<br>")
print("Armó DICC en: %.10f segundos." % armo1)
print("<br>")
print("-------------------------------------------------<br>")

# Arma una lista con los valores unidos de los registros:
recibidos
listaSQL = []
for reng in recibidos:
    listaSQL.append(str(reng[1])+str(reng[2])+str(reng[3])+str(reng[4]))
    
print(listaSQL, "<br>")

if '1121176503530538990627' in listaSQL:
    print("EXISTOOOOOOOO!!!!!!!<br>")
else:
    print("NOOOOOO existo <br>")
armo2 = (time() - start)- leyo1 - armo1
print("-------------------------------------------------<br>")
print("Armó Lista() en: %.10f segundos." % armo2)
print("<br>")
print("-------------------------------------------------<br>")

# Abri sin utilizar el -with as- lo cierro al final:
csvfile = open("AfipMovRec.csv", newline="")
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
        print("-> {} - {} - {} <br>".format(cont, nro, fecha_emi))
        query = ("SELECT * FROM afip_recibidos WHERE "
                 "tipo=%s AND punto_venta=%s AND numero_d=%s"
                 " AND nro_doc_emisor=%s")
        cursor.execute(query, (tipo, punto_venta, nro, cuit))
        renglones = cursor.fetchall()
            
        for reng in renglones:
            print("{} - {} - <br>".format(reng[1], reng[4], reng[8]))
            
    cont = cont + 1   
     
cursor.close()        
print(agregados, "Registros agregados <br>") 
print(repetidos, "Registro repetidos <br>")
print(cont, "Registros leidos <br>") 
elapsed = (time() - start) - leyo1 - armo1 - armo2
print("-------------------------------------------------<br>")
print("Ejecutó SQL en: %.10f segundos." % elapsed)
print("<br>")
print("-------------------------------------------------<br>")

csvfile.seek(0)
arch = csv.reader(csvfile, delimiter=",") 
next(arch)
print(arch, "<br>") 
for dato in arch:
    fecha = dato[0].split("/")
    fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
    fecha_emi = date.strftime(fecha_op, '%Y-%m-%d')
    tipo = dato[1]
    punto_venta = dato[2]
    nro = dato[3]
    cuit = dato[7]
    print("-> {} - {} - {}<br>".format(cont, nro, fecha_emi))
            
    if int(tipo) and int(punto_venta) and int(nro) and int(cuit) in compro:
        print("No existe comprobante lo agrego<br>")
    else:
        ren = compro[int(nro)]
        print("Existe: {} - {} SIGOOOO <br>".format(ren[3], ren[4]))

comparo1 = (time() - start) - leyo1 - armo1 - armo2 - elapsed
print("-------------------------------------------------<br>")
print("Comparó CSV con Dicc en: %.10f segundos." % comparo1)
print("<br>")
print("-------------------------------------------------<br>") 

csvfile.seek(0)
arch = csv.reader(csvfile, delimiter=",") 
next(arch)
cantidad = sum(1 for row in arch)
print("Cantidad : {} <br>".format(cantidad) )

csvfile.seek(0)
arch = csv.reader(csvfile, delimiter=",") 
next(arch)
cont = 1 
for dato in arch:
    fecha = dato[0].split("/")
    fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
    fecha_emi = date.strftime(fecha_op, '%Y-%m-%d')
    if cont == 1: break
    
csvfile.close()   

