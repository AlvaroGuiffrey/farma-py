# -*- coding: utf-8 -*-
#
# chequeEmiPDF.py
#
# Creado: 24/03/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
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
        self.cell(0, 10, titulo, 0, 0, 'C')
        self.ln(5)
        self.set_font('Arial', 'I', 9)
        self.cell(0, 10, detalle, 0, 0, 'L')
        self.ln(5)
        # Encabezado de los renglones del archivo PDF:
        self.line(20, 25, 285, 25)
        self.set_font('Arial', '', 9)
        self.cell(10, 9, "#", 0, 0, 'C')
        self.cell(22, 9, 'NRO. CHEQUE', 0, 0, 'C')
        self.cell(22, 9, 'FECHA EMI.', 0, 0, 'C')
        self.cell(35, 9, '------ IMPORTE ------', 0, 0, 'R')
        self.cell(22, 9, 'FECHA PAGO', 0, 0, 'C')
        self.cell(70, 9, '------------------- ORDEN DE -------------------', 0, 0, 'L')
        self.cell(25, 9, '---- ESTADO ----', 0, 0, 'C')
        self.cell(22, 9, 'FECHA DEB.', 0, 0, 'C')
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



class ChequeEmiPDF(PDF):
    """
    Clase que escribe un archivo PDF con datos para descargar.

    Escribe un archivo PDF con datos del listado que se graba en el
    directorio: 'archivos/banco' de la aplicación. También se puede abrir
    desde el navegador.
    """

    def escribir_pdf(self, datos, titulo_pdf, detalle_pdf, opciones):
        """
        Escribe el archivo PDF con los datos recibidos.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
        global titulo
        titulo = titulo_pdf
        global detalle
        detalle = detalle_pdf
        # Configura el PDF:
        self.alias_nb_pages()
        self.set_title("Listado Cheques Emitidos")
        self.set_left_margin(20)
        self.set_auto_page_break(True , 10.0)
        self.add_page('L')
        self.set_font('Arial', '', 9)
        # Escribe renglones del PDF:
        cont = total_emi = 0
        for dato in datos:

            # Cambia formato a las fechas:
            fecha_emi = date.strftime(dato[2], '%d/%m/%Y')
            fecha_pago = date.strftime(dato[3], '%d/%m/%Y')
            if dato[7] == None:
                fecha_banco = "00/00/0000"
            else:
                fecha_banco = date.strftime(dato[7], '%d/%m/%Y')


            # Suma a totales:
            total_emi += float(dato[4])
            """
            if dato[7] == None:
                fecha_hoy = date.strftime(datetime.now(), '%d/%m/%Y')
                if (fecha_pago > fecha_hoy) == True:
                    total_pago_pend += float(dato[4])
                else:
                    total_pago_cobro += float(dato[4])
            else:
                total_banco += float(dato[4])
            """
            # Cambia a formato de moneda local:
            importe = locale.format("%.2f", (dato[4]), True)

            # Renglón del archivo PDF:
            self.cell(10, 8, str(dato[0]), 0, 0, 'C')
            self.cell(22, 8, str(dato[1]), 0, 0, 'C')
            self.cell(22, 8, str(fecha_emi), 0, 0, 'C')
            self.cell(35, 8, str(importe), 0, 0, 'R')
            self.cell(22, 8, str(fecha_pago), 0, 0, 'C')
            self.cell(70, 8, str(dato[5]), 0, 0, 'L')
            self.cell(25, 8, str(dato[6]), 0, 0, 'L')
            self.cell(22, 8, str(fecha_banco), 0, 0, 'C')
            self.cell(10, 8, '__', 0, 0, 'C')

            self.ln(4)

            cont += 1

        # Totales del archivo PDF:
        cantidad = cont

        total_emi = locale.format("%.2f", (total_emi), True)
        """
        total_pago_pend = locale.format("%.2f", (total_pago_pend), True)
        total_pago_cobro = locale.format("%.2f", (total_pago_cobro), True)
        total_banco = locale.format("%.2f", (total_banco), True)
        """
        # Renglon de total general:
        self.ln(2)
        y = self.get_y()
        self.line(20, y, 285, y)
        self.cell(128, 8, "Son "+str(cantidad)+" cheques emitidos, que suman $ ",
                  0, 0, 'R')
        self.cell(25, 8, str(total_emi), 0, 0, 'R')
        """
        self.cell(25, 8, str(total_no_grav), 0, 0, 'R')
        self.cell(25, 8, str(total_exento), 0, 0, 'R')
        self.cell(25, 8, str(total_iva), 0, 0, 'R')
        self.cell(25, 8, str(total_total), 0, 0, 'R')
        """
        self.ln(4)
        # Descarga el archivo PDF:
        self.output('C:/xampp/htdocs/farma-py/archivos/banco/chequeEmiPDF.pdf', 'F' )
