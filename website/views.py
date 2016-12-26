# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from models import CtaCte


def index(request):
	return render(request, 'index.html')


def company(request):
	return render(request, 'company.html')


def contact(request):
	return render(request, 'contact.html')


def ctacte(request):

	def evalDate(date):
		#Catch format error in date
		try:
			return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
		except ValueError:
			return ''

	def evalFloat(num):
		try:
			return float(num.replace('.', '').replace(',','.'))
		except ValueError:
			return 0

	def evalInt(num):
		try:
			return int(num.replace('.', '').replace(',','.'))
		except ValueError:
			return 0

	def evalText(text):
		return unicode(text.strip(' ').decode('iso-8859-1'))

	file = os.path.join(settings.BASE_DIR, 'FTP', 'CtaCteP.txt')
	#Chequea que el txt CtaCteP.txt existe, para evitar borrar los objetos del modelo y que no tenga contenido para cargar
	if os.path.isfile(file):
		
		#Si existen objetos en el modelo los borra
		if CtaCte.objects.count() > 0:
			CtaCte.objects.all().delete()

		with open(file, 'r') as f:
			reg = []
			i = 0
			for line in f:
				line = line.replace('\n', '')
				if len(line) > 0:
					data = re.split('\t+', line)
					print i
					#CtaCte.objects.create(
					reg.append(
						CtaCte(
							algoritmo_code = evalInt(data[0]),
							name = evalText(data[1]),
							email = evalText(data[2]),
							address_street = evalText(data[3]),
							address_number = evalText(data[4]),
							address_floor = evalText(data[5]),
							address_apartment = evalText(data[6]),
							postal_code = evalText(data[7]),
							postal_sufix = evalText(data[8]),
							location = evalText(data[9]),
							state = evalText(data[10]),
							tel = evalText(data[11]),
							initial_balance_pes = evalFloat(data[12]),
							initial_balance_usd = evalFloat(data[13]),
							initial_balance_countable = evalFloat(data[14]),
							number_movements = evalInt(data[15]),
							balance = evalFloat(data[16]),
							voucher = evalText(data[17]),
							afected_voucher = evalText(data[18]),
							voucher_date = evalDate(data[19]),
							#afected_date = evalDate(data[20]),
							concept = evalText(data[21]),
							currency = evalText(data[22]),
							amount = evalFloat(data[23]),
							amount_tax = evalFloat(data[24]),
							movement_type = evalText(data[25]),
							exchange_rate = evalFloat(data[26]),
							exchange_rate_adjustment = evalFloat(data[27]),
							exchange_rate_adjustment_date = evalDate(data[28]),
							date_1 = evalDate(data[29]),
							date_2 = evalDate(data[30]),
							amount_usd = evalFloat(data[31]),
							balance_mod = evalText(data[32]),
							link = evalText(data[33]),
							cuit = evalText(data[34]),
							cbu = evalText(data[35]),
							tax_address_street = evalText(data[36]),
							tax_address_number = evalText(data[37]),
							tax_address_floor = evalText(data[38]),
							tax_address_apartment = evalText(data[39]),
							tax_postal_code = evalText(data[40]),
							tax_posta_sufix = evalText(data[41]),
							tax_location = evalText(data[42]),
							tax_state = evalText(data[43]),
							tax_tel = evalText(data[44]),
							amount_sign = evalFloat(data[45]),
							numeric_voucher = evalText(data[46]),
							internal_contract = evalText(data[47]),
							export_contract = evalText(data[48]),
							exporter = evalInt(data[49]),
							exporter_name = evalText(data[50]),
							exporter_group1 = evalInt(data[51]),
							exporter_name_group1 = evalText(data[52]),
							exporter_group2 = evalInt(data[53]),
							exporter_name_group2 = evalText(data[54]),
							cta_cte = evalText(data[55]),
							cta_cte_name = evalText(data[56]),
							credit_limit = evalInt(data[57]),
							credit_limit_other = evalInt(data[58]),
							zone = evalInt(data[59]),
							zone_name = evalText(data[60]),
							seller = evalInt(data[61]),
							seller_name = evalText(data[62]),
							alert = evalText(data[63]),
							overdue_balance = evalFloat(data[64]),
							outstanding_balance = evalFloat(data[65]),
							overdue_balance_pes = evalFloat(data[66]),
							outstanding_balance_pes = evalFloat(data[67]),
							overdue_balance_usd = evalFloat(data[68]),
							outstanding_balance_usd = evalFloat(data[69]),
							exp = evalText(data[70]),
							voucher_order = evalText(data[71])
						)
					)
				i = i + 1
				#reg.append(i)
			CtaCte.objects.bulk_create(reg)

	return render(request, 'ctacte.html', {'reg':reg})