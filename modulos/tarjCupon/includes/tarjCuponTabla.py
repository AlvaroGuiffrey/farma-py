# -*- coding: utf-8 -*-
#
# tarjCuponTabla.py
#
# Creado: 07/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
import locale


class TarjCuponTabla():
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
            tipo_fecha = "Operación"
        elif int(opciones['tipo']) == 2:
            tipo_fecha = "Presentación"
        else:
            tipo_fecha = ""
        cabecera_html = (
            "<!-- Datos de la cabecera de la tabla -->"
            "<div class='table-responsive-sm'>"
            "<h6> Listado de Cupones:</h6>"
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
            "<th scope='col' title='Marca de error y comentarios'>Marca</th>"
            "<th scope='col' title='Número de Liquidación'>Liquid.</th>"
            "<th scope='col' title='Acciones para el cupón'>Acciones</th>"
            "</tr></thead><tbody>"
            "<!-- Datos de los renglones -->")
        tabla.write(cabecera_html)
        # Crea diccionario para totales:
        totales = {}
        totales_lote = {}

        # Arma y escribe los renglones de la tabla html con los datos:
        cont = cont_control = cupon_control = total = 0
        for dato in datos:
            # Da formato a los datos del renglón:
            # Cambia formato a la fecha:
            fecha_ope = date.strftime(dato[2], '%d/%m/%Y')
            fecha_pre = date.strftime(dato[8], '%d/%m/%Y')
            # Reemplaza datos del producto:
            nombre_producto = "VISA"
            inicial_producto = "VS-CR"
            id_producto = int(dato[4])
            if id_producto in productos_dicc:
                nombre_producto = productos_dicc[id_producto][0]
                inicial_producto = productos_dicc[id_producto][1]
            else:
                nombre_producto = "Sin identificar Producto"
                inicial_producto = "OTRA"
            # Importe:
            importe = dato[6]
            # Suma a totales:
            # Suma por fecha operación
            if dato[2] in totales:
                totales[dato[2]][0] += 1
                totales[dato[2]][1] += importe
            else:
                totales[dato[2]] = [1, importe]
            # Suma por Lote
            if dato[9] in totales_lote:
                totales_lote[dato[9]][0] += 1
                totales_lote[dato[9]][1] += importe
                totales_lote[dato[9]][2] = dato[8]
            else:
                totales_lote[dato[9]] = [1, importe, dato[8]]
            # Suma total del listado
            total += importe
            # Cambia formato del importe a modato[9n][2] = dato[8]eda local:
            importe = locale.format("%.2f", (importe), True)
            #importe = ({:,.2f}'.format(importe).replace(",", "@")
            #    .replace(".", ",").replace("@", "."))
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
            "<caption> Son: "+str(cont)+" cupon/es por $ "+str(total)+"<br>"
            )

        if cont > 0:
            # Totales por fecha de las operaciones
            pie_html += ("<b>Totales por Fechas de Operación: </b><br>")
            for item in totales:
                fecha = date.strftime(item, '%d/%m/%Y')
                importe = locale.format("%.2f", totales[item][1], True)
                pie_html += (
                    "# "+str(totales[item][0])+" cupon/es del "+str(fecha)+
                    " por $ "+str(importe)+"<br>"
                    )
            # Totales por lote
            pie_html += ("<b>Totales por Lote de Presentación: </b><br>")
            for item in totales_lote:
                fecha = date.strftime(totales_lote[item][2], '%d/%m/%Y')
                #fecha = totales_lote[item][2]
                importe = locale.format("%.2f", totales_lote[item][1], True)
                #importe = totales_lote[item][1]
                pie_html += (
                    "# "+str(totales_lote[item][0])+" cupon/es del Lote:"
                    +str(item)+" ("+str(fecha)+") por $ "
                    +str(importe)+"<br>"
                    )
        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)
        # Cierra el archivo
        tabla.close()
