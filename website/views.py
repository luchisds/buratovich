# -*- coding: utf-8 -*-

import math
import os
import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect

from models import CtaCte
from models import UserInfo


def index(request):
	return render(request, 'index.html')


def company(request):
	return render(request, 'company.html')


def contact(request):
	return render(request, 'contact.html')


def auth_login(request):
	# If receive data via POST (login form)
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)

			user_code = User.objects.get(username=request.POST['username'])
			algoritmo_code = UserInfo.objects.get(user=user_code.id)
			# Save algoritmo_code on session
			request.session['algoritmo_code'] = algoritmo_code.algoritmo_code

			return redirect(settings.LOGIN_REDIRECT_URL)
		else:
			return redirect('/login/invalid/')
	else:
		# If data is received via GET and user is already authenticated redirect to /extranet/
		if request.user.is_authenticated():
			return redirect(settings.LOGIN_REDIRECT_URL)
		else:
			return render(request, 'login.html', {'login': 'login'})


def auth_login_invalid(request):
	return render(request, 'login.html', {'login_invalid': 'login invalid'})


def auth_login_required(request):
	return render(request, 'login.html', {'login_required': 'login required'})


@login_required
def auth_logout(request):
	logout(request)
	return redirect('/')


@login_required
def extranet(request):
	return render(request, 'extranet.html')


@login_required
def ctacte(request):
	# If exists 'algoritmo_code' variable in session
	if 'algoritmo_code' in request.session:
		data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_2')
		
		balance = 0
		tmp_list = []
		for d in data:
			balance += d['amount_sign']
			tmp_dict = {}
			tmp_dict['obj'] = d
			tmp_dict['balance'] = balance
			tmp_list.append(tmp_dict)

		# Create a new ordered queryset/list
		limit = settings.EL_PAGINATION_PER_PAGE
		# total = len(data)
		total = len(tmp_list)
		new_data = []

		while total >= 0:
			if total - limit < 0:
				# tmp = data[0:total]
				tmp = tmp_list[0:total]
			else:
				# tmp = data[total-limit:total]
				tmp = tmp_list[total-limit:total]

			for obj in tmp:
				new_data.append(obj)

			total = total-limit

	return render(request, 'ctacte.html', {'data': new_data})



def importcc(request):

	def evalDate(date):
		# Catch format error in date
		try:
			return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
		except ValueError:
			return None

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
		# Decode text in latin iso-8859-1 like (0xd1 --> ñ)
		return unicode(text.strip(' ').decode('iso-8859-1'))

	file = os.path.join(settings.BASE_DIR, 'FTP', 'CtaCteP.txt')
	# Check if the file exists before deleteing all objects
	if os.path.isfile(file):
		
		# Delete all objects if there is 1 or more model objects
		if CtaCte.objects.count() > 0:
			CtaCte.objects.all().delete()

		with open(file, 'r') as f:
			record = []
			r = 0
			for line in f:
				# Delete new line character
				line = line.replace('\n', '')
				if len(line) > 0:
					data = re.split('\t+', line)
					print r
					record.append(
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
							afected_date = evalDate(data[20]),
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
				r = r + 1

			# bulk_create have a limit of 999 objects per batch for SQLite
			BULK_SIZE = 999
			# break batch in small batches of 999 objects
			for j in range(0, len(record), BULK_SIZE):
				CtaCte.objects.bulk_create(record[j:j+BULK_SIZE])

	return render(request, '__ctacte.html')