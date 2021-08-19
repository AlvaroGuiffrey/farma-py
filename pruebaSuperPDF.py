#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaSuperPDF.py
#
# Creado: 12/09/2019
# Versión: 001
# Ultima modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

# Modulos que se importan de la librería estandar

from fpdf import FPDF
from datetime import datetime

print("Content-Type: text/html")
print("""
    <TITLE>Prueba PDF</TITLE>
    """)

class PDF(FPDF):
            
    def header(self):
        
        ahora = datetime.now()
        fecha = datetime.strftime(ahora, '%d/%m/%Y %H:%M')
        self.set_font('Arial', '', 9)
        self.cell(30, 10, "Farmacia Villa Elisa SRL", 0, 0, 'L')
        self.cell(230, 10, "Fecha: "+fecha+"", 0, 0, 'R')
        self.ln(3)
        self.set_font('Arial', 'BU', 12)
        self.cell(0, 10, "Listado de Comprobantes Recibidos AFIP", 0, 0, 'C')
        self.ln(5)
        self.set_font('Arial', 'I', 9)
        self.cell(0, 10, detalle_pdf, 0, 0, 'L')
        self.ln(5)
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
        self.set_y(-15)
        self.set_font('Arial', 'I', 6)
        self.cell(0, 10, 'Pagina '+str(self.page_no())+'/{nb}', 0, 0, 'C')
        

class SPDF(PDF):
    
    
    def escribe_pdf(self):
        
        print(detalle_pdf, "<br>")
        self.alias_nb_pages()
        self.set_title("Listado Compr. Rec. AFIP") 
        self.set_left_margin(20)
        self.set_auto_page_break(True , 10.0)
        self.add_page('L')
        pdf.set_font('Arial', 'BI', 9)
        pdf.cell(0, 10, detalle_pdf, 0, 0, 'L')
        pdf.ln(5)
        self.set_font('Arial', '', 9)
        for i in range(1, 51):
            self.cell(6, 8, str(i), 0, 0, 'C')
            self.cell(22, 8, '11/09/2019', 0, 0, 'C')
            self.cell(36, 8, 'FC A-0180-00128946', 0, 0, 'C')
            self.cell(70, 8, 'DROGUERIA DEL SUD SOCIEDAD ANONIMA', 0, 0)
            self.cell(25, 8, '10.560,20', 0, 0, 'R')
            self.cell(25, 8, '450,00', 0, 0, 'R')
            self.cell(25, 8, '120.456,55', 0, 0, 'R')
            self.cell(25, 8, '2.217,85', 0, 0, 'R')
            self.cell(25, 8, '133.684,60', 0, 0, 'R')
            self.cell(6, 8, '__', 0, 0, 'C')
            self.ln(4)
            
        self.output('C:/xampp/htdocs/farma-py/archivos/recibidosAFIP.pdf', 'F' )
        
        
        
global detalle_pdf
detalle_pdf = (
    "Desde: 2019-08-01 - Hasta: 2019-08-30 - de: COOPERATIVA FARMACEUTICA"
    " LITORAL "
    )
print("Hola loco<br>")
pdf = SPDF()
pdf.escribe_pdf()
enlace = (
    "<a href='/farma-py/archivos/recibidosAFIP.pdf'>Abrir PDF</a><br>"
    )
print(enlace)

