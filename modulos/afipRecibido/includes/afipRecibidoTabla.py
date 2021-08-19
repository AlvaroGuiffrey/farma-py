#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# afipRecibidoTabla.py
#
# Creado: 28/08/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
import locale


class AfipRecibidoTabla():
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

    def arma_tabla(self, datos, opciones, comentarios_prov, comprobantes_dicc):
        """
        Método que arma la tabla html para la vista.

        @param datos:
        @return: tabla.html
        """
        # Crea el archivo para la tabla:
        tabla = open("tabla.html", "w")
        # Arma los hidden y escribe la cabecera de la tabla html:
        cabecera_html = (
            "<!-- Datos de la cabecera de la tabla -->"
            "<div class='table-responsive-sm'>"
            "<h6> Listado de Comprobantes:</h6>"
            "<p>Desde: "+opciones['fecha_d']+" - "
            "Hasta: "+opciones['fecha_h']+""
            )
        hidden_html = (
            "<!-- Datos enviados por hidden -->"
            "<input type='hidden' name='fecha_d' "
            "value='"+opciones['fecha_d']+"'>"
            "<input type='hidden' name='fecha_h' "
            "value='"+opciones['fecha_h']+"'>"
            )
        if 'tipo' in opciones:
            if int(opciones['tipo']) > 0:
                tipo = comprobantes_dicc[int(opciones['tipo'])]
                cabecera_html += (" - Tipo: "+tipo+"")
            hidden_html += (
                "<input type='hidden' name='tipo' "
                "value='"+opciones['tipo']+"'>"
                )
        if 'numero' in opciones:
            if int(opciones['numero']) > 0:
                numero = opciones['numero']
                numero = numero.zfill(8)
                cabecera_html += (" - Número: "+numero+"")
            hidden_html += (
                "<input type='hidden' name='numero' "
                "value='"+str(opciones['numero'])+"'>"
                )
        if 'nombre_prov' in opciones:
            cabecera_html += (" - de: "+str(opciones['nombre_prov'])+"")
        if 'prov' in opciones:
            hidden_html += (
                "<input type='hidden' name='prov' "
                "value='"+opciones['prov']+"'>"
                )
        cabecera_html += (
            "</p><table class='table table-hover table-sm'>"
            "<thead><tr>"
            "<th scope='col'>#id</th>"
            "<th scope='col'>Fecha</th>"
            "<th scope='col'>Tipo</th>"
            "<th scope='col'>P.V.</th>"
            "<th scope='col'>Numero</th>"
            "<th scope='col'>Nombre Proveedor</th>"
            "<th scope='col'>Importe</th>"
            "<th scope='col' title='Comentario de recibidos AFIP'>"
            "<i class='fas fa-info' </th>"
            "<th scope='col' title='Recibido en Libro de IVA'>Rec.</th>"
            "<th scope='col' title='Comentario del Libro de IVA'>"
            "<i class='fas fa-info' </th>"
            "<th scope='col' title='Recibido de app del Proveedor'>Prov</th>"
            "<th scope='col' title='Comentario del Proveedor'>"
            "<i class='fas fa-info' </th>"
            "<th scope='col'>Acciones</th>"
            "</tr></thead><tbody>"
            "<!-- Datos de los renglones -->")
        tabla.write(cabecera_html)
        # Crea diccionario para totales:
        totales = {}
        # Crea diccionario con comentarios:
        if len(comentarios_prov) > 0:
            comentarios_dicc = {str(reng[1])+str(reng[2]).zfill(4)
                                  +str(reng[3]).zfill(8)+str(reng[4]):
                                  reng[5] for reng in comentarios_prov}
        else:
            comentarios_dicc = {}
        # Arma y escribe los renglones de la tabla html con los datos:
        cont = 0
        total = 0
        for dato in datos:
            # Da formato a los datos del renglón:
            # Cambia formato a la fecha:
            fecha_emi = date.strftime(dato[1], '%d/%m/%Y')
            # Reemplaza el tipo de comprobante:
            if dato[2] in comprobantes_dicc: tipo = comprobantes_dicc[dato[2]]
            else: tipo = "OTRO"
            # Cambia a negativo las notas de créditos:
            if dato[2] == 3 or dato[2] == 13 or dato[2] == 8:
                importe = dato[6] * -1
            else: importe = dato[6]
            # Suma a totales:
            if dato[2] in totales:
                totales[dato[2]][0] += 1
                totales[dato[2]][1] += importe
            else:
                totales[dato[2]] = [1, importe]
            total += importe
            # Cambia formato del importe a moneda local:
            importe = locale.format("%.2f", (importe), True)
            # Observaciones sobre conciliación con otras tablas:
            if dato[7] == 1:
                rec_obs = ("<i class='fas fa-check' style='color:green' "
                          "title='Conciliado con Recibidos'></i>")
            elif dato[7] == 2:
                rec_obs = ("<i class='fas fa-exclamation-triangle'"
                          "style='color:yellow' "
                          "title='Diferencia en importes con Recibidos'></i>")
            else:
                rec_obs = ("<i class='fas fa-ban' style='color:red' "
                          "title='No registrado en Recibidos'></i>")
            if dato[8] == 1:
                prov_obs = ("<i class='fas fa-check' style='color:green' "
                          "title='Conciliado con Proveedores'></i>")
            elif dato[8] == 2:
                prov_obs = ("<i class='fas fa-exclamation-triangle'"
                          "style='color:yellow' "
                          "title='Diferencia en importes con Proveedores'></i>")
            else:
                prov_obs = ("<i class='fas fa-ban' style='color:red' "
                          "title='No registrado en Proveedores'></i>")
            # Comentarios en la tabla:
            if dato[10] == None or dato[10] == "":
                afip_com = " "
            else:
                afip_com = ("<i class='fas fa-info-circle' "
                            "style='color:blue' "
                            "title='"+str(dato[10])+"'></i>")
            # Comentarios en Recibido del Proveedor:
            clave = (str(dato[2])+str(dato[3]).zfill(4)+str(dato[4]).zfill(8)
                     +str(dato[9]))
            if clave in comentarios_dicc:
                prov_com = ("<i class='fas fa-info-circle' "
                            "style='color:blue' "
                            "title='"+str(comentarios_dicc[clave])+"'></i>")
            else:
                prov_com = " "
            # Escribe el renglón:
            renglon_html = (
                "<tr><td>"+str(dato[0])+"</td>"
                "<td>"+str(fecha_emi)+"</td>"
                "<td>"+str(tipo)+"</td>"
                "<td>"+str(dato[3]).zfill(4)+"</td>"
                "<td>"+str(dato[4]).zfill(8)+"</td>"
                "<td>"+str(dato[5])[0:30]+"</td>"
                "<td style='text-align:right;'>"+str(importe)+"</td>"
                "<td>"+str(afip_com)+"</td>"
                "<td>"+str(rec_obs)+"</td>"
                "<td></td>"
                "<td>"+str(prov_obs)+"</td>"
                "<td>"+str(prov_com)+"</td>"
                "<td><button type='button' class='btn btn-light btn-sm "
                "float-sm-right rounded-circle' style='font-size: 0.6em' "
                "title='Botón para ver datos' data-toggle='tooltip' "
                "onclick='javascrip:window.open(\"http://localhost/farma-py/"
                "appAfipRecibidoV.py?accion=Ver&id="+str(dato[0])+"\", \"Ventana\", "
                "\"width=600, height=500, top=100, left=100, menubar=0, "
                "toolbar=0, titlebar=1, location=0, scrollbars=1\"); void 0'>"
                "<i class='fas fa-search'></i></button>"
                "</td></tr>"
                )

            tabla.write(renglon_html)
            cont += 1

        # Escribe los datos que envia por hidden:
        tabla.write(hidden_html)
        # Arma y escribe el pie de la tabla html:
        total = locale.format("%.2f", (total), True)
        pie_html = (
            "<!-- Datos del pie de la tabla -->"
            "<caption> Son: $cantidad comprobante/s por $ "+total+"<br>"
            )
        if cont > 0:
            lista = sorted(totales.items())
            for item in lista:
                tipo = comprobantes_dicc[item[0]]
                importe = locale.format("%.2f", (item[1][1]), True)
                pie_html += (
                    "# "+str(item[1][0])+" "+str(tipo)+" por "
                    "$ "+importe+"<br>"
                    )

        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)
        # Cierra el archivo
        tabla.close()
