/**
 * JavaScript - Funciones varias de la pagina.html
 */

/**
 *  ----- del Menú ----
*/
function openNav() {
  document.getElementById("mySidenav").style.width = "250px"; /* Ancho del menú */
}

function closeNav() {
  document.getElementById("mySidenav").style.width = '0';
}

/**
 *  ---- de los Tooltip ----
 */
$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip({trigger: "hover"});
});

/**
 * ---- del daterangepicker ----
 */

/**
 * ---- sessionStorage ----
 */
