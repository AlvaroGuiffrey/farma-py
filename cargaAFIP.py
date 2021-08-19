#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# cargaAFIP.py
#
# Creado: 15/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

"""
Módulo que agrega a la tabla afip_mis_comprobantes los datos de 'Mis 
Comprobantes Recibidos' del csv descargado de la página de AFIP.

AFIPMovimientos.csv (Nombre del archivo descargado que lee)

Verifica existentes por fecha y número de comprobante
"""

# Modulos que se importan de la librería estándar
import csv
from datetime import date
from datetime import datetime

# Módulos que se importan de paquetes propios
from includes.modelo.conexionMySQL import ConexionMySQL

print("Content-Type: text/html")
print("""
    <TITLE>AFIP agrega a DB</TITLE>
    <h4>Agrega datos de "Mis Comprobantes" AFIP</h4>
    <p>-Verifica que no estén repetidos-</p>
    """)

ccnx = ConexionMySQL().conectar()
cursor = ccnx.cursor()
cont = agregados = repetidos = 0
with open("AFIPMovimientos.csv", newline="") as csvfile:
    archivo = csv.reader(csvfile, delimiter=",")
    
    print("<table><tr><th>OPERACION</th>",
          "<th>RENG.csv</th><th></th>", 
          "<th>NRO. COMPR.</th><th></th>", 
          "<th>FECHA EMI.</th>",
          "<th>NOMBRE DEL EMISOR</th></b></tr>")
    
    for dato in archivo:
        
        if cont > 0: # No lee el renglón de títulos
            
            fecha = dato[0].split("/")
            fecha_op = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
            fecha_emi = date.strftime(fecha_op, '%Y-%m-%d')
            nro_doc = dato[3]
            # Consulta a la tabla 
            query = ("SELECT * FROM afip_mis_comprobantes WHERE "
                "fecha = %s AND numero_d = %s")
            cursor.execute(query, (fecha_emi, nro_doc))
            renglones = cursor.fetchall()
                        
            if cursor.rowcount > 0: # Si existe no agrega el registro
                movi = "Repetido -> "
                repetidos += cursor.rowcount
            else:
                movi = "Agregado -> "
                                
                if dato[11] == "":
                    importe_gravado = "{0:.2f}".format(float(0))
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
            
                cursor.execute(query, valor)
                ccnx.commit()
                agregados += cursor.rowcount
                   
        
            print("<tr><td>", movi, "</td>"
                  "<td style='text-align:center'>", cont, "</td>"
                  "<td> - </td>" 
                  "<td style='text-align:center'>", nro_doc, "</td>"
                  "<td> - </td>" 
                  "<td style='text-align:center'>", fecha_emi, "</td>"
                  "<td>", dato[8], "</td></tr>")    
        cont += 1   
     

print("</table>")        
print(agregados, "Registros agregados <br>") 
print(repetidos, "Registro repetidos <br>")
print(cont, "Registros leidos <br>")   
cursor.close()
