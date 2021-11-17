# -*- coding: utf-8 -*-
#
# tarjResPDF.py
#
# Creado: 12/11/2021
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
        self.cell(0, 10, "Resumen Impositivo - Tarjetas", 0, 0, 'C')
        self.ln(5)
        self.set_font('Arial', 'I', 9)
        self.cell(0, 10, detalle, 0, 0, 'L')
        self.ln(5)
        # Encabezado de los renglones del archivo PDF:
        self.line(20, 25, 285, 25)
        self.set_font('Arial', 'B', 10)
        self.cell(30, 9, "# Concepto", 0, 0, 'L')
        self.ln(5)
        self.set_font('Arial', '', 9)
        self.cell(30, 9, '--- DETALLE ----', 0, 0, 'C')
        self.cell(25, 9, '--- IMPORTE ----', 0, 0, 'C')
        self.cell(30, 9, '--- DETALLE ----', 0, 0, 'C')
        self.cell(25, 9, '--- IMPORTE ----', 0, 0, 'C')
        self.cell(30, 9, '--- DETALLE ----', 0, 0, 'C')
        self.cell(25, 9, '--- IMPORTE ----', 0, 0, 'C')
        self.ln(7)
        y = self.get_y()
        self.line(20, y, 285, y)

    def footer(self):
        """
        Reescribe el método footer() de la clase FPDF
        """
        # Pie de página del archivo PDF:
        self.set_y(-15)
        self.set_font('Arial', 'I', 6)
        self.cell(0, 10, 'Pagina '+str(self.page_no())+'/{nb}', 0, 0, 'C')



class TarjResPDF(PDF):
    """
    Clase que escribe un archivo PDF con datos para descargar.

    Escribe un archivo PDF con datos del listado que se graba en el
    directorio: 'archivos/tarjetas' de la aplicación. También se puede
    abrir desde el navegador.
    """


    def escribir_pdf(self, datos, detalle_pdf):
        """
        Escribe el archivo PDF con los datos recibidos.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
        global detalle
        detalle = detalle_pdf
        # Configura el PDF:
        self.alias_nb_pages()
        self.set_title("Resumen Impositivo")
        self.set_left_margin(20)
        self.set_auto_page_break(True , 10.0)
        self.add_page('L')
        self.set_font('Arial', '', 9)
        # Escribe renglones del PDF:
        cont = 0
        # Importes del Resumen Impositivo
        # Renglón 1 del PDF
        self.ln(2)
        self.set_font('Arial', 'B', 10)
        self.cell(40, 8, str('# Importes liquidados:'), 0, 0, 'L')
        self.ln(4)
        # Renglón 2 del PDF
        self.set_font('Arial', '', 9)
        self.cell(30, 8, "Bruto ..................", 0, 0)
        self.cell(25, 8, "$ "+str(datos['importe_bruto']), 0, 0, 'R')
        self.cell(30, 8, " - Descuentos ..........", 0, 0)
        self.cell(25, 8, "$ "+str(datos['importe_desc']), 0, 0, 'R')
        self.cell(30, 8, " - Neto ................", 0, 0)
        self.cell(25, 8, "$ "+str(datos['importe_neto']), 0, 0, 'R')
        self.ln(6)
        # Separador
        self.set_font('Arial', '', 9)
        self.ln(2)
        y = self.get_y()
        self.line(20, y, 285, y)
        # Renglón 3 del PDF
        self.set_font('Arial', 'B', 10)
        self.cell(40, 8, str('# Cargos p/:'), 0, 0, 'L')
        self.ln(4)
        # Renglón 4 del PDF
        self.set_font('Arial', '', 9)
        self.cell(30, 8, "Arancel ................", 0, 0)
        self.cell(25, 8, "$ "+str(datos['arancel']), 0, 0, 'R')
        self.cell(30, 8, " - Costo Financ. .......", 0, 0)
        self.cell(25, 8, "$ "+str(datos['costo_financiero']), 0, 0, 'R')
        self.cell(30, 8, " - Otros Deb. ..........", 0, 0)
        self.cell(25, 8, "$ "+str(datos['otros_debitos']), 0, 0, 'R')
        self.ln(6)
        # Renglón 5 del PDF
        self.set_font('Arial', 'B', 10)
        self.cell(40, 8, str('# Iva s/cargos:'), 0, 0, 'L')
        self.ln(4)
        # Renglón 6 del PDF
        self.set_font('Arial', '', 9)
        self.cell(30, 8, "Arancel ................", 0, 0)
        self.cell(25, 8, "$ "+str(datos['iva_arancel']), 0, 0, 'R')
        self.cell(30, 8, " - Costo Financ. .......", 0, 0)
        self.cell(25, 8, "$ "+str(datos['iva_costo_financiero']), 0, 0, 'R')
        self.cell(30, 8, " - Otros Deb. ..........", 0, 0)
        self.cell(25, 8, "$ "+str(datos['iva_otros_debitos']), 0, 0, 'R')
        self.ln(6)
        # Renglón 7 del PDF
        self.set_font('Arial', 'B', 10)
        self.cell(40, 8, str('# Impuestos a/:'), 0, 0, 'L')
        self.ln(4)
        # Renglón 8 del PDF
        self.set_font('Arial', '', 9)
        self.cell(30, 8, "Deb/Cred. ..............", 0, 0)
        self.cell(25, 8, "$ "+str(datos['impuesto_debcred']), 0, 0, 'R')
        self.cell(30, 8, " - Intereses ...........", 0, 0)
        self.cell(25, 8, "$ "+str(datos['impuesto_interes']), 0, 0, 'R')
        self.ln(6)
        # Renglón 9 del PDF
        self.set_font('Arial', 'B', 10)
        self.cell(40, 8, str('# Retenciones p/:'), 0, 0, 'L')
        self.ln(4)
        # Renglón 10 del PDF
        self.set_font('Arial', '', 9)
        self.cell(30, 8, "IVA ....................", 0, 0)
        self.cell(25, 8, "$ "+str(datos['retencion_iva']), 0, 0, 'R')
        self.cell(30, 8, " - Imp. a las Gan. .....", 0, 0)
        self.cell(25, 8, "$ "+str(datos['retencion_imp_gan']), 0, 0, 'R')
        self.cell(30, 8, " - Imp. Ingr. Brutos ...", 0, 0)
        self.cell(25, 8, "$ "+str(datos['retencion_ing_brutos']), 0, 0, 'R')
        self.ln(6)
        # Renglón 11 del PDF
        self.set_font('Arial', 'B', 10)
        self.cell(40, 8, str('# Percepciones p/:'), 0, 0, 'L')
        self.ln(4)
        # Renglón 12 del PDF
        self.set_font('Arial', '', 9)
        self.cell(30, 8, "IVA ....................", 0, 0)
        self.cell(25, 8, "$ "+str(datos['percepcion_iva']), 0, 0, 'R')
        self.cell(30, 8, " - Imp. Ingr. Brutos ...", 0, 0)
        self.cell(25, 8, "$ "+str(datos['percepcion_ing_brutos']), 0, 0, 'R')
        self.ln(6)
        # Renglon de total general:
        self.ln(2)
        y = self.get_y()
        self.line(20, y, 285, y)
        self.cell(134, 8, "Son: "+str(datos['cant_liq'])+" liquidaciones.",
                  0, 0)
        self.ln(4)
        # Descarga el archivo PDF:
        self.output('C:/xampp/htdocs/farma-py/archivos/tarjetas/tarjResImp.pdf', 'F' )
