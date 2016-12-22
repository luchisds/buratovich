import os
import re

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
				CtaCte.object.create(
					algoritmo_code = data[0],
					name = data[1],
					email = data[2],
					address_street = data[3],
					address_number = data[4],
					address_floor = data[5],
					address_apartment = data[6],
					postal_code = data[7],
					postal_sufix = data[8],
					location = data[9],
					state = data[10],
					tel = data[11],
					initial_balance_pes = data[12],
					initial_balance_usd = data[13],
					initial_balance_countable = data[14],
					number_movements = data[15],
					balance = data[16],
					voucher = data[17],
					afected_voucher = data[18],
					voucher_date = data[19],
					afected_date = data[20],
					concept = data[21],
					currency = data[22],
					concept = data[23],
					amount = data[24],
					amount_tax = data[25],
					movement_type = data[26],
					exchange_rate = data[27],
					exchange_rate_adjustment = data[28],
					exchange_rate_adjustment_date = data[29],
					date_1 = data[30],
					date_2 = data[31],
					amount_usd = data[32],
					balance_mod = data[33],
					link = data[34],
					cuit = data[35],
					cbu = data[36],
					tax_address_street = data[37],
					tax_address_number = data[38],
					tax_address_floor = data[39],
					tax_address_apartment = data[40],
					tax_postal_code = data[41],
					tax_posta_sufix = data[42],
					tax_location = data[43],
					tax_state = data[44],
					tax_tel = data[45],
					amount_sign = data[46],
					numeric_voucher = data[47],
					internal_contract = data[48],
					export_contract = data[49],
					exporter = data[50],
					exporter_name = data[51],
					exporter_group1 = data[52],
					exporter_name_group1 = data[53],
					exporter_group2 = data[54],
					exporter_name_group2 = data[55],
					cta_cte = data[56],
					cta_cte_name = data[57],
					credit_limit = data[58],
					credit_limit_other = data[59],
					zone = data[60],
					zone_name = data[61],
					seller = data[62],
					seller_name = data[63],
					alert = data[64],
					overdue_balance = data[65],
					outstanding_balance = data[66],
					overdue_balance_pes = data[67],
					outstanding_balance_pes = data[68],
					overdue_balance_usd = data[69],
					outstanding_balance_usd = data[70],
					exp = data[71],
					voucher_order = data[72]
				)
				i = i + 1
				reg.append(i)


	return render(request, 'ctacte.html', {'reg':reg})