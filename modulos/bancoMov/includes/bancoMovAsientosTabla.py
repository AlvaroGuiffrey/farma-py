# -*- coding: latin-1 -*-
#
# bancoMovAsientosTabla.py
#
# Creado: 23/06/2022
# Versión: 002
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
import locale


class BancoMovAsientosTabla():
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


    def arma_tabla(self, asientos_dicc, opciones):
        """
        Método que arma la tabla html para la vista.

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
            "<h6> Listado de Asientos Contables:</h6>"
            "<p>Con movimientos de fecha "+tipo_fecha+" desde: "
            +str(opciones['fecha_d'])+" - hasta: "+str(opciones['fecha_h'])+
            "</p><hr>"
            )
        tabla.write(cabecera_html)
        # Crea diccionario para totales:
        totales = {}

        # Pone en 0 los contadores y totales auxiliares:
        cont = total_deb = total_cred = 0
        # Arma y escribe los renglones de la tabla html con los datos:
        for reng in asientos_dicc.values():

            if str(reng[0]) == "000000":
                cont += 1
                total_deb_asiento = total_cred_asiento = 0
                titulo_html = ("Asiento de:<b> "+str(reng[1]+"</b>"))
                tabla.write(titulo_html)
                enca_html = ("<table class='table table-hover table-sm'>"
                    "<thead><tr class='table-active'>"
                    "<th class='col-sm-2' scope='col' title='Cuenta del asiento'>Cuenta</th>"
                    "<th class='col-sm-8' scope='col' title='Nombre de la cuenta'>Nombre cuenta</th>"
                    "<th scope='col' title='Importe al débito'>Débito</th>"
                    "<th scope='col' title='Importe al crédito'>Crédito</th>"
                    "</tr></thead><tbody>")
                tabla.write(enca_html)


            elif str(reng[0]) == "999999":
                total_d = locale.format("%.2f", total_deb_asiento, True)
                total_c = locale.format("%.2f", total_cred_asiento, True)
                renglon_html = ("<tr><td></td><td>"+str(reng[1])+"</td>"
                    "<td style='text-align:right;'>"+str(total_d)+"</td>"
                    "<td style='text-align:right;'>"+str(total_c)+"</td></tr>"
                    "</tbody></table><hr>")
                tabla.write(renglon_html)


            else:
                #print(type(reng[1]))
                nombre = str(reng[1])
                #renglon_html = ("<tr><td>"+str(reng[0])+"</td>"
                #                "<td>"+str(reng[1])+"</td>")
                renglon_html = ("<tr><td>"+str(reng[0])+"</td>"
                                "<td>"+str(reng[1])+"</td>")
                #tabla.write(renglon_html)

                if int(reng[2]) == 0:
                    if int(reng[3]) < 0:
                        cred = reng[3] * (-1)
                    else:
                        cred = reng[3]
                    importe = locale.format("%.2f", cred, True)
                    renglon_html += ("<td ></td>"
                        "<td style='text-align:right;'>"+str(importe)+"</td></tr>")
                    total_cred_asiento += cred
                    total_cred += cred
                else:
                    if int(reng[2]) < 0:
                        deb = reng[2] * (-1)
                    else:
                        deb = reng[2]
                    importe = locale.format("%.2f", deb, True)
                    renglon_html += ("<td style='text-align:right;'>"+str(importe)+
                            "</td><td ></td></tr>")
                    total_deb_asiento += deb
                    total_deb += deb

                #print(str(reng[1]))
                #renglon_html = ("Renglones"+str(reng[0])+nombre+"<br>")
                #tabla.write(renglon_html)
                #tabla.write(renglon_html)
                tabla.write(renglon_html)

        fin_html =("</div>")
        tabla.write(fin_html)
        tabla.close()
