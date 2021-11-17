#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# tarjCuponInvTabla.py
#
# Creado: 17/11/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
import locale


class TarjCuponInvTabla():
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
        cabecera_html = (
            "<!-- Datos de la cabecera de la tabla -->"
            "<div class='table-responsive-sm'>"
            "<h6> Listado del Inventario de Cupones:</h6>"
            "<p>Cupones pendientes de pago al "+opciones['fecha']+" </p>"
            "<table class='table table-hover table-sm'>"
            "<thead><tr>"
            "<th scope='col'>#id</th>"
            "<th scope='col' title='Fecha Operación'>Fecha Op.</th>"
            "<th scope='col' title='Número de Cupón'>Cupón</th>"
            "<th scope='col' title='Nombre de producto'>Tarjeta</th>"
            "<th scope='col' title='Últimos números de tarjeta'>Nro.</th>"
            "<th scope='col' title='Importe de la operación'>Importe</th>"
            "<th scope='col' title='Fecha Presentación'>Present.</th>"
            "<th scope='col' title='Número del Lote'>Lote</th>"
            "<th scope='col' title='Marca de error y comentarios'>Marca</th>"
            "<th scope='col' title='Número de Liquidación'>Liquid.</th>"
            "<th scope='col' title='Acciones para el cupón'>Acciones</th>"
            "</tr></thead><tbody>"
            "<!-- Datos de los renglones -->")
        tabla.write(cabecera_html)

        # Arma y escribe los renglones de la tabla html con los datos:
        cont = total = 0
        for dato in datos:
            # Da formato a los datos del renglón:
            # Cambia formato a la fecha:
            fecha_ope = date.strftime(dato[2], '%d/%m/%Y')
            fecha_pre = date.strftime(dato[8], '%d/%m/%Y')
            # Reemplaza datos del producto:
            id_producto = int(dato[4])
            if id_producto in productos_dicc:
                nombre_producto = productos_dicc[id_producto][0]
                inicial_producto = productos_dicc[id_producto][1]
            else:
                nombre_producto = "Sin identificar Producto"
                inicial_producto = "OTRA"
            # Importe:
            importe = dato[6]
            # Suma total del listado:
            total += importe
            # Cambia formato del importe:
            importe = locale.format("%.2f", (importe), True)
            # Errores del cupón:
            if dato[7] == 0:
                tarj_error = ("<i class='fas fa-check' style='color:green' "
                          "title='Aceptado por operador'></i>")
            elif dato[7] == 1:
                tarj_error = ("<i class='fas fa-ban' style='color:red'"
                          "title='Rechazado por operador'></i>")
            elif dato[7] == 2:
                tarj_error = ("<i class='fas fa-times' style='color:yellow' "
                          "title='Anulado en operación -POSNET-'></i>")
            else:
                tarj_error = ("<i class='fas fa-exclamation-triangle'"
                          "style='color:yellow' "
                          "title='Marca no definida -Consultar-'></i>")
            # Comentario del cupón
            if dato[11] != "":
                tarj_comentario = ("<i class='far fa-comment-alt' "
                          "style='color:blue' title='"+dato[11]+"'></i>")
            else:
                tarj_comentario = ""
            # Escribe el renglón:
            renglon_html = (
                "<tr><td>"+str(dato[0])+"</td>"
                "<td>"+str(fecha_ope)+"</td>"
                "<td>"+str(dato[1])+"</td>"
                "<td title='"+str(inicial_producto)+"'>"
                +str(nombre_producto)+"</td>"
                "<td>"+str(dato[3]).zfill(4)+"</td>"
                "<td style='text-align:right;'>"+str(importe)+"</td>"
                "<td>"+str(fecha_pre)+"</td>"
                "<td>"+str(dato[9]).zfill(3)+"</td>"
                "<td>"+str(tarj_error)+"    "+str(tarj_comentario)+"</td>"
                "<td>"+str(dato[10])+"</td>"
                "<td><button type='button' class='btn btn-light btn-sm "
                "float-sm-right rounded-circle' style='font-size: 0.6em' "
                "title='Botón para ver datos' data-toggle='tooltip' "
                "onclick='javascrip:window.open(\"http://localhost/farma-py/"
                "appTarjCuponV.py?accion=Ver&id="+str(dato[0])+"\", \"Ventana\", "
                "\"width=600, height=500, top=100, left=100, menubar=0, "
                "toolbar=0, titlebar=1, location=0, scrollbars=1\"); void 0'>"
                "<i class='fas fa-search'></i></button>"
                "</td></tr>"
                )
            tabla.write(renglon_html)
            cont += 1

        # Arma y escribe el pie de la tabla html:
        # Totales del listado
        total = locale.format("%.2f", (total), True)
        pie_html = (
            "<!-- Datos del pie de la tabla -->"
            "<caption> Son: "+str(cont)+" cupon/es pendientes de pago por $ "+str(total)+"<br>"
            )
        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)
        # Cierra el archivo
        tabla.close()
