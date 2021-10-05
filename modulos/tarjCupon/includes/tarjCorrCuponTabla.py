#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjCorrCuponTabla.py
#
# Creado: 08/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
import locale


class TarjCorrCuponTabla():
    '''
    Clase para armar una tabla html para la vista.

    Permite armar una tabla, con etiquetas html para la vista, con los datos
    obtenidos del modelo.
    '''

    def __init__(self):
        """
        Método que inicializa los atributos de la instancia.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR.utf8')

    def arma_tabla(self, datos, opciones):
        """
        Método que arma la tabla html para la vista.

        @param datos:
        @param opciones:
        @return: tabla.html
        """
        # Crea el archivo para la tabla:
        tabla = open("tabla.html", "w")

        # Arma los hidden y escribe la cabecera de la tabla html:
        if int(opciones['tipo']) == 1:
            tipo_fecha = "Operación"
        elif int(opciones['tipo']) == 2:
            tipo_fecha = "Presentación"
        else:
            tipo_fecha = ""
        cabecera_html = (
            "<!-- Datos de la cabecera de la tabla -->"
            "<div class='table-responsive-sm'>"
            "<h6> Listado de Cupones Faltantes:</h6>"
            "<p>Fecha de "+tipo_fecha+" desde: "+opciones['fecha_d']+" - "
            "hasta: "+opciones['fecha_h']+""
            "</p><table class='table table-hover table-sm'>"
            "<thead><tr>"
            "<th scope='col'>#id</th>"
            "<th scope='col' title='Fecha Operación'>Fecha Op.</th>"
            "<th scope='col' title='Número de Cupón'>Cupón</th>"
            "<th scope='col' title='Nombre de producto'>Tarjeta</th>"
            "<th scope='col' title='Últimos números de tarjeta'>Nro.</th>"
            "<th scope='col' title='Importe de la operación'>Importe</th>"
            "<th scope='col' title='Fecha Presentación'>Present.</th>"
            "<th scope='col' title='Número del Lote'>Lote</th>"
            "<th scope='col' title='Marca de error'>Marca</th>"
            "<th scope='col' title='Número de Liquidación'>Liquid.</th>"
            "<th scope='col' title='Acciones para el cupón'>Acciones</th>"
            "</tr></thead><tbody>"
            "<!-- Datos de los renglones -->")
        tabla.write(cabecera_html)
        # Crea diccionario para totales:
        totales = {}
        totales_lote = {}

        # Arma y escribe los renglones de la tabla html con los datos:
        cont = 0
        for dato in datos:
            # Da formato a los datos del renglón:
            # Escribe el renglón:
            renglon_html = (
                "<tr><td></td>"
                "<td></td>"
                "<td>"+str(dato)+"</td>"
                "<td></td>"
                "<td></td>"
                "<td style='text-align:right;'></td>"
                "<td></td>"
                "<td></td>"
                "<td></td>"
                "<td></td>"
                "<td><button type='button' class='btn btn-light btn-sm "
                "float-sm-right rounded-circle' style='font-size: 0.6em' "
                "title='Botón para agregar datos' data-toggle='tooltip' "
                "onclick='javascrip:window.open(\"http://localhost/farma-py/"
                "appTarjCuponV.py?accion=Agregar&cupon="+str(dato)+"\", \"Ventana\", "
                "\"width=600, height=500, top=100, left=100, menubar=0, "
                "toolbar=0, titlebar=1, location=0, scrollbars=1\"); void 0'>"
                "<i class='fas fa-plus'></i></button></td></tr>"
                )
            tabla.write(renglon_html)
            cont += 1

        # Arma y escribe el pie de la tabla html:
        # Totales del listado
        pie_html = (
            "<!-- Datos del pie de la tabla -->"
            "<caption> Son: "+str(cont)+" cupon/es faltantes.<br>"
            )
        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)
        # Cierra el archivo
        tabla.close()
