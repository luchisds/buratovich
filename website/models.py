# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# User related info
class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	algoritmo_code = models.IntegerField(unique=True, verbose_name='Cuenta Algoritmo')
	company_name = models.CharField(max_length=150, verbose_name='Razón Social')
	account_confirmed = models.BooleanField(default=False)
	random_password = models.BooleanField(default=True)


class Analysis(models.Model):
	entry_point = models.IntegerField(verbose_name='Punto de Ingreso')
	analysis_number = models.IntegerField(verbose_name='Numero de Analisis')
	analysis = models.CharField(max_length=13, verbose_name='Analisis')
	date = models.DateField(verbose_name='Fecha de Analisis')
	newsletter_number = models.CharField(max_length=20, verbose_name='Numero de Boletin')
	field = models.IntegerField(verbose_name='Campo')
	lot = models.CharField(max_length=10, verbose_name='Lote')
	field_description = models.CharField(max_length=100, verbose_name='Nombre de Campo')
	species = models.CharField(max_length=4, verbose_name='Especie')
	harvest = models.CharField(max_length=4, verbose_name='Cosecha')
	protein = models.FloatField(verbose_name='Contenido Proteico')
	grade = models.IntegerField(verbose_name='Grado')
	factor = models.FloatField(verbose_name='Factor')
	analysis_costs = models.FloatField(verbose_name='Gastos de Analisis')
	gluten = models.IntegerField(verbose_name='Gluten')
	analysis_item = models.IntegerField(verbose_name='Rubro de Analisis')
	percentage = models.FloatField(verbose_name='Porcentaje')
	bonus = models.FloatField(verbose_name='Bonificacion')
	reduction = models.FloatField(verbose_name='Rebaja')
	item_descripcion = models.CharField(max_length=100, verbose_name='Descripcion')

	class Meta:
		verbose_name = 'Analisis'


class Remittances(models.Model):
	entry_point = models.IntegerField(verbose_name='Punto de Ingreso')
	analysis_number = models.IntegerField(verbose_name='Numero de Analisis')
	analysis = models.CharField(max_length=13, verbose_name='Analisis')
	date = models.DateField(verbose_name='Fecha de Analisis')
	entry_point_ticket = models.IntegerField(verbose_name='Punto de Ingreso Ticket')
	ticket_number = models.IntegerField(verbose_name='Numero de Ticket')
	certified = models.BooleanField(verbose_name='Certificado', default=True)
	ticket = models.CharField(max_length=16, verbose_name='Ticket')
	ticket_date = models.DateField(verbose_name='Fecha de Ticket')
	net_kg = models.IntegerField(verbose_name='Kilos Netos')

	class Meta:
		verbose_name = 'Remesa'
		verbose_name_plural = 'Remesas'


class Deliveries(models.Model):
	algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
	name = models.CharField(max_length=150, verbose_name='Razón Social')
	indicator = models.CharField(max_length=1, verbose_name='Indicador')
	species = models.CharField(max_length=4, verbose_name='Especie')
	harvest = models.CharField(max_length=4, verbose_name='Cosecha')
	speciesharvest = models.CharField(max_length=8, verbose_name='Especie Cosecha', null=True)
	species_description = models.CharField(max_length=50, verbose_name='Especie y Cosecha')
	field = models.IntegerField(verbose_name='Codigo de Campo')
	field_description = models.CharField(max_length=100, verbose_name='Nombre de Campo')
	date = models.DateField(null=True, verbose_name='Fecha')
	voucher = models.CharField(max_length=16, verbose_name='Comprobante')
	gross_kg = models.IntegerField(verbose_name='Peso Bruto')
	humidity_percentage = models.FloatField(verbose_name='Humedad (%)')
	humidity_reduction = models.FloatField(verbose_name='Merma de Humedad')
	humidity_kg = models.IntegerField(verbose_name='Kilos de Humedad')
	shaking_reduction = models.FloatField(verbose_name='Merma de Zarandeo')
	shaking_kg = models.IntegerField(verbose_name='Kilos de Zarandeo')
	volatile_reduction = models.FloatField(verbose_name='Merma Volatil')
	volatile_kg = models.IntegerField(verbose_name='Kilos Volatil')
	price_per_yard = models.FloatField(verbose_name='Precio por Quintal')
	driver_code = models.IntegerField(verbose_name='Chofer')
	driver_name = models.CharField(max_length=150, verbose_name='Nombre del Chofer')
	factor = models.FloatField(verbose_name='Factor')
	grade = models.IntegerField(verbose_name='Grado')
	gluten = models.IntegerField(verbose_name='Gluten')
	number_1116A = models.IntegerField(verbose_name='Numero 1116A')
	km = models.IntegerField(verbose_name='Kilometros')
	charge_carry = models.CharField(max_length=2, verbose_name='Cobra Acarreo')
	external_voucher_code = models.CharField(max_length=2, verbose_name='Codigo de Comprobante Externo')
	external_voucher_branch = models.IntegerField(verbose_name='Sucursal Comprobante Externo')
	external_voucher_number = models.IntegerField(verbose_name='Numero Comprobante Externo')
	aeration_reduction = models.FloatField(verbose_name='Merma de Aireacion')
	aeration_kg = models.IntegerField(verbose_name='Kilos de Aireacion')
	quality_reduction = models.FloatField(verbose_name='Merma de Calidad')
	quality_kg = models.IntegerField(verbose_name='Kilos de Calidad')
	zone = models.CharField(max_length=2, verbose_name='Zona')
	zone_description = models.CharField(max_length=80, verbose_name='Descripcion de Zona')
	plant_code = models.IntegerField(verbose_name='Planta')
	service_billing_code = models.CharField(max_length=2, verbose_name='Codigo Factura de Servicios')
	service_billing_branch = models.IntegerField(verbose_name='Sucursal Factura de Servicios')
	service_billing_number = models.IntegerField(verbose_name='Numero Factura de Servicios')
	service_billing_date = models.DateField(null=True, verbose_name='Fecha Factura de Servicios')
	service_billing = models.CharField(max_length=50, verbose_name='Factura de Servicios')
	carrier_code = models.IntegerField(verbose_name='Empresa de Transporte')
	carrier_name = models.CharField(max_length=150, verbose_name='Nombre de Empresa de Transporte')
	exclude_charge_expenses = models.CharField(max_length=2, verbose_name='Excluye Cobro de Gastos')
	to_date = models.DateField(null=True, verbose_name='Fecha Entrega Hasta')
	observations = models.CharField(max_length=300, verbose_name='Observaciones')
	follow_destination = models.CharField(max_length=2, verbose_name='Sigue a Destino')
	destination_code = models.CharField(max_length=5, verbose_name='Codigo de Destino')
	net_weight = models.IntegerField(verbose_name='Peso Neto')
	tare = models.IntegerField(verbose_name='Tara')
	gross_weight_recognized = models.IntegerField(verbose_name='Peso Bruto Reconocido')
	plant_description = models.CharField(max_length=80, verbose_name='Descripcion de Planta')
	gross_kg_var = models.IntegerField(verbose_name='Kilos Brutos (otro)')
	gross_kg_2 = models.IntegerField(verbose_name='Kilos Brutos 2')
	blank_1 = models.CharField(max_length=1, verbose_name='Blanco 1')
	blank_2 = models.CharField(max_length=1, verbose_name='Blanco 1')
	blank_3 = models.CharField(max_length=1, verbose_name='Blanco 1')
	blank_4 = models.CharField(max_length=1, verbose_name='Blanco 4')
	allotment = models.CharField(max_length=10, verbose_name='Lote')
	allotment_description = models.CharField(max_length=100, verbose_name='Descripcion Lote')
	blank_5 = models.IntegerField(verbose_name='Blanco 5')
	blank_6 = models.CharField(max_length=2, verbose_name='Blanco 6')
	kg_cnv = models.IntegerField(verbose_name='Kilos Conf. de Venta')
	kg_cnv_2 = models.IntegerField(verbose_name='Kilos Conf. de Venta 2')
	kg_cnv_3 = models.IntegerField(verbose_name='Kilos Conf. de Venta 3')
	blank_7 = models.CharField(max_length=2, verbose_name='Blanco 7')
	blank_8 = models.CharField(max_length=2, verbose_name='Blanco 8')
	blank_9 = models.CharField(max_length=2, verbose_name='Blanco 9')
	blank_10 = models.CharField(max_length=2, verbose_name='Blanco 10')
	gross_kg_3 = models.IntegerField(verbose_name='Kilos Brutos 3')
	unknown_1 = models.IntegerField(verbose_name='Desconocido 1')
	unknown_2 = models.IntegerField(verbose_name='Desconocido 2')
	gross_kg_4 = models.IntegerField(verbose_name='Kilos Brutos 4')
	rate = models.FloatField(verbose_name='Tarifa')
	net_weight_2 = models.IntegerField(verbose_name='Peso Neto 2')
	humidity_kg_2 = models.IntegerField(verbose_name='Kilos de Humedad 2')
	blank_11 = models.CharField(max_length=1, verbose_name='Blanco 11')
	blank_12 = models.CharField(max_length=1, verbose_name='Blanco 12')
	blank_13 = models.CharField(max_length=1, verbose_name='Blanco 13')
	blank_14 = models.CharField(max_length=2, verbose_name='Blanco 14')
	ctg = models.IntegerField(verbose_name='CTG')

	class Meta:
		verbose_name = 'Entregas'


class Sales(models.Model):
	algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
	name = models.CharField(max_length=150, verbose_name='Razón Social')
	indicator = models.CharField(max_length=1, verbose_name='Indicador')
	species = models.CharField(max_length=4, verbose_name='Especie')
	harvest = models.CharField(max_length=4, verbose_name='Cosecha')
	speciesharvest = models.CharField(max_length=8, verbose_name='Especie Cosecha', null=True)
	species_description = models.CharField(max_length=50, verbose_name='Especie y Cosecha')
	field = models.IntegerField(verbose_name='Codigo de Campo')
	field_description = models.CharField(max_length=100, verbose_name='Nombre de Campo')
	date = models.DateField(null=True, verbose_name='Fecha')
	voucher = models.CharField(max_length=16, verbose_name='Comprobante')
	gross_kg = models.IntegerField(verbose_name='Peso Bruto')
	humidity_percentage = models.FloatField(verbose_name='Humedad (%)')
	humidity_reduction = models.FloatField(verbose_name='Merma de Humedad')
	humidity_kg = models.IntegerField(verbose_name='Kilos de Humedad')
	shaking_reduction = models.FloatField(verbose_name='Merma de Zarandeo')
	shaking_kg = models.IntegerField(verbose_name='Kilos de Zarandeo')
	volatile_reduction = models.FloatField(verbose_name='Merma Volatil')
	volatile_kg = models.IntegerField(verbose_name='Kilos Volatil')
	price_per_yard = models.FloatField(verbose_name='Precio por Quintal')
	driver_code = models.IntegerField(verbose_name='Chofer')
	driver_name = models.CharField(max_length=150, verbose_name='Nombre del Chofer')
	factor = models.FloatField(verbose_name='Factor')
	grade = models.IntegerField(verbose_name='Grado')
	gluten = models.IntegerField(verbose_name='Gluten')
	number_1116A = models.IntegerField(verbose_name='Numero 1116A')
	km = models.IntegerField(verbose_name='Kilometros')
	charge_carry = models.CharField(max_length=2, verbose_name='Cobra Acarreo')
	external_voucher_code = models.CharField(max_length=2, verbose_name='Codigo de Comprobante Externo')
	external_voucher_branch = models.IntegerField(verbose_name='Sucursal Comprobante Externo')
	external_voucher_number = models.IntegerField(verbose_name='Numero Comprobante Externo')
	aeration_reduction = models.FloatField(verbose_name='Merma de Aireacion')
	aeration_kg = models.IntegerField(verbose_name='Kilos de Aireacion')
	quality_reduction = models.FloatField(verbose_name='Merma de Calidad')
	quality_kg = models.IntegerField(verbose_name='Kilos de Calidad')
	zone = models.CharField(max_length=2, verbose_name='Zona')
	zone_description = models.CharField(max_length=80, verbose_name='Descripcion de Zona')
	plant_code = models.IntegerField(verbose_name='Planta')
	service_billing_code = models.CharField(max_length=2, verbose_name='Codigo Factura de Servicios')
	service_billing_branch = models.IntegerField(verbose_name='Sucursal Factura de Servicios')
	service_billing_number = models.IntegerField(verbose_name='Numero Factura de Servicios')
	service_billing_date = models.DateField(null=True, verbose_name='Fecha Factura de Servicios')
	service_billing = models.CharField(max_length=50, verbose_name='Factura de Servicios')
	carrier_code = models.IntegerField(verbose_name='Empresa de Transporte')
	carrier_name = models.CharField(max_length=150, verbose_name='Nombre de Empresa de Transporte')
	exclude_charge_expenses = models.CharField(max_length=2, verbose_name='Excluye Cobro de Gastos')
	to_date = models.DateField(null=True, verbose_name='Fecha Entrega Hasta')
	observations = models.CharField(max_length=300, verbose_name='Observaciones')
	follow_destination = models.CharField(max_length=2, verbose_name='Sigue a Destino')
	destination_code = models.CharField(max_length=5, verbose_name='Codigo de Destino')
	net_weight = models.IntegerField(verbose_name='Peso Neto')
	tare = models.IntegerField(verbose_name='Tara')
	gross_weight_recognized = models.IntegerField(verbose_name='Peso Bruto Reconocido')
	plant_description = models.CharField(max_length=80, verbose_name='Descripcion de Planta')
	gross_kg_var = models.IntegerField(verbose_name='Kilos Brutos (otro)')
	gross_kg_2 = models.IntegerField(verbose_name='Kilos Brutos 2')
	blank_1 = models.CharField(max_length=1, verbose_name='Blanco 1')
	blank_2 = models.CharField(max_length=1, verbose_name='Blanco 1')
	blank_3 = models.CharField(max_length=1, verbose_name='Blanco 1')
	blank_4 = models.CharField(max_length=1, verbose_name='Blanco 4')
	allotment = models.CharField(max_length=10, verbose_name='Lote')
	allotment_description = models.CharField(max_length=100, verbose_name='Descripcion Lote')
	blank_5 = models.IntegerField(verbose_name='Blanco 5')
	blank_6 = models.CharField(max_length=2, verbose_name='Blanco 6')
	kg_cnv = models.IntegerField(verbose_name='Kilos Conf. de Venta')
	kg_cnv_2 = models.IntegerField(verbose_name='Kilos Conf. de Venta 2')
	kg_cnv_3 = models.IntegerField(verbose_name='Kilos Conf. de Venta 3')
	blank_7 = models.CharField(max_length=2, verbose_name='Blanco 7')
	blank_8 = models.CharField(max_length=2, verbose_name='Blanco 8')
	blank_9 = models.CharField(max_length=2, verbose_name='Blanco 9')
	blank_10 = models.CharField(max_length=2, verbose_name='Blanco 10')
	gross_kg_3 = models.IntegerField(verbose_name='Kilos Brutos 3')
	unknown_1 = models.IntegerField(verbose_name='Desconocido 1')
	unknown_2 = models.IntegerField(verbose_name='Desconocido 2')
	gross_kg_4 = models.IntegerField(verbose_name='Kilos Brutos 4')
	rate = models.FloatField(verbose_name='Tarifa')
	net_weight_2 = models.IntegerField(verbose_name='Peso Neto 2')
	humidity_kg_2 = models.IntegerField(verbose_name='Kilos de Humedad 2')
	blank_11 = models.CharField(max_length=1, verbose_name='Blanco 11')
	blank_12 = models.CharField(max_length=1, verbose_name='Blanco 12')
	blank_13 = models.CharField(max_length=1, verbose_name='Blanco 13')
	blank_14 = models.CharField(max_length=2, verbose_name='Blanco 14')
	ctg = models.IntegerField(verbose_name='CTG')

	class Meta:
		verbose_name = 'Ventas'


class Applied(models.Model):
	entity_type = models.IntegerField(verbose_name='Tipo de Entidad')
	algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
	name = models.CharField(max_length=150, verbose_name='Razón Social')
	address_street = models.CharField(max_length=150, verbose_name='Calle')
	address_number = models.CharField(max_length=10, verbose_name='Numero')
	address_floor = models.CharField(max_length=10, verbose_name='Piso')
	address_apartment = models.CharField(max_length=10, verbose_name='Depto.')
	postal_code = models.CharField(max_length=10, verbose_name='Código Postal')
	postal_sufix = models.CharField(max_length=10, verbose_name='Sufijo')
	location = models.CharField(max_length=50, verbose_name='Localidad')
	state = models.CharField(max_length=80, verbose_name='Provincia')
	tel = models.CharField(max_length=80, verbose_name='Teléfono')
	amount = models.FloatField(verbose_name='Importe del Comprobante')
	movement_type = models.CharField(max_length=7, verbose_name='Tipo Movimiento')
	account_balance = models.FloatField(verbose_name='Saldo Cuenta')
	affected_voucher_balance = models.FloatField(verbose_name='Saldo de Movimientos Afectados')
	voucher = models.CharField(max_length=16, verbose_name='Comprobante')
	afected_voucher = models.CharField(max_length=16, verbose_name='Comprobante Afectado')
	voucher_date = models.DateField(null=True, verbose_name='Fecha Comprobante')
	afected_date = models.DateField(null=True, verbose_name='Fecha Afectado')
	expiration_date = models.DateField(null=True, verbose_name='Fecha Vencimiento')
	issue_date = models.DateField(null=True, verbose_name='Fecha Emision')
	concept = models.CharField(max_length=200, verbose_name='Concepto')
	cta_cte = models.CharField(max_length=1, verbose_name='Codigo de Cta. Cte.')
	cta_cte_description = models.CharField(max_length=50, verbose_name='Descripcion de Cta. Cte.')
	cta_cte_detail = models.CharField(max_length=100, verbose_name='Detalle de Cta. Cte.')
	amount_usd = models.FloatField(verbose_name='Importe del Comprobante en USD')
	modify_balance = models.CharField(max_length=2, verbose_name='Modifica Saldo')
	account_balance_usd = models.FloatField(verbose_name='Saldo Cuenta en USD')
	affected_balance_usd = models.FloatField(verbose_name='Saldo Afectado en USD')
	link = models.CharField(max_length=100, verbose_name='Detalle de Cta. Cte.')
	currency = models.CharField(max_length=1, verbose_name='Moneda')
	cuit = models.CharField(max_length=13, verbose_name='CUIT')
	cbu = models.CharField(max_length=27, verbose_name='CBU')
	zone = models.IntegerField(verbose_name='Codigo de Zona')
	zone_name = models.CharField(max_length=80, verbose_name='Descripcion Zona')
	amount_sign = models.FloatField(verbose_name='Importe Signo')
	numeric_voucher = models.CharField(max_length=12, verbose_name='Comprobante Numerico')
	internal_contract = models.CharField(max_length=80, verbose_name='Contrato Interno')
	export_contract = models.CharField(max_length=80, verbose_name='Contrato Exportador')
	exporter = models.IntegerField(verbose_name='Exportador')
	exporter_name = models.CharField(max_length=150, verbose_name='Nombre Exportador')
	exporter_group1 = models.IntegerField(verbose_name='Exportador Grupo1')
	exporter_name_group1 = models.CharField(max_length=150, verbose_name='Nombre Exportador Grupo1')
	exporter_group2 = models.IntegerField(verbose_name='Exportador Grupo2')
	exporter_name_group2 = models.CharField(max_length=150, verbose_name='Nombre Exportador Grupo2')
	exchange_rate = models.FloatField(verbose_name='Tipo de Cambio Emisión')
	debit_amount_pes = models.FloatField(verbose_name='Saldo Debito $')
	credit_amount_pes = models.FloatField(verbose_name='Saldo Credito $')
	debit_amount_usd = models.FloatField(verbose_name='Saldo Debito USD')
	credit_amount_usd = models.FloatField(verbose_name='Saldo Credito USD')

	class Meta:
		verbose_name = 'Cuenta Corriente Aplicada'
		verbose_name_plural = 'Cuentas Corrientes Aplicadas'


class CtaCte(models.Model):
	algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
	name = models.CharField(max_length=150, verbose_name='Razón Social')
	email = models.CharField(max_length=300, verbose_name='Email')
	address_street = models.CharField(max_length=150, verbose_name='Calle')
	address_number = models.CharField(max_length=10, verbose_name='Numero')
	address_floor = models.CharField(max_length=10, verbose_name='Piso')
	address_apartment = models.CharField(max_length=10, verbose_name='Depto.')
	postal_code = models.CharField(max_length=10, verbose_name='Código Postal')
	postal_sufix = models.CharField(max_length=10, verbose_name='Sufijo')
	location = models.CharField(max_length=50, verbose_name='Localidad')
	state = models.CharField(max_length=80, verbose_name='Provincia')
	tel = models.CharField(max_length=80, verbose_name='Teléfono')
	initial_balance_pes = models.FloatField(verbose_name='Saldo Inicial Pesos')
	initial_balance_usd = models.FloatField(verbose_name='Saldo Inicial Dolares')
	initial_balance_countable = models.FloatField(verbose_name='Saldo Inicial Contable')
	number_movements = models.IntegerField(verbose_name='Cantidad de Movimientos')
	balance = models.FloatField(verbose_name='Saldo')
	voucher = models.CharField(max_length=16, verbose_name='Comprobante')
	afected_voucher = models.CharField(max_length=16, verbose_name='Comprobante Afectado')
	voucher_date = models.DateField(null=True, verbose_name='Fecha Comprobante')
	afected_date = models.DateField(null=True, verbose_name='Fecha Afectado')
	concept = models.CharField(max_length=200, verbose_name='Concepto')
	currency = models.CharField(max_length=1, verbose_name='Moneda')
	amount = models.FloatField(verbose_name='Importe Comprobante')
	amount_tax = models.FloatField(verbose_name='Importe Sujeto Retencion')
	movement_type = models.CharField(max_length=7, verbose_name='Tipo Movimiento')
	exchange_rate = models.FloatField(verbose_name='Tipo de Cambio Emisión')
	exchange_rate_adjustment = models.FloatField(verbose_name='Tipo de Cambio Ajuste')
	exchange_rate_adjustment_date = models.DateField(null=True, verbose_name='Fecha Ajuste de Cambio')
	date_1 = models.DateField(null=True, verbose_name='Fecha Emision')
	date_2 = models.DateField(null=True, verbose_name='Fecha Vencimiento')
	amount_usd = models.FloatField(verbose_name='Importe Dolar')
	balance_mod = models.CharField(max_length=2, verbose_name='Modifica Saldo')
	link = models.CharField(max_length=80, verbose_name='Link')
	cuit = models.CharField(max_length=13, verbose_name='CUIT')
	cbu = models.CharField(max_length=27, verbose_name='CBU')
	tax_address_street = models.CharField(max_length=150, verbose_name='Calle Dom. Fiscal')
	tax_address_number = models.CharField(max_length=10, verbose_name='Numero Dom. Fiscal')
	tax_address_floor = models.CharField(max_length=10, verbose_name='Piso Dom. Fiscal')
	tax_address_apartment = models.CharField(max_length=10, verbose_name='Depto. Dom. Fiscal')
	tax_postal_code = models.CharField(max_length=10, verbose_name='Código Postal Fiscal')
	tax_posta_sufix = models.CharField(max_length=10, verbose_name='Sufijo Postal Fiscal')
	tax_location = models.CharField(max_length=50, verbose_name='Localidad Fiscal')
	tax_state = models.CharField(max_length=80, verbose_name='Provincia Fiscal')
	tax_tel = models.CharField(max_length=80, verbose_name='Teléfono Fiscal')
	amount_sign = models.FloatField(verbose_name='Importe Signo')
	numeric_voucher = models.CharField(max_length=12, verbose_name='Comprobante Numerico')
	internal_contract = models.CharField(max_length=80, verbose_name='Contrato Interno')
	export_contract = models.CharField(max_length=80, verbose_name='Contrato Exportador')
	exporter = models.IntegerField(verbose_name='Exportador')
	exporter_name = models.CharField(max_length=150, verbose_name='Nombre Exportador')
	exporter_group1 = models.IntegerField(verbose_name='Exportador Grupo1')
	exporter_name_group1 = models.CharField(max_length=150, verbose_name='Nombre Exportador Grupo1')
	exporter_group2 = models.IntegerField(verbose_name='Exportador Grupo2')
	exporter_name_group2 = models.CharField(max_length=150, verbose_name='Nombre Exportador Grupo2')
	cta_cte = models.CharField(max_length=1, verbose_name='Tipo Cta. Cte.')
	cta_cte_name = models.CharField(max_length=80, verbose_name='Descripcion Cta. Cte.')
	credit_limit = models.IntegerField(verbose_name='Limite Credito')
	credit_limit_other = models.IntegerField(verbose_name='Limite Credito Otro')
	zone = models.IntegerField(verbose_name='Codigo de Zona')
	zone_name = models.CharField(max_length=80, verbose_name='Descripcion Zona')
	seller = models.IntegerField(verbose_name='Vendedor')
	seller_name = models.CharField(max_length=80, verbose_name='Nombre Vendedor')
	alert = models.CharField(max_length=80, verbose_name='Alerta')
	overdue_balance = models.FloatField(verbose_name='Saldo Vencido')
	outstanding_balance = models.FloatField(verbose_name='Saldo A Vencer')
	overdue_balance_pes = models.FloatField(verbose_name='Saldo Vencido Pesos')
	outstanding_balance_pes = models.FloatField(verbose_name='Saldo A Vencer Pesos')
	overdue_balance_usd = models.FloatField(verbose_name='Saldo Vencido Dolar')
	outstanding_balance_usd = models.FloatField(verbose_name='Saldo A Vencer Dolar')
	exp = models.CharField(max_length=80, verbose_name='Estado Vencimiento')
	voucher_order = models.CharField(max_length=16, verbose_name='Comprobante Orden')

	class Meta:
		verbose_name = 'Cuenta Corriente'
		verbose_name_plural = 'Cuentas Corrientes'


class Currencies(models.Model):
	date = models.DateField(verbose_name='Fecha')
	dn_buy = models.FloatField(verbose_name='Dolar Nación')
	dl_buy = models.FloatField(blank=True, null=True, default=None, verbose_name='Dolar Libre')
	dn_sell = models.FloatField(verbose_name='Dolar Nación')
	dl_sell = models.FloatField(blank=True, null=True, default=None, verbose_name='Dolar Libre')

	class Meta:
		verbose_name = 'Moneda'
		verbose_name_plural = 'Monedas'


class Board(models.Model):
	date = models.DateField(verbose_name='Fecha')
	wheat_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
	wheat_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
	wheat_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
	wheat_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
	wheat12_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
	wheat12_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
	wheat12_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
	wheat12_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
	corn_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
	corn_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
	corn_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
	corn_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
	sunflower_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
	sunflower_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
	sunflower_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
	sunflower_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
	soy_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
	soy_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
	soy_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
	soy_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
	sorghum_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')
	sorghum_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')
	sorghum_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')
	sorghum_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')

	class Meta:
		verbose_name = 'Pizarra'
		verbose_name_plural = 'Pizarras'


class City(models.Model):
	STATE_CHOICES = (
		('BUE', 'Buenos Aires'),
		('CHA', 'Chaco'),
	)
	city = models.CharField(max_length=80, verbose_name='Ciudad')
	state = models.CharField(max_length=3, choices=STATE_CHOICES, verbose_name='Provincia', default='BUE')

	class Meta:
		verbose_name = 'Ciudad'
		verbose_name_plural = 'Ciudades'

	def __unicode__(self):
		return unicode(self.city)


class Rain(models.Model):
	date = models.DateField(verbose_name='Fecha')

	class Meta:
		verbose_name = 'Lluvia'
		verbose_name_plural = 'Lluvias'

	def __unicode__(self):
		return unicode(self.date)


class RainDetail(models.Model):
	rain = models.ForeignKey(Rain, on_delete=models.CASCADE)
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	mm = models.FloatField(verbose_name='Milimetros')

	class Meta:
		verbose_name = 'Detalle'
		verbose_name_plural = 'Detalles'
		unique_together = (('rain', 'city'),)


class Notifications(models.Model):
	date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
	title = models.CharField(max_length=200, verbose_name='Titulo')
	notification = models.TextField(verbose_name='Notificación')
	active = models.BooleanField(verbose_name='Activa/Inactiva', default=True)
	date_from = models.DateField(verbose_name='Vigencia Desde')
	date_to = models.DateField(verbose_name='Vigencia Hasta')

	class Meta:
		verbose_name = 'Notificación'
		verbose_name_plural = 'Notificaciones'


class ViewedNotifications(models.Model):
	notification = models.ForeignKey(Notifications, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	viewed = models.BooleanField(verbose_name='Notificación vista', default=False)

	class Meta:
		verbose_name = 'Notificación por Usuario'
		verbose_name_plural = 'Notificaciones por Usuario'
