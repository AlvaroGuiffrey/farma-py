# -*- coding: latin-1 -*-
#
# chequeEmiTabla.py
#
# Creado: 21/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date, datetime
import locale


class ChequeEmiTabla():
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

        # Reescribe las opciones:
        if int(opciones['tipo']) == 1:
            tipo_fecha = "Emisión"
            tipo = 1
        elif int(opciones['tipo']) == 2:
            tipo_fecha = "Pago"
            tipo = 2
        elif int(opciones['tipo']) == 3:
            tipo_fecha = "Débito"
            tipo = 3
        else:
            tipo_fecha = ""
            tipo = 0

        # Cambia formato:
        fecha_r = opciones['fecha'].split("-")
        fecha = (fecha_r[2]+"/"+fecha_r[1]+"/"+fecha_r[0])
        fecha_r = opciones['fecha_d'].split("-")
        fecha_d = (fecha_r[2]+"/"+fecha_r[1]+"/"+fecha_r[0])
        fecha_r = opciones['fecha_h'].split("-")
        fecha_h = (fecha_r[2]+"/"+fecha_r[1]+"/"+fecha_r[0])
        # Escribe el título y subtítulo de la tabla:
        if opciones['accion'] == "ConfListarInv":
            titulo = ("<h6> Listado del Inventario de Cheques Emitidos:</h6>")
            subtitulo = ("<p>Pendientes de pago al: "+fecha)
        else:
            titulo = ("<h6> Listado de Cheques Emitidos:</h6>")
            subtitulo = ("<p>Fecha de "+tipo_fecha+" desde: "+fecha_d+
            " - hasta: "+fecha_h)
            if opciones['nombre_emi'] != "0":
                subtitulo += (" a: "+opciones['nombre_emi'])
            if opciones['estado_cheque'] != "TODOS":
                subtitulo += (" c/estado: "+opciones['estado_cheque'])
            subtitulo += ("</p>")

        # Escribe los hidden:

        hidden_html = (
            "<!-- Datos enviados por hidden -->"
            "<input type='hidden' name='fecha' "
            "value='"+opciones['fecha']+"'>"
            "<input type='hidden' name='fecha_d' "
            "value='"+opciones['fecha_d']+"'>"
            "<input type='hidden' name='fecha_h' "
            "value='"+opciones['fecha_h']+"'>"
            "<input type='hidden' name='tipo' "
            "value='"+str(tipo)+"'>"
            "<input type='hidden' name='tipo_fecha' "
            "value='"+tipo_fecha+"'>"
            "<input type='hidden' name='nombre_emi' "
            "value='"+opciones['nombre_emi']+"'>"
            "<input type='hidden' name='estado_cheque' "
            "value='"+opciones['estado_cheque']+"'>"
            "<input type='hidden' name='accion' "
            "value='"+opciones['accion']+"'>"
            )

        # Escribe la cabecera de la tabla:
        cabecera_html = (
            "<!-- Datos de la cabecera de la tabla -->"
            "<div class='table-responsive-sm'>"
            +str(titulo)+str(subtitulo)+
            "<table class='table table-hover table-sm'>"
            "<thead><tr>"
            "<th scope='col'>#id</th>"
            "<th scope='col' title='Número del cheque'>Nro.Ch.</th>"
            "<th scope='col' title='Fecha Emisión del cheque'>Fecha Emi.</th>"
            "<th scope='col' title='Importe del cheque'>Importe</th>"
            "<th scope='col' title='Fecha Pago'>Fecha Pago</th>"
            "<th scope='col' title='Nombre del beneficiario del cheque'>"
            "Orden de</th>"
            "<th scope='col' title='Estado del cheque'>Estado</th>"
            "<th scope='col' title='Fecha débito en Banco'>"
            "Fecha Deb.</th>"
            "<th scope='col' title='Acciones a realizar'>Acciones</th>"
            "</tr></thead><tbody>"
            "<!-- Datos de los renglones -->")
        tabla.write(cabecera_html)
        # Crea diccionario para totales:
        totales = {}

        # Arma y escribe los renglones de la tabla html con los datos:
        cont = cont_control = 0
        total_emi = total_pago_pend = total_pago_cobro = total_banco = 0
        for dato in datos:
            # Da formato a los datos del renglón:
            # Cambia formato a las fechas:
            fecha_emi = date.strftime(dato[2], '%d/%m/%Y')
            fecha_pago = date.strftime(dato[3], '%d/%m/%Y')
            if dato[7] == None:
                fecha_banco = "00/00/0000"
            else:
                fecha_banco = date.strftime(dato[7], '%d/%m/%Y')
            # Cambia formato al importe del cheque:
            importe = locale.format("%.2f", (dato[4]), True)
            # Suma a totales:
            total_emi += float(dato[4])
            if dato[7] == None:
                fecha_hoy = date.strftime(datetime.now(), '%d/%m/%Y')
                if (fecha_pago > fecha_hoy) == True:
                    total_pago_pend += float(dato[4])
                else:
                    total_pago_cobro += float(dato[4])
            else:
                total_banco += float(dato[4])

            # Escribe el renglón:
            renglon_html = (
                "<tr><td>"+str(dato[0])+"</td>"
                "<td>"+str(dato[1])+"</td>"
                "<td>"+str(fecha_emi)+"</td>"
                "<td style='text-align:right;'>"+str(importe)+"</td>"
                "<td>"+str(fecha_pago)+"</td>"
                "<td>"+str(dato[5])+"</td>"
                "<td>"+str(dato[6])+"</td>"
                "<td>"+str(fecha_banco)+"</td>"
                "<td><button type='button' class='btn btn-light btn-sm "
                "float-sm-right rounded-circle' style='font-size: 0.6em' "
                "title='Botón para ver datos' data-toggle='tooltip' "
                "onclick='javascrip:window.open(\"http://localhost/farma-py/"
                "appChequeEmiV.py?accion=Ver&id="+str(dato[0])+"\", \"Ventana\", "
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
        # Totales del listado
        total_emi = locale.format("%.2f", (total_emi), True)
        total_banco = locale.format("%.2f", (total_banco), True)
        total_pago_pend = locale.format("%.2f", (total_pago_pend), True)
        total_pago_cobro = locale.format("%.2f", (total_pago_cobro), True)
        pie_html = ("<!-- Datos del pie de la tabla -->")
        if opciones['accion'] == "ConfListarInv":
            pie_html +=("<caption> Son: "+str(cont)+" cheque/es pendientes. <br>")
            pie_html += ("Total pendiente $ "+str(total_emi)+"<br>")
        else:
            pie_html +=("<caption> Son: "+str(cont)+" cheque/es emitidos. <br>")
            pie_html += ("Total emitidos $ "+str(total_emi)+"<br>")
            pie_html += ("Total debitados $ "+str(total_banco)+"<br>")
            pie_html += ("Total pendientes $ "+str(total_pago_pend)+"<br>")
            pie_html += ("<b>Total al cobro $ "+str(total_pago_cobro)+"</b><br>")
        pie_html += ("</caption></tbody></table></div>")
        tabla.write(pie_html)

        # Cierra el archivo
        tabla.close()
