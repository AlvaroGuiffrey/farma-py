#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# select.py
#
# Creado: 09/09/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

class Select(object):
    """
    Clase que arma un select para la vista.

    Arma un select con los datos recibidos en una archivo html para
    usar en la vista con Boostrap.
    """

    def arma_select(self, dicc, cantidad, nombre):
        """
        Arma un select con los datos recibidos para la vista.

        Con los datos recibidos arma un select en un archivo html para
        usar en la vista.
        @param datos: resultado de la consulta a la select MySQL.
        @param cantidad: cantidad de renglones de la consulta.
        @param nombre: con el que denominamos a la variable y al archivo.
        @return: select_<nombre>.html - archivo html (bootstrap 4) que envía
        el valor seleccionado por método GET-POST en la variable: <nombre>.
        """
        # Crea el archivo para la select:
        archivo = open("select_"+nombre+".html", "w")
        # Arma y escribe la cabecera de la select html:
        cabecera_html = (
            "<div class='input-group-prepend'>"
            "<div class='input-group-text' data-toggle='tooltip' "
            "title='Seleccione opción'>"+str(nombre.capitalize())+": "
            "</div><div class='input-group-text' data-toggle='tooltip' "
            "title='Cantidad de opciones'>"
            "<span class='badge badge-pill badge-secondary'>"+str(cantidad)+" "
            "</span></div></div><select class='custom-select' id='"+nombre+"' "
            "name='"+nombre+"' >"
            )
        archivo.write(cabecera_html)
        # Arma y escribe los renglones de la select html con los datos:
        renglon_html = ("<option value='0' selected> Todos ...</option>")
        archivo.write(renglon_html)
        datos = dicc.items()
        for dato in datos:
            # Da formato a los datos del renglón:
            item = dato[1]
            item = item[:20]
            # Escribe el renglón:
            renglon_html = (
                "<option value='"+str(dato[0])+"'>"+str(item)+"</option>")
            archivo.write(renglon_html)

        # Arma y escribe el pie de la select html:
        pie_html = (
            "</select><div class='input-group-append'>"
            "<div class='input-group-text'></div></div>"
            )
        archivo.write(pie_html)
        # Cierra el archivo
        archivo.close()
