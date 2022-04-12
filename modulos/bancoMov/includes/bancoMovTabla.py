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


    def arma_tabla(self, datos, opciones, grupos_dicc):
        """
        Método que arma la tabla html para la vista.

        @param datos:
        @param opciones:
        @param grupos_dicc:
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
            "<th scope='col' title='Grupo, marca y comentario del movimiento'>"
                "Grupo/Marca/Com.</th>"
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
            # Suma por orden del grupo

            if int(dato[6]) == 0:
                if importe < 0:
                    nombre = "<b>DB SIN GRUPO</b>"
                    orden = "D99"
                else:
                    nombre = "<b>CR SIN GRUPO</b>"
                    orden = "C99"
            else:
                nombre = grupos_dicc[int(dato[6])][0]
                orden = grupos_dicc[int(dato[6])][1]

            if orden in totales:
                totales[orden][0] += 1
                totales[orden][1] += importe
            else:
                totales[orden] = [1, importe, nombre]

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
            # Grupo del movimiento:
            if int(dato[6]) == 0:
                grupo = ("<i class='fa fa-object-group'"
                          "style='color:red' "
                          "title='Sin grupo'></i>")
            else:
                nombre = grupos_dicc[int(dato[6])][0]
                grupo = ("<i class='fa fa-object-group'"
                          "style='color:blue' "
                          "title='"+nombre+"'></i>")
            # Marcas del movimiento:
            if dato[7] == 0:
                marca = ("<i class='fas fa-exclamation-triangle'"
                          "style='color:yellow' "
                          "title='Sin conciliar -Consultar-'></i>")
            elif dato[7] == 1:
                marca = ("<i class='fas fa-check' style='color:green' "
                          "title='Mov. conciliado'></i>")
            elif dato[7] == 2:
                marca = ("<i class='fas fa-ban' style='color:red'"
                          "title='Conciliado c/diferencia'></i>")
            else:
                marca = ("<i class='fas fa-times' style='color:yellow' "
                          "title='Marca no definida -Consultar-'></i>")
            # Comentario del movimiento:
            if dato[8] != "":
                comentario = ("<i class='far fa-comment-alt' "
                          "style='color:blue' title='"+dato[8]+"'></i>")
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
                "<td>"+str(grupo)+"  /   "+str(marca)+""
                "  /  "+str(comentario)+"</td>"
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
        if cont > 0:
            # Totales por orden de grupo
            pie_html += ("<b>Totales por Grupo del movimiento: </b><br>")
            for key in sorted(totales.keys()) :
                importe = locale.format("%.2f", totales[key][1], True)
                pie_html += (
                    "# "+str(totales[key][2])+": "+str(totales[key][0])+
                    " mov. por $ "+str(importe)+"<br>"
                    )
        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)
        # Cierra el archivo
        tabla.close()
