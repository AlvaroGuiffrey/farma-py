#!C:\Users\AlvaroG\AppData\Local\Programs\Python\Python310\python.exe
# -*- coding: utf-8 -*-
#
# pruebaDB.py
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la aplicación
from modulos.producto.modelo.productoActiveRecord import ProductoActiveRecord


class PruebaDB(ProductoActiveRecord):

    def inicio(self):

        print("Content-Type: text/html")
        print("""
            <TITLE>MySQL</TITLE>
        """)

        producto = ProductoActiveRecord()
        producto.find()

        print("Id: ", producto.get_id(), " - Nombre: ", producto.get_nombre(), "<br>")




PruebaDB().inicio()
