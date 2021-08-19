#!C:\Users\alvar\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
# 
# pruebaBootstrap.py
#
# Creado: 18/08/2019
# Versión: 001
# Última modificación: 
# 
# Copyright 2019 Alvaro Alejandro Guiffrey <alvaroguiffrey@gmail.com>
# 

html = ("""
<!doctype html>
<html lang="es">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link href="/farma-py/libs/bootstrap-4.3.1/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <!-- Font Awesome Iconos -->
    <link href="/farma-py/libs/fontawesome-5.10.1/css/all.min.css" rel="stylesheet" media="screen">
    
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="/farma_py/libs/bootstrap-4.3.1/js/bootstrap.min.js"></script>
    
    <title>$TITULO</title>
  </head> 
  <body>
    <h1>Hello, world!</h1>
    <div class="d-flex flex-sm-row p-1">
        <button type="button" class="btn btn-info btn-sm" data-toogle="tooltip" title="Cantidad de ...">
        {botonTitulo} <span class="badge badge-light">4</span></button>
        <button type="button" class="btn btn-outline-success btn-sm ml-1" data-toogle="tooltip" title="Agregar">
        <i class="fas fa-plus"></i></button>
    </div>
    
  </body>
</html>
    """
    )

html = html.replace("$TITULO", "Prueba Bootstrap 4.3.1")
html = html.replace("{botonTitulo}", "Cantidad: ")
print(html)
