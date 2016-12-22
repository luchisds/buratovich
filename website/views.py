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
				data = re.split('\t+', line)
				print i, datetime.strptime(data[19], "%d/%m/%Y")
				# CtaCte.objects.create(
				# 	algoritmo_code = data[0],
				# 	name = data[1],
				# 	email = data[2],
				# 	address_street = data[3],
				# 	address_number = data[4],
				# 	address_floor = data[5],
				# 	address_apartment = data[6],
				# 	postal_code = data[7],
				# 	postal_sufix = data[8],
				# 	location = data[9],
				# 	state = data[10],
				# 	tel = data[11],
				# 	initial_balance_pes = data[12],
				# 	initial_balance_usd = data[13],
				# 	initial_balance_countable = data[14],
				# 	number_movements = data[15],
				# 	balance = data[16],
				# 	voucher = data[17],
				# 	afected_voucher = data[18],
				# 	voucher_date = datetime.strptime(data[19], '%d/%m/%Y'),
				# 	afected_date = datetime.strptime(data[20], '%d/%m/%Y'),
				# 	concept = data[21],
				# 	currency = data[22],
				# 	amount = data[23],
				# 	amount_tax = data[24],
				# 	movement_type = data[25],
				# 	exchange_rate = data[26],
				# 	exchange_rate_adjustment = data[27],
				# 	exchange_rate_adjustment_date = data[28],
				# 	date_1 = data[29],
				# 	date_2 = data[30],
				# 	amount_usd = data[31],
				# 	balance_mod = data[32],
				# 	link = data[33],
				# 	cuit = data[34],
				# 	cbu = data[35],
				# 	tax_address_street = data[36],
				# 	tax_address_number = data[37],
				# 	tax_address_floor = data[38],
				# 	tax_address_apartment = data[39],
				# 	tax_postal_code = data[40],
				# 	tax_posta_sufix = data[41],
				# 	tax_location = data[42],
				# 	tax_state = data[43],
				# 	tax_tel = data[44],
				# 	amount_sign = data[45],
				# 	numeric_voucher = data[46],
				# 	internal_contract = data[47],
				# 	export_contract = data[48],
				# 	exporter = data[49],
				# 	exporter_name = data[50],
				# 	exporter_group1 = data[51],
				# 	exporter_name_group1 = data[52],
				# 	exporter_group2 = data[53],
				# 	exporter_name_group2 = data[54],
				# 	cta_cte = data[55],
				# 	cta_cte_name = data[56],
				# 	credit_limit = data[57],
				# 	credit_limit_other = data[58],
				# 	zone = data[59],
				# 	zone_name = data[60],
				# 	seller = data[61],
				# 	seller_name = data[62],
				# 	alert = data[63],
				# 	overdue_balance = data[64],
				# 	outstanding_balance = data[65],
				# 	overdue_balance_pes = data[66],
				# 	outstanding_balance_pes = data[67],
				# 	overdue_balance_usd = data[68],
				# 	outstanding_balance_usd = data[69],
				# 	exp = data[70],
				# 	voucher_order = data[71]
				# )
				i = i + 1
				reg.append(i)


	return render(request, 'ctacte.html', {'reg':reg})