#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: latin-1 -*-
#
# bancoMovTabla.py
#
# Creado: 04/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
import locale


class BancoMovTabla():
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
            tipo_fecha = "Movimiento"
        elif int(opciones['tipo']) == 2:
            tipo_fecha = "Valor"
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
            "<th scope='col' title='Fecha del movimiento'>Fecha Mov.</th>"
            "<th scope='col' title='Fecha valor del movimiento'>Fecha Valor</th>"
            "<th scope='col' title='Importe del movimiento'>Importe</th>"
            "<th scope='col' title='Número del movimiento'>Número</th>"
            "<th scope='col' title='Concepto del movimiento'>Concepto</th>"
            "<th scope='col' title='Marca y comentario del movimiento'>Marca/Com.</th>"
            "<th scope='col' title='Acciones para el movimiento'>Acciones</th>"
            "</tr></thead><tbody>"
            "<!-- Datos de los renglones -->")
        tabla.write(cabecera_html)
        # Crea diccionario para totales:
        totales = {}

        # Arma y escribe los renglones de la tabla html con los datos:
        cont = cont_control = cont_deb = cont_cred = 0
        total = total_deb = total_cred = 0
        for dato in datos:
            # Da formato a los datos del renglón:
            # Cambia formato a la fecha:
            fecha_mov = date.strftime(dato[1], '%d/%m/%Y')
            fecha_valor = date.strftime(dato[2], '%d/%m/%Y')
            # Importe:
            importe = dato[3]
            # Suma a totales:
            # Suma por fecha operación
            # >>>>>>>>>> ver totales
            """
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
            """
            #  >>>>>>>>> Fin ver totales
            # Suma totales del listado
            total += importe
            if importe < 0:
                cont_deb += 1
                total_deb += importe
            else:
                cont_cred +=1
                total_cred += importe
            # Cambia formato del importe a formato local:
            importe = locale.format("%.2f", (importe), True)
            #importe = ({:,.2f}'.format(importe).replace(",", "@")
            #    .replace(".", ",").replace("@", "."))
            # Marcas del movimiento:
            if dato[6] == 0:
                marca = ("<i class='fas fa-exclamation-triangle'"
                          "style='color:yellow' "
                          "title='Sin conciliar -Consultar-'></i>")
            elif dato[6] == 1:
                marca = ("<i class='fas fa-check' style='color:green' "
                          "title='Mov. conciliado'></i>")
            elif dato[6] == 2:
                marca = ("<i class='fas fa-ban' style='color:red'"
                          "title='Conciliado c/diferencia'></i>")
            else:
                marca = ("<i class='fas fa-times' style='color:yellow' "
                          "title='Marca no definida -Consultar-'></i>")
            # Comentario del movimiento:
            if dato[7] != "":
                comentario = ("<i class='far fa-comment-alt' "
                          "style='color:blue' title='"+dato[7]+"'></i>")
            else:
                comentario = ""
            # Escribe el renglón:
            renglon_html = (
                "<tr><td>"+str(dato[0])+"</td>"
                "<td>"+str(fecha_mov)+"</td>"
                "<td>"+str(fecha_valor)+"</td>"
                "<td style='text-align:right;'>"+str(importe)+"</td>"
                "<td>"+str(dato[4])+"</td>"
                "<td>"+str(dato[5])+"</td>"
                "<td>"+str(marca)+"    "+str(comentario)+"</td>"
                "<td><button type='button' class='btn btn-light btn-sm "
                "float-sm-right rounded-circle' style='font-size: 0.6em' "
                "title='Botón para ver datos' data-toggle='tooltip' "
                "onclick='javascrip:window.open(\"http://localhost/farma-py/"
                "appBancoMovV.py?accion=Ver&id="+str(dato[0])+"\", \"Ventana\", "
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
        total_deb = locale.format("%.2f", (total_deb), True)
        total_cred = locale.format("%.2f", (total_cred), True)
        pie_html = (
            "<!-- Datos del pie de la tabla -->"
            "<caption> Son: "+str(cont)+" movimiento/s por $ "+str(total)+"<br>"
            "Débitos: "+str(cont_deb)+" movimiento/s por $ "+str(total_deb)+"<br>"
            "Créditos: "+str(cont_cred)+" movimiento/s por $ "+str(total_cred)+"<br>"
            )
        """
        if cont > 0:
            # Totales por
            pie_html += ("<b>Totales por Fechas de Operación: </b><br>")
            for item in totales:
                fecha = date.strftime(item, '%d/%m/%Y')
                importe = locale.format("%.2f", totales[item][1], True)
                pie_html += (
                    "# "+str(totales[item][0])+" cupon/es del "+str(fecha)+
                    " por $ "+str(importe)+"<br>"
                    )
            # Totales por
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
        """
        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)
        # Cierra el archivo
        tabla.close()
