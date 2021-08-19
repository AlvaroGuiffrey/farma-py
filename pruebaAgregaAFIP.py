#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaAgregaAFIP.py
#
# Creado: 08/08/2019
# Versi�n: 001
# �ltima modificaci�n: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos que se importan
import csv
from datetime import date
from datetime import datetime

from includes.modelo.conexionMySQL import ConexionMySQL

print("Content-Type: text/html")
print("""
    <TITLE>AFIP csv</TITLE>
    """)

with open("AfipMovRec.csv", newline="") as csvfile:
    archivo = csv.reader(csvfile, delimiter=",")
    ccnx = ConexionMySQL().conectar()
    cursor = ccnx.cursor()
    
    cont = agregados = repetidos = 0
    
    for dato in archivo:
        
        if cont > 0: # el primer renglón es el encabezado 
            fecha = dato[0].split("/")
            fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
            fecha_emi = date.strftime(fecha_op, '%Y-%m-%d')
            
            if dato[11] == "":
                importe_gravado = "{0:.2f}".format(float(0))
                print("aca -> ", importe_gravado, "<br>")
            else:    
                importe_gravado = "{0:.2f}".format(float(dato[11]))
             
            if dato[12] == "":
                importe_no_grav = "{0:.2f}".format(float(0))
            else:       
                importe_no_grav = "{0:.2f}".format(float(dato[12]))
                
            if dato[13] == "":
                importe_exento = "{0:.2f}".format(float(0))
            else:    
                importe_exento = "{0:.2f}".format(float(dato[13]))
                
            if dato[14] == "":
                iva = "{0:.2f}".format(float(0))
            else:    
                iva = "{0:.2f}".format(float(dato[14]))
                
            importe_total = "{0:.2f}".format(float(dato[15]))
            cuit = dato[7]
            id_usuario = 1 # Coloco un usuario a prepo
            ahora = datetime.now()
            fecha_act = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
            
                     
            tarea = "Agregado -> "
            query = (
                "INSERT INTO afip_mis_comprobantes (fecha, tipo,"
                "punto_venta, numero_d, numero_h, cai, tipo_doc_emisor,"
                "nro_doc_emisor, nombre_emisor, tipo_cambio, moneda,"
                "importe_gravado, importe_no_grav, importe_exento,"
                "iva, importe_total, id_usuario_act, fecha_act)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s, %s, %s, %s, %s, %s)"
                )
            valor = (fecha_emi, dato[1], dato[2], dato[3], dato[4],
                    dato[5],  dato[6], cuit, dato[8],  dato[9], dato[10],
                    importe_gravado, importe_no_grav, importe_exento,
                    iva, importe_total, id_usuario, fecha_act)
            print(valor, "<br>")
            
            #cursor.execute(query, valor)
            #ccnx.commit()
            #agregados = agregados + cursor.rowcount
                
            print(tarea, fecha_op, " - ", dato[8], 
                  " (", cuit, ") $ ", importe_total, " - ", fecha_act, 
                  "<br>")
            
        cont = cont + 1   
        
    print(agregados, "Registros agregados <br>") 
    print(repetidos, "Registro repetidos <br>")   
    cursor.close()
    
