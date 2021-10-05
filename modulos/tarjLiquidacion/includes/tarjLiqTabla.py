#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjLiqTabla.py
#
# Creado: 30/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
import locale


class TarjLiqTabla():
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
        locale.setlocale(locale.LC_ALL, 'es_AR')

    def arma_tabla(self, datos, opciones, productos_dicc):
        """
        Método que arma la tabla html para la vista.

        @param datos:
        @param opciones:
        @param productos_dicc:
        @return: tabla.html
        """
        # Crea el archivo para la tabla:
        tabla = open("tabla.html", "w")

        # Arma los hidden y escribe la cabecera de la tabla html:
        if int(opciones['tipo']) == 1:
            tipo_fecha = "Proceso"
        elif int(opciones['tipo']) == 2:
            tipo_fecha = "Pago"
        else:
            tipo_fecha = ""

        cabecera_html = (
            "<!-- Datos de la cabecera de la tabla -->"
            "<div class='table-responsive-sm'>"
            "<h6> Listado de Liquidaciones:</h6>"
            "<p>Fecha de "+tipo_fecha+" desde: "+opciones['fecha_d']+" - "
            "hasta: "+opciones['fecha_h']+""
            "</p><table class='table table-hover table-sm'>"
            "<thead><tr>"
            "<th scope='col'>#id</th>"
            "<th scope='col' title='Fecha Proceso'>Fecha Pr.</th>"
            "<th scope='col' title='Fecha Pago'>Fecha Pago</th>"
            "<th scope='col' title='Número de Liquidación'>Nro.Liq.</th>"
            "<th scope='col' title='Nombre de producto'>Producto</th>"
            "<th scope='col' colspan='2' "
            "title='Marca sobre la cantidad de cupones'>Cupones</th>"
            "<th scope='col' title='Importe bruto de la liquidación'>"
            "Imp.Bruto</th>"
            "<th scope='col' title='Importe de descuentos de la liquidación'>"
            "Imp.Desc.</th>"
            "<th scope='col' title='Importe neto de la liquidación'>"
            "Imp.Neto</th>"
            "<th scope='col' colspan='2' title='Operación por la que se "
            "acreditó en Banco'>Banco Oper.</th>"
            "<th scope='col' title='Acciones a realizar'>Acciones</th>"
            "</tr></thead><tbody>"
            "<!-- Datos de los renglones -->")
        tabla.write(cabecera_html)
        # Crea diccionario para totales:
        totales = {}

        # Arma y escribe los renglones de la tabla html con los datos:
        cont = cont_control = total_bruto = total_desc = total_neto = 0
        for dato in datos:
            # Da formato a los datos del renglón:
            # Cambia formato a las fechas:
            fecha_proceso = date.strftime(dato[2], '%d/%m/%Y')
            fecha_pago = date.strftime(dato[3], '%d/%m/%Y')
            # Reemplaza datos del producto:
            #nombre_producto = "VISA"
            #inicial_producto = "VS-CR"
            id_producto = int(dato[4])
            if id_producto in productos_dicc:
                nombre_producto = productos_dicc[id_producto][0]
                inicial_producto = productos_dicc[id_producto][1]
            else:
                nombre_producto = "Sin identificar Producto"
                inicial_producto = "OTRA"
            # Suma y cambia formato de los importes a moneda local:
            # Importe bruto
            bruto = dato[5]
            total_bruto += bruto
            bruto = locale.format("%.2f", (bruto), True)
            # Importe descuentos
            desc = dato[6]
            total_desc += desc
            desc = locale.format("%.2f", (desc), True)
            # Importe neto
            neto = dato[7]
            total_neto += neto
            neto = locale.format("%.2f", (neto), True)
            # Errores en cantidad de cupones:
            if dato[9] == 0:
                cupon_error = ("<i class='fas fa-asterisk' style='color:blue' "
                          "title='Cantidad de cupones sin verificar'></i>")
            elif dato[9] == 1:
                cupon_error = ("<i class='fas fa-check' style='color:green' "
                          "title='Verificado cantidad de cupones'></i>")
            elif dato[9] == 2:
                cupon_error = ("<i class='fas fa-ban' style='color:red' "
                          "title='Diferencia en la cantidad de cupones'></i>")
            else:
                cupon_error = ("<i class='fas fa-exclamation-triangle'"
                          "style='color:yellow' "
                          "title='Marca no definida -Consultar-'></i>")
            # Errores en acreditación del banco:
            if dato[10] == 0:
                banco_error = ("<i class='fas fa-asterisk' style='color:blue' "
                          "title='Acreditación sin verificar'></i>")
            elif dato[10] == 1:
                banco_error = ("<i class='fas fa-check' style='color:green' "
                          "title='Verificada la acreditación'></i>")
            elif dato[10] == 2:
                banco_error = ("<i class='fas fa-ban' style='color:red' "
                          "title='Diferencia en la acreditación'></i>")
            else:
                banco_error = ("<i class='fas fa-exclamation-triangle'"
                          "style='color:yellow' "
                          "title='Marca no definida -Consultar-'></i>")
            # Escribe el renglón:
            renglon_html = (
                "<tr><td>"+str(dato[0])+"</td>"
                "<td>"+str(fecha_proceso)+"</td>"
                "<td>"+str(fecha_pago)+"</td>"
                "<td>"+str(dato[1])+"</td>"
                "<td title='"+str(inicial_producto)+"'>"
                +str(nombre_producto)+"</td>"
                "<td style='text-align:right;'>"+str(dato[8])+"</td>"
                "<td>"+str(cupon_error)+"</td>"
                "<td style='text-align:right;'>"+str(bruto)+"</td>"
                "<td style='text-align:right;'>"+str(desc)+"</td>"
                "<td style='text-align:right;'>"+str(neto)+"</td>"
                "<td style='text-align:right;'>"+str(dato[12]).zfill(1)+"</td>"
                "<td>"+str(banco_error)+"</td>"
                "<td><button type='button' class='btn btn-light btn-sm "
                "float-sm-right rounded-circle' style='font-size: 0.6em' "
                "title='Botón para ver datos' data-toggle='tooltip' "
                "onclick='javascrip:window.open(\"http://localhost/farma-py/"
                "appTarjLiqV.py?accion=Ver&id="+str(dato[0])+"\", \"Ventana\", "
                "\"width=600, height=500, top=100, left=100, menubar=0, "
                "toolbar=0, titlebar=1, location=0, scrollbars=1\"); void 0'>"
                "<i class='fas fa-search'></i></button>"
                "</td></tr>"
                )
            tabla.write(renglon_html)
            cont += 1
        # Arma y escribe el pie de la tabla html:
        # Totales del listado
        total_bruto = locale.format("%.2f", (total_bruto), True)
        total_desc = locale.format("%.2f", (total_desc), True)
        total_neto = locale.format("%.2f", (total_neto), True)
        pie_html = (
            "<!-- Datos del pie de la tabla -->"
            "<caption> Son: "+str(cont)+" liquidación/es. <br>"
            )
        pie_html += ("Total Bruto $ "+str(total_bruto)+"<br>")
        pie_html += ("Descuentos  $ "+str(total_desc)+"<br>")
        pie_html += ("Total Neto  $ "+str(total_neto)+"<br>")
        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)

        # Cierra el archivo
        tabla.close()
