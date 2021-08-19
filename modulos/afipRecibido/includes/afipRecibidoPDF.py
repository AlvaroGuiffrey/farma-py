#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
#
# afipRecibidoPDF.py
#
# Creado: 11/09/2019
# Versión: 001
# Última modificación:
#
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos de la librería estandar:
from fpdf import FPDF
from datetime import datetime
from datetime import date
import locale


class PDF(FPDF):
    """
    Clase que reescribe métodos de la clase FPDF.

    Reescribe los métodos header() y Footer() de la clase FPDF.
    """

    def header(self):
        """
        Reescribe el método header() de la clase FPDF
        """

        # Carga la fecha y hora actual:
        ahora = datetime.now()
        fecha = datetime.strftime(ahora, '%d/%m/%Y %H:%M')
        # Titulos del archivo PDF:
        self.set_font('Arial', '', 9)
        self.cell(30, 10, "Farmacia Villa Elisa SRL", 0, 0, 'L')
        self.cell(230, 10, "Fecha: "+fecha+"", 0, 0, 'R')
        self.ln(3)
        self.set_font('Arial', 'BU', 12)
        self.cell(0, 10, "Listado de Comprobantes Recibidos AFIP", 0, 0, 'C')
        self.ln(5)
        self.set_font('Arial', 'I', 9)
        self.cell(0, 10, detalle, 0, 0, 'L')
        self.ln(5)
        # Encabezado de los renglones del archivo PDF:
        self.line(20, 25, 285, 25)
        self.set_font('Arial', '', 9)
        self.cell(6, 9, "#", 0, 0, 'C')
        self.cell(22, 9, 'FECHA', 0, 0, 'C')
        self.cell(36, 8, 'COMPROBANTE', 0, 0, 'C')
        self.cell(70, 9, 'NOMBRE PROVEEDOR', 0, 0, 'C')
        self.cell(25, 9, '--- GRAVADO --', 0, 0, 'C')
        self.cell(25, 9, ' NO GRAVADO', 0, 0, 'C')
        self.cell(25, 9, '---- EXENTO ---', 0, 0, 'C')
        self.cell(25, 9, '------- IVA -------', 0, 0, 'C')
        self.cell(25, 9, '----- TOTAL -----', 0, 0, 'C')
        self.ln(5)
        self.line(20, 29, 285, 29)

    def footer(self):
        """
        Reescribe el método footer() de la clase FPDF
        """
        # Pie de página del archivo PDF:
        self.set_y(-15)
        self.set_font('Arial', 'I', 6)
        self.cell(0, 10, 'Pagina '+str(self.page_no())+'/{nb}', 0, 0, 'C')



class AfipRecibidoPDF(PDF):
    """
    Clase que escribe un archivo PDF con datos para descargar.

    Escribe un archivo PDF con datos del listado que se graba en el
    directorio: 'archivos' de la aplicación. También se puede abrir
    desde el navegador.
    """


    def escribir_pdf(self, datos, detalle_pdf, comprobantes_dicc):
        """
        Escribe el archivo PDF con los datos recibidos.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
        global detalle
        detalle = detalle_pdf
        # Configura el PDF:
        self.alias_nb_pages()
        self.set_title("Listado Compr. Rec. AFIP")
        self.set_left_margin(20)
        self.set_auto_page_break(True , 10.0)
        self.add_page('L')
        self.set_font('Arial', '', 9)
        # Escribe renglones del PDF:
        totales = {}
        totales[0] = [0, 0, 0, 0, 0, 0]
        cont = 0
        for dato in datos:
            # Cambia formato a los datos:
            # Cambia formato a la fecha:
            fecha_emi = date.strftime(dato[1], '%d/%m/%Y')
            # Reemplaza el tipo de comprobante:
            if dato[2] in comprobantes_dicc:
                tipo = comprobantes_dicc[int(dato[2])]
            else: tipo = "OTRO"
            # Arma el comprobante (tipo-pto Vta-numero):
            punto_venta = str(dato[3]).zfill(4)
            numero = str(dato[4]).zfill(8)
            comprobante = tipo+"-"+punto_venta+"-"+numero
            # Rebana el nombre del proveedor:
            nombre = dato[5][:35]
            # Pone en negativo NC notas de c´redito:
            if dato[2] == 3 or dato[2] == 13 or dato[2] == 8:
                importe_gravado = dato[6] * -1
                importe_no_grav = dato[7] * -1
                importe_exento = dato[8] * -1
                iva = dato[9] * -1
                importe_total = dato[10] * -1
            else:
                importe_gravado = dato[6]
                importe_no_grav = dato[7]
                importe_exento = dato[8]
                iva = dato[9]
                importe_total = dato[10]
            # Suma a totales:
            if dato[2] in totales:
                totales[dato[2]][0] += 1
                totales[dato[2]][1] += importe_gravado
                totales[dato[2]][2] += importe_no_grav
                totales[dato[2]][3] += importe_exento
                totales[dato[2]][4] += iva
                totales[dato[2]][5] += importe_total
            else:
                totales[dato[2]] = [1, importe_gravado, importe_no_grav,
                                    importe_exento, iva, importe_total]
            totales[0][0] += 1
            totales[0][1] += importe_gravado
            totales[0][2] += importe_no_grav
            totales[0][3] += importe_exento
            totales[0][4] += iva
            totales[0][5] += importe_total
            # Cambia a formato de moneda local:
            importe_gravado = locale.format("%.2f", (importe_gravado), True)
            importe_no_grav = locale.format("%.2f", (importe_no_grav), True)
            importe_exento = locale.format("%.2f", (importe_exento), True)
            iva = locale.format("%.2f", (iva), True)
            importe_total = locale.format("%.2f", (importe_total), True)
            # Renglón del archivo PDF:
            self.cell(6, 8, str(dato[0]), 0, 0, 'C')
            self.cell(22, 8, str(fecha_emi), 0, 0, 'C')
            self.cell(36, 8, str(comprobante), 0, 0, 'C')
            self.cell(70, 8, str(nombre), 0, 0)
            self.cell(25, 8, str(importe_gravado), 0, 0, 'R')
            self.cell(25, 8, str(importe_no_grav), 0, 0, 'R')
            self.cell(25, 8, str(importe_exento), 0, 0, 'R')
            self.cell(25, 8, str(iva), 0, 0, 'R')
            self.cell(25, 8, str(importe_total), 0, 0, 'R')
            self.cell(6, 8, '__', 0, 0, 'C')
            self.ln(4)
            cont += 1

        # Totales del archivo PDF:
        cantidad = totales[0][0]
        total_gravado = totales[0][1]
        total_no_grav = totales[0][2]
        total_exento = totales[0][3]
        total_iva = totales[0][4]
        total_total = totales[0][5]
        total_gravado = locale.format("%.2f", (total_gravado), True)
        total_no_grav = locale.format("%.2f", (total_no_grav), True)
        total_exento = locale.format("%.2f", (total_exento), True)
        total_iva = locale.format("%.2f", (total_iva), True)
        total_total = locale.format("%.2f", (total_total), True)
        # Renglon de total general:
        self.ln(2)
        y = self.get_y()
        self.line(20, y, 285, y)
        self.cell(134, 8, "Son: "+str(cantidad)+" comprobantes, que suman: ",
                  0, 0, 'R')
        self.cell(25, 8, str(total_gravado), 0, 0, 'R')
        self.cell(25, 8, str(total_no_grav), 0, 0, 'R')
        self.cell(25, 8, str(total_exento), 0, 0, 'R')
        self.cell(25, 8, str(total_iva), 0, 0, 'R')
        self.cell(25, 8, str(total_total), 0, 0, 'R')
        self.ln(4)
        # Descarga el archivo PDF:
        self.output('C:/xampp/htdocs/farma-py/archivos/recibidosAFIP.pdf', 'F' )
