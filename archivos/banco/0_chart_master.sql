-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 13-04-2022 a las 09:59:36
-- Versión del servidor: 5.7.31-log
-- Versión de PHP: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `c2010188_front`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `0_chart_master`
--

CREATE TABLE `0_chart_master` (
  `account_code` varchar(15) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `account_code2` varchar(15) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `account_name` varchar(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `account_type` varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  `inactive` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `0_chart_master`
--

INSERT INTO `0_chart_master` (`account_code`, `account_code2`, `account_name`, `account_type`, `inactive`) VALUES
('111001', '', 'Caja', '111', 0),
('111002', '', 'Nuevo BERSA -CC. 661336/9 ', '111', 0),
('111101', '', 'Nuevo BERSA - Depósitos Plazo Fijo', '111', 0),
('112001', '', 'Ctas.Ctes. de Clientes Vs.', '112', 0),
('112002', '', 'Tarjetas de Deb.y Cred. ', '112', 0),
('112003', '', 'Cheques Recibidos de Vs.', '112', 0),
('112004', '', 'Transf. Rec. de Vs. sin Imputar', '112', 0),
('112005', '', 'Tarj. Liquidadas Pendientes de Acred.', '112', 0),
('112006', '', 'Código QR BERSA', '112', 0),
('113001', '', 'Obras Sociales - Ordenes sin Presentar', '113', 0),
('113002', '', 'Obras Sociales - Ordenes al Cobro', '113', 0),
('113003', '', 'Obras Sociales - Honorarios PAMI al Cobro', '113', 0),
('113004', '', 'Obras Sociales - Honorarios IOSPER al Cobro', '113', 0),
('113101', '', 'PAMI - Comp. Costo Drog. (CCD)', '113', 0),
('113201', '', 'Laboratorios Vs. p/ant. COFA-PAMI', '113', 0),
('113501', '', 'Drog. prov/Ob.Soc. - Honorarios sin Presentar', '113', 0),
('113502', '', 'Drog. prov/Ob.Soc. - Honorarios al Cobro', '113', 0),
('114001', '', 'IVA - Credito Fiscal (Mercaderias)', '114', 0),
('114002', '', 'IVA - Saldo a Favor', '114', 0),
('114003', '', 'IVA - Retenciones', '114', 0),
('114004', '', 'IVA - Percepciones Compras', '114', 0),
('114005', '', 'IVA - Credito Fiscal (Gastos y Comisiones c/21%)', '114', 0),
('114006', '', 'IVA - Credito Fiscal (Gastos c/27%)', '114', 0),
('114007', '', 'IVA - Credito Fiscal (Comisiones c/10,5%)', '114', 0),
('114008', '', 'IVA - Credito Fiscal (Bs. de Uso c/10,5%)', '114', 0),
('114009', '', 'IVA - Crédito Fiscal (Bs. de Uso c/21%)', '114', 0),
('114011', '', 'Imp. a las Ganancias - Anticipos', '114', 0),
('114012', '', 'Imp. a las Ganancias - Retenciones', '114', 0),
('114021', '', 'Imp. Ley 25413 - Computable ', '114', 0),
('114031', '', 'Imp. a las Participaciones Societarias', '114', 0),
('114101', '', 'Ingresos Brutos - Retenciones', '114', 0),
('114102', '', 'Ingresos Brutos - Percepciones', '114', 0),
('115001', '', 'Mercadería -IVA Exento- Medicamentos', '115', 0),
('115002', '', 'Mercadería -IVA 21%- Perf.,Acc.y Otros', '115', 0),
('115003', '', 'Mercadería -IVA 10,5%-', '115', 0),
('115004', '', 'Mercadería - Monotributo', '115', 0),
('116001', '', 'Socio Bochaton Maria Delfa', '116', 0),
('116002', '', 'Socio Guiffrey Alvaro Alejandro', '116', 0),
('116003', '', 'Socio Barrera Silvia Ines', '116', 0),
('121001', '', 'Muebles y Utiles', '121', 0),
('121002', '', 'Amort. Acum. Muebles y Utiles', '121', 0),
('121011', '', 'Máquinas y Equipos', '121', 0),
('121012', '', 'Amort. Acum. Máquinas y Equipos', '121', 0),
('121021', '', 'Instalaciones', '121', 0),
('121022', '', 'Amort. Acum. Instalaciones', '121', 0),
('121031', '', 'Edificio', '121', 0),
('121032', '', 'Amort. Acum. Edificio', '121', 0),
('121041', '', 'Rodados', '121', 0),
('121042', '', 'Amortización Acum. Rodados', '121', 0),
('122001', '', 'Gastos de Constitucion', '122', 0),
('122002', '', 'Amort. Acumul. Gastos de Const.', '122', 0),
('131001', '', 'Partidas en Suspenso', '131', 0),
('131002', '', 'Transferencias en Suspenso', '131', 0),
('131003', '', 'Ctas.Ctes. - Correcciones en Suspenso ', '131', 0),
('131004', '', 'Pagos Link en Suspenso', '131', 0),
('211001', '', 'Coop. Farm. del Litoral', '211', 0),
('211002', '', 'Drog. Kellerhoff SA', '211', 0),
('211003', '', 'Drog. del Sud SA', '211', 0),
('211004', '', 'Proveedores Varios', '211', 0),
('211005', '', 'Sucesion de Guiffrey Carlos M.', '211', 0),
('211006', '', 'Cheques Diferidos Emitidos', '211', 0),
('211007', '', 'Anticipos de Ob.Soc. a Prov.(Drog.del Sud SA)', '211', 0),
('211008', '', 'Anticipo de Clientes Vs. p/CC', '211', 0),
('211009', '', 'Anticipos COFA a Drog. del Sud (Efectivo)', '211', 0),
('211010', '', 'Anticipos COFA a Lab.Vs. p/PAMI', '211', 0),
('212001', '', 'Sueldos a Pagar', '212', 0),
('212002', '', 'Borrar cuenta', '212', 0),
('212003', '', 'Retenciones Sueldos a Depositar', '212', 0),
('212006', '', 'Leyes Sociales a Pagar', '212', 0),
('212101', '', 'Borrar cuenta', '212', 0),
('213001', '', 'AFIP - IVA a Pagar', '213', 0),
('213002', '', 'AFIP - Imp. a las Ganancias a Pagar', '213', 0),
('213003', '', 'AFIP - Imp. a las Part.Soc. a Pagar', '213', 0),
('213004', '', 'AFIP - Anticipo Imp. a las Ganancias a Pagar', '213', 0),
('213101', '', 'ATER - Ing. Brutos a Pagar', '213', 0),
('213201', '', 'MVE - TISHPyS a Pagar', '213', 0),
('214001', '', 'Prestamos y Acuerdos Bancarios', '214', 0),
('214002', '', 'Prestamos Socios', '214', 0),
('214003', '', 'Prestamo Circ.Farm. de Colon', '214', 0),
('215001', '', 'Socio Bochaton Maria Delfa', '215', 0),
('215002', '', 'Socio Guiffrey Alvaro Alejandro', '215', 0),
('215003', '', 'Socio Barrera Silvia Ines', '215', 0),
('216001', '', 'IVA - Débito Fiscal', '216', 0),
('216002', '', 'Seguros a Pagar', '216', 0),
('216003', '', 'Co.Fa.E.R. - Acred. en CC. BERSA', '216', 0),
('216004', '', 'Co.Fa.E.R. - Antic. PAMI-COFA', '216', 0),
('217001', '', 'Partidas en Suspenso', '217', 0),
('311001', '', 'Capital Social', '311', 0),
('311002', '', 'Ajuste al Capital', '311', 0),
('311003', '', 'Patrimonio Neto', '311', 0),
('320001', '', 'Reserva Legal', '320', 0),
('330001', '', 'Resultado del Ejercicio', '330', 0),
('330002', '', 'Resultados no Asignados', '330', 0),
('330003', '', 'Resultado Acumulado Ejercicios Ant.', '330', 0),
('410001', '', 'Ventas Mercaderías -IVA Exento-', '410', 0),
('410002', '', 'Ventas Mercaderías -IVA 21%-', '410', 0),
('420001', '', 'Honorarios p/Serv.a O.Soc. y Drog.', '420', 0),
('420002', '', 'Descuentos y Bonific. Obtenidas', '420', 0),
('420003', '', 'Intereses Ganados', '420', 0),
('420004', '', 'Reintegros y Gastos Recuperados', '420', 0),
('420005', '', 'Otros Ingresos', '420', 0),
('420006', '', 'Diferencias p/Redondeo y Otros', '420', 0),
('420007', '', 'Recupero Incobrables Ctas.Ctes.', '420', 0),
('510001', '', 'Costo Mercadería -IVA Exento-', '510', 0),
('510002', '', 'Costo Mercadería -IVA 21%-', '510', 0),
('611001', '', 'Sueldos', '611', 0),
('611002', '', 'Contribuciones por Leyes Sociales', '611', 0),
('611003', '', 'Asignaciones no Remunerativas', '611', 0),
('612001', '', 'Descuentos a Clientes', '612', 0),
('612002', '', 'Descuentos a O.Sociales', '612', 0),
('613001', '', 'Viáticos por Compras', '613', 0),
('613002', '', 'Flete de Mercaderías y Acarreos', '613', 0),
('614001', '', 'AFIP - Imp. a las Ganancias', '614', 0),
('614002', '', 'AFIP - Imp. a las Part.Soc. ', '614', 0),
('614003', '', 'AFIP - Impuesto Debitos y Creditos Ley 25413', '614', 0),
('614051', '', 'AFIP - Impuestos Internos', '614', 0),
('614101', '', 'ATER - Impuesto a los Ingresos Brutos', '614', 0),
('614102', '', 'ATER - Impuesto de Sellos ', '614', 0),
('614103', '', 'Impuestos y Tasas Vs.', '614', 0),
('614201', '', 'MVE - TISHPyS', '614', 0),
('615001', '', 'Retencion Colegio Farm.de Entre Rios', '615', 0),
('615002', '', 'Retencion Circ.Farm. de Colon', '615', 0),
('615003', '', 'Gastos Varios Colegio Farmac.', '615', 0),
('615004', '', 'Comisiones Varias', '615', 0),
('615005', '', 'Débitos y Ajustes Ob. Sociales', '615', 0),
('615006', '', 'Acred. de O.S. a Laboratorios sin Utilizar', '615', 0),
('615007', '', 'Ctas. Ctes. de Clientes - Incobrables', '615', 0),
('615008', '', 'Tarjetas Deb. y Cred. Rechazadas', '615', 0),
('615101', '', 'Gastos Varios Com.', '615', 0),
('615102', '', 'Gastos Varios Com. (Monotributistas)', '615', 0),
('615103', '', 'Gastos Varios Com. Med. Vencidos', '615', 0),
('620001', '', 'Honorarios ', '620', 0),
('620002', '', 'Amortizaciones', '620', 0),
('620003', '', 'Energia Electrica y Teléfono', '620', 0),
('620004', '', 'Gastos Varios Adm.', '620', 0),
('620005', '', 'Gastos Varios Adm. (Monotributistas)', '620', 0),
('620006', '', 'Gastos Varios Adm. (Sin Facturas)', '620', 0),
('630001', '', 'Intereses, Comisiones y Gastos Financieros', '630', 0),
('630002', '', 'Intereses y Recargos Fiscales', '630', 0),
('630003', '', 'Intereses Varios', '630', 0),
('630004', '', 'RECPAM', '630', 0),
('640002', '', 'Diferencias p/Redondeo y Otros', '640', 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `0_chart_master`
--
ALTER TABLE `0_chart_master`
  ADD PRIMARY KEY (`account_code`),
  ADD KEY `account_name` (`account_name`),
  ADD KEY `accounts_by_type` (`account_type`,`account_code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
