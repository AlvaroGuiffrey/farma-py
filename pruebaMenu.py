#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaMenu.py
#
# Creado: 20/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos que se importan de la librería estandar
import socket
import cgi

# Módulos que se importan de la aplicación
from includes.control.motorVista import MotorVista 
from modulos.producto.modelo.productoModelo import ProductoModelo
from modulos.afipRecibido.modelo.afipRecibidoModelo import AfipRecibidoModelo

nombre_equipo = socket.gethostname()
ip = socket.gethostbyname(nombre_equipo)

form = cgi.FieldStorage()

datos_pg = dict(
        ip = ip,
        tituloPagina = "Artículos",
        usuario = "Alvaro",
    )

botones_ac = ["botonBadge", "botonAgregar", "botonListar", "botonBuscar", 
             "botonEditar", "botonDescartar"]

botones_ev = []
alertas = []

datos_pg['tituloBadge'] = 'Artículos'
datos_pg['cantidad'] = 150

# Selector de acciones
accion = "Iniciar"
if "bt_agregar" in form: accion = "Agregar" 
elif "bt_listar" in form: accion = "Listar"
elif "bt_buscar" in form: accion = "Buscar"
elif "bt_editar" in form: accion = "Editar"
elif "bt_descartar" in form: accion = "Descartar"
else: accion = "Iniciar"

# Acción para iniciar
if accion == "Iniciar":
    datos_pg['tituloPanel'] = "Tabla de Artículos"
    datos_pg['info'] = ("Permite realizar acciones en la tabla seleccionando" 
                        " con los botones.")
    datos_pg['comentario'] = "INICIO !!!!"
    alertas = ["alertaInfo",]
    datos_pg['alertaInfo'] = 'Seleccione una acción con los <b>BOTONES</b>.'


# Acción para agregar    
if accion == "Agregar": 
    datos_pg['tituloPanel'] = "Agrega Artículo"
    datos_pg['info'] = "Permite agregar un artículo a la tabla."
    datos_pg['comentario'] = "Voy a agregar un artículo nuevo !!!! <br>"
    botones_ev = ["botonConfirmar",]

# Acción para listar   
if accion == "Listar": 
    datos_pg['tituloPanel'] = "Listado de Artículos"
    datos_pg['info'] = "Permite listar los artículos de la tabla."
    datos_pg['comentario'] = "Voy a listar los artículos de la tabla !!!! <br>"
   
# Acción para Buscar    
if accion == "Buscar": 
    datos_pg['tituloPanel'] = "Busca Artículo"
    datos_pg['info'] = "Permite buscar un artículo a la tabla."
    datos_pg['comentario'] = "Voy a buscar un artículo nuevo !!!! <br>"
    botones_ev = ["botonConfirmar", "botonVolver"]
            
producto = ProductoModelo()
producto.set_id(100205) 
dato = producto.find()
if dato == None:
    datos_pg['id'] = producto.get_id()
    datos_pg['nombre'] = "Producto Inexistente..."
else:
    datos_pg['id'] = producto.get_id()
    datos_pg['nombre'] = producto.get_nombre()
    
datos_pg['prueba'] = '<b>Artículo con Ñ</b>'
pagina = MotorVista().arma_vista(botones_ac, botones_ev, alertas, datos_pg)

print(pagina)

print(accion, "<br>")
producto.count()
print("registros: ", producto.get_cantidad(), "<br>")
print("AFIP Recibidos<br>")
afip_recibido = AfipRecibidoModelo()
afip_recibido.count()
print("registros: ", afip_recibido.get_cantidad(), "<br>")
tabla = open("tabla.html", "w")
renglon = "Son: "+str(afip_recibido.get_cantidad())
line = tabla.write(renglon)

tabla.close()

    
