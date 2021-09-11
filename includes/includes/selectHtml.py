#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# selectHtml.py
#
# Creado: 10/09/2021
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

class SelectHtml(object):
    """
    Clase que arma un select para la vista.

    Arma un select con los datos recibidos en una archivo html5 para
    usar en la vista.
    """

    def arma_select(self, dicc, nombre):
        """
        Arma un select con los datos recibidos para la vista.

        Con los datos recibidos arma un select en un archivo html para
        usar en la vista.
        @param datos: resultado de la consulta a la select MySQL.
        @param nombre: con el que denominamos a la variable y al archivo.
        @return: select_<nombre>.html - archivo html5 que envía
        el valor seleccionado por método GET-POST en la variable: <nombre>.
        """
        # Crea el archivo para la select:
        archivo = open("select_"+nombre+".html", "w")
        # Arma y escribe la cabecera de la select html:
        cabecera_html = ("<select id='"+nombre+"' name='"+nombre+"' >")
        archivo.write(cabecera_html)
        # Arma y escribe los renglones de la select html con los datos:
        renglon_html = ("<option value='0' selected> Seleccione ...</option>")
        archivo.write(renglon_html)
        datos = dicc.items()
        for dato in datos:
            # Escribe el renglón:
            renglon_html = (
                "<option value='"+str(dato[0])+"'>"+str(dato[1][0])+"</option>")
            archivo.write(renglon_html)

        # Arma y escribe el pie de la select html:
        pie_html = ("</select>")
        archivo.write(pie_html)
        # Cierra el archivo
        archivo.close()
