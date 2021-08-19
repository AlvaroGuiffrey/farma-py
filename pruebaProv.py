#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaProv.py
#
# Creado: 08/08/2019
# Versión: 001
# Ultima modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos que se importan de la librería estandar

from includes.modelo.conexionMySQL import ConexionMySQL
from modulos.afipRecibido.modelo.afipRecibidoModelo import AfipRecibidoModelo

print("Content-Type: text/html")
print("""
    <TITLE>Proveedores Dicc</TITLE>
    """)

ccnx = ConexionMySQL().conectar()
cursor = ccnx.cursor()
recibido_modelo = AfipRecibidoModelo()
query = (
        "SELECT nro_doc_emisor, nombre_emisor AS c FROM "
        "afip_recibidos GROUP BY nro_doc_emisor "
        "ORDER BY nombre_emisor"
        )
cursor.execute(query)
datos = cursor.fetchall()
cantidad = cursor.rowcount
cursor.close()
ccnx.close() 

print("Cantidad: ", cantidad,"<br>")
print(datos, "<br>")

print(
"<button type='button' value='Ver Artículo' title='Botón para ver datos' "
"onclick='javascrip:window.open(\"http://www.google.com.ar\", \"Ventana\", \"width=600, height=500, top=100, left=100, menubar=0, toolbar=0, titlebar=1, location=0, scrollbars=1\"); void 0'>"
"<span class='glyphicon glyphicon-search' aria-hidden='true'>"
"</span> Ver</button>"
)