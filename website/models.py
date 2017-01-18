# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# User related info
class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
	company_name = models.CharField(max_length=150, verbose_name='Razón Social')


class CtaCte(models.Model):
	algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
	name = models.CharField(max_length=100, verbose_name='Razón Social')
	email = models.CharField(max_length=100, verbose_name='Email')
	address_street = models.CharField(max_length=100, verbose_name='Calle')
	address_number = models.CharField(max_length=5, verbose_name='Numero')
	address_floor = models.CharField(max_length=3, verbose_name='Piso')
	address_apartment = models.CharField(max_length=5, verbose_name='Depto.')
	postal_code = models.CharField(max_length=5, verbose_name='Código Postal')
	postal_sufix = models.CharField(max_length=5, verbose_name='Sufijo')
	location = models.CharField(max_length=50, verbose_name='Localidad')
	state = models.CharField(max_length=80, verbose_name='Provincia')
	tel = models.CharField(max_length=20, verbose_name='Teléfono')
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
	tax_address_street = models.CharField(max_length=100, verbose_name='Calle Dom. Fiscal')
	tax_address_number = models.CharField(max_length=5, verbose_name='Numero Dom. Fiscal')
	tax_address_floor = models.CharField(max_length=3, verbose_name='Piso Dom. Fiscal')
	tax_address_apartment = models.CharField(max_length=5, verbose_name='Depto. Dom. Fiscal')
	tax_postal_code = models.CharField(max_length=5, verbose_name='Código Postal Fiscal')
	tax_posta_sufix = models.CharField(max_length=5, verbose_name='Sufijo Postal Fiscal')
	tax_location = models.CharField(max_length=50, verbose_name='Localidad Fiscal')
	tax_state = models.CharField(max_length=80, verbose_name='Provincia Fiscal')
	tax_tel = models.CharField(max_length=20, verbose_name='Teléfono Fiscal')
	amount_sign = models.FloatField(verbose_name='Importe Signo')
	numeric_voucher = models.CharField(max_length=12, verbose_name='Comprobante Numerico')
	internal_contract = models.CharField(max_length=80, verbose_name='Contrato Interno')
	export_contract = models.CharField(max_length=80, verbose_name='Contrato Exportador')
	exporter = models.IntegerField(verbose_name='Exportador')
	exporter_name = models.CharField(max_length=100, verbose_name='Nombre Exportador')
	exporter_group1 = models.IntegerField(verbose_name='Exportador Grupo1')
	exporter_name_group1 = models.CharField(max_length=100, verbose_name='Nombre Exportador Grupo1')
	exporter_group2 = models.IntegerField(verbose_name='Exportador Grupo2')
	exporter_name_group2 = models.CharField(max_length=100, verbose_name='Nombre Exportador Grupo2')
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


class Notifications(models.Model):
	date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
	title = models.CharField(max_length=200, verbose_name='Titulo')
	notification = models.TextField(verbose_name='Notificación')
	active = models.BooleanField(verbose_name='Activa/Inactiva', default=True)

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
