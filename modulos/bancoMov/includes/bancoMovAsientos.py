# -*- coding: latin-1 -*-
#
# bancoMovAsientos.py
#
# Creado: 15/04/2022
# Versión: 001
# Última modificación:
#
# Copyright 2022 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
#

# Módulos que se importan de la librería estandar
from datetime import date
from decimal import Decimal
import locale


class BancoMovAsientos():
    '''
    Clase para armar un diccionario de asientos contables.

    Permite armar un diccionario de asientos contables con los datos obtenidos
    del modelo.
    '''

    def __init__(self):
        """
        Método que inicializa los atributos de la instancia.
        """
        # Instancia el seteo a local:
        locale.setlocale(locale.LC_ALL, 'es_AR')


    def arma_dicc(self, datos, grupos_dicc, p_ctas_dicc):
        """
        Método que el diccionario con datos de la tabla.

        @param datos:
        @param grupos_dicc:
        @return: asientos_dicc
        """
        # Crea los diccionarios:
        asientos_dicc = {}
        totales = {}
        # Recorre los datos y totaliza por grupo:
        cont = cont_control = cont_deb = cont_cred = 0
        total = total_deb = total_cred = 0
        for dato in datos:
            # Importe:
            importe = dato[3]
            # Suma por orden del grupo
            nombre = grupos_dicc[int(dato[6])][0]
            orden = grupos_dicc[int(dato[6])][1]
            if orden in totales:
                totales[orden][0] += 1
                totales[orden][1] += importe
            else:
                totales[orden] = [1, importe, nombre]

        # Arma los renglones de los asientos contables:
        # 1 - DEPOSITOS

        if "C01" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - DEPOSITOS", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("111002", p_ctas_dicc["111002"],
                                    totales["C01"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111001", p_ctas_dicc["111001"],
                                    0, totales["C01"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                                    "POR "+totales["C01"][0]+" DEPOSITO/S DEL MES.",
                                    0, 0)
        # 2 - ACREDITACIONES Co.Fa.E.R.
        if "C03" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - ACRED. Co.Fa.E.R.", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("111002", p_ctas_dicc["111002"],
                                    totales["C03"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 216003", p_ctas_dicc["216003"],
                                    0, totales["C03"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["C03"][0])+" ACREDITACION/ES "+\
                        " DE Co.Fa.E.R. DEL MES.", 0, 0)
        # 3 - ACREDITACIONES TARJETAS VS
        if "C04" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - ACRED. TARJETAS VS.", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("111002", p_ctas_dicc["111002"],
                                    totales["C04"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 112005", p_ctas_dicc["112005"],
                                    0, totales["C04"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["C04"][0])+" ACREDITACION/ES "+\
                        " DE TARJETAS VS. DEL MES.", 0, 0)
        # 4 - ACREDITACIONES DEBIN
        if "C02" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - ACRED. DEBIN", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("111002", p_ctas_dicc["111002"],
                                    totales["C02"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 112007", p_ctas_dicc["112007"],
                                    0, totales["C02"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["C02"][0])+" ACREDITACION/ES "+\
                        " DE DEBIN DEL MES.", 0, 0)
        # 5 - ACREDITACIONES TRANSFERENCIAS RECIBIDAS
        if "C05" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - TRANSFERENCIAS RECIBIDAS", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("111002", p_ctas_dicc["111002"],
                                    totales["C05"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 112004", p_ctas_dicc["112004"],
                                    0, totales["C05"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["C05"][0])+" TRANSFERENCIA/S "+\
                        " RECIBIDAS DEL MES.", 0, 0)
        # 6 - ACREDITACIONES PLAZOS FIJOS
        if "C06" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - ACRED. PLAZOS FIJOS", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("111002", p_ctas_dicc["111002"],
                                    totales["C06"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111101", p_ctas_dicc["111101"],
                                    0, totales["C06"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["C06"][0])+" ACREDITACION/ES "+\
                        " DE PLAZOS FIJOS DEL MES.", 0, 0)
        # 11 - CHEQUES COBRADOS
        if "D01" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - CH. COBRADOS", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("211006", p_ctas_dicc["211006"],
                                    totales["D01"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111002", p_ctas_dicc["111002"],
                                    0, totales["D01"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["D01"][0])+" CHEQUES "+\
                        " COBRADOS DEL MES.", 0, 0)
        # 12 - DEBITOS TARJETAS VS
        if "D07" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - DEBITOS TARJ. VS.", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("112002", p_ctas_dicc["112002"],
                                    totales["D07"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111002", p_ctas_dicc["111002"],
                                    0, totales["D07"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["D07"][0])+" DEBITOS "+\
                        "DE TARJETAS VS. DEL MES.", 0, 0)
        # 13 - TRANSFERENCIAS REALIZADAS
        if "D05" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - TRANSFERENCIAS REALIZADAS", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("131002", p_ctas_dicc["131002"],
                                    totales["D05"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111002", p_ctas_dicc["111002"],
                                    0, totales["D05"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["D05"][0])+" TRANSFERENCIAS "+\
                        "REALIZADAS DEL MES.", 0, 0)
        # 14 - PAGOS LINK
        if "D06" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - PAGOS LINK", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("131004", p_ctas_dicc["131004"],
                                    totales["D06"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111002", p_ctas_dicc["111002"],
                                    0, totales["D06"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["D06"][0])+" PAGOS LINK "+\
                        "DEL MES.", 0, 0)
        # 15 - DEBITOS AUTOMÁTICOS DE PROVEEDORES
        if "D10" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - DEBITO AUT. DE SERVICIOS", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("211004", p_ctas_dicc["211004"],
                                    totales["D10"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111002", p_ctas_dicc["111002"],
                                    0, totales["D10"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["D10"][0])+" DEBITO AUT. "+\
                        "DE SERVICIOS DEL MES.", 0, 0)
        # 16 - DEBITOS PLAZOS FIJOS
        if "D04" in totales:
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - PLAZOS FIJOS CONSTITUIDOS", 0, 0)
            cont += 1
            asientos_dicc[cont] = ("111101", p_ctas_dicc["111101"],
                                    totales["D04"][1], 0)
            cont += 1
            asientos_dicc[cont] = ("a 111002", p_ctas_dicc["111002"],
                                    0, totales["D04"][1])
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(totales["D04"][0])+" PLAZOS FIJOS "+\
                        "CONSTITUIDOS DEL MES.", 0, 0)
        # 17 - IMPUESTOS VARIOS
        if "I04" or "I05" or "I02" or "I03" in totales:
            total = float(0)
            importe = float(0)
            cantidad = int(0)
            cont += 1
            asientos_dicc[cont] = ("000000", "BANCO - IMPUESTOS VS.", 0, 0)

            if "I04" in totales:
                cont += 1
                asientos_dicc[cont] = ("114101", p_ctas_dicc["114101"],
                                    totales["I04"][1], 0)
                total += float(totales["I04"][1])
                cantidad += int(totales["I04"][0])

            if "I02" or "I03" in totales:
                cont += 1
                if "I02" in totales:
                    #print(str(type(totales["I02"][1])))
                    importe += float(totales["I02"][1])
                    cantidad += int(totales["I02"][0])
                if "I03" in totales:
                    importe += float(totales["I03"][1])
                    cantidad += int(totales["I03"][0])
                asientos_dicc[cont] = ("614003", p_ctas_dicc["614003"],
                                    Decimal(importe), 0)
                total += importe


            if "I05" in totales:
                cont += 1
                asientos_dicc[cont] = ("614102", p_ctas_dicc["614102"],
                                    totales["I05"][1], 0)
                total += float(totales["I05"][1])
                cantidad += int(totales["I05"][0])

            cont += 1
            asientos_dicc[cont] = ("a 111002", p_ctas_dicc["111002"],
                                    0, Decimal(total))
            cont += 1
            asientos_dicc[cont] = ("999999",
                        "POR "+str(cantidad)+" DEBITOS DE "+\
                        "IMPUESTOS VS. DEL MES.", 0, 0)
        
        # Retorna el resultado del armado de los asientos contables:
        return asientos_dicc
