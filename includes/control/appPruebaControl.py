'''
Created on 10 oct. 2019

@author: alvar
'''
from includes.vista.appPruebaVista import AppPruebaVista


class AppPruebaControl(object):
    '''
    classdocs
    '''

    
    def muestro(self):
        print("""
            <TITLE>Python</TITLE>
            """)
        print("#SI SE PUEDE.<br>")
        AppPruebaVista.saludo(self)