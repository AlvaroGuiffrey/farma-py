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

print("Content-Type: text/html")
print("""
    <TITLE>Select</TITLE>
    """)

cantidad = 126
nombre = 'tipo'
"""
Prueba de traslate
"""
# Crea el archivo para la select:
select = open("select_"+nombre+".html", "w") 
# Arma y escribe la cabecera de la select html:
cabecera_html = (
    "<div class='input-group-prepend'>"
    "<div class='input-group-text' data-toggle='tooltip' "
    "title='Seleccione opción'>"+str(nombre.capitalize())+": "
    "</div><div class='input-group-text' data-toggle='tooltip' "
    "title='Cantidad de tipos de comprobantes'>"
    "<span class='badge badge-pill badge-secondary'>"+str(cantidad)+"</span>"
    "</div></div><select class='custom-select' id='"+nombre+"' "
    "name='"+nombre+"'>"
    )

select.write(cabecera_html)
select.close()
print("FINAL <br>")

elementos = {}
print("Diccionario vacio: ",elementos, "<br>")
elementos['CONTENIDOS'] = ''
dato = "select_tipo"
datos = "html de la vista"
elementos[dato] = datos
print("Diccionario con datos: ",elementos, "<br>")

elementos['FC A'] = 3
elementos['FC A'] += 10
print("Diccionario con datos: ",elementos, "<br>")

dic = {}
dic['FC C'] = [1, 100]
dic['FC A'] = [1, 10]
dic['ND A'] = [1, 150]
dic['NC a'] = [1, 40]
print(dic, "<br>")
dic['FC A'][0] += 1
dic['FC A'][1] += 1500
print(dic, "<br>")
lista = dic.items()
print(lista, "<br>")
lista_ord = sorted(lista)
print(lista_ord, "<br>")
for reng in lista_ord:
    print("Clave: ", reng[0], " cantidad: ", reng[1][0], " importe: ",
          reng[1][1], "<br>")