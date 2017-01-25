# -*- coding: utf-8 -*-

import math
import os
import re
from datetime import datetime
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect

import django_excel as excel

from models import CtaCte
from models import CtaCteKilos
from models import UserInfo
from models import Notifications
from models import ViewedNotifications


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
	notifications = Notifications.objects.filter(active=True)
	notifications_list = []
	notifications_id = []
	for n in notifications:
		if ViewedNotifications.objects.filter(notification=n.id, user=request.user).exists():
			pass
		else:
			notifications_list.append(n)
			notifications_id.append(n.id)

	if len(notifications_id) > 0:
		request.session['notifications'] = notifications_id
	
	return render(request, 'extranet.html', {'notifications': notifications_list})


@login_required
def notifications(request):
	if 'notifications' in request.session:
		notifications = request.session['notifications']
		for n in notifications:
			not_obj = Notifications.objects.get(id=n)
			ViewedNotifications.objects.create(notification=not_obj, user=request.user, viewed=True)
		del request.session['notifications']
		return redirect('/extranet/')
	else:
		return redirect('/')


@login_required
def ctacte(request):
	# If exists 'algoritmo_code' variable in session
	if 'algoritmo_code' in request.session:
		# Queryset with cta cte data
		data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_2')
		# Total amount
		total_sum = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).aggregate(Sum('amount_sign'))

		#### Add balance for every record in "data" queryset
		balance = 0
		records = []
		for d in data:
			balance += d['amount_sign']
			tmp_dict = {}
			tmp_dict['obj'] = d
			tmp_dict['balance'] = balance
			records.append(tmp_dict)

		#### Create a new sorted queryset/list
		limit = settings.EL_PAGINATION_PER_PAGE
		total_records = len(records)
		ctacte = []

		page_records = total_records
		while page_records >= 0:
			if page_records - limit < 0:
				tmp = records[0:page_records]
			else:
				tmp = records[page_records-limit:page_records]

			for obj in tmp:
				ctacte.append(obj)

			page_records -= limit

		#### Initial balance
		ib_records = 0
		remainder = total_records % limit
		initial_balance = []
		page_balance = []
		while ib_records < total_records:
			if ib_records == 0:
				tmp = records[0:remainder]
				ib_records += remainder
			else:
				tmp = records[0:ib_records+limit]
				ib_records += limit

			partial_balance = 0
			for obj in tmp:
				partial_balance += obj['obj']['amount_sign']

			initial_balance.append(partial_balance)

		# Scroll the list from first item to last-1 (is the cta cte total amount)
		for n in range(0,len(initial_balance)-1):
			tmp_dict = {}
			tmp_dict['page'] = len(initial_balance)-1-n
			tmp_dict['balance'] = initial_balance[n]
			page_balance.append(tmp_dict)

	return render(request, 'ctacte.html', {'ctacte': ctacte, 'total_sum': total_sum, 'page_balance': page_balance})


@login_required
def downloadexcel(request):
	if 'algoritmo_code' in request.session:
		data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_2')
		
		balance = 0
		records = []
		for d in data:
			balance += d['amount_sign']
			tmp_dict = OrderedDict()
			tmp_dict['Fecha Vencimiento'] = d['date_1']
			tmp_dict['Comprobante'] = d['voucher']
			tmp_dict['Observaciones'] = d['concept']
			tmp_dict['Fecha Emision'] = d['date_2']
			if d['movement_type'] == 'Debito':
				tmp_dict['Debe'] = d['amount_sign']
				tmp_dict['Haber'] = 0
			else:
				tmp_dict['Debe'] = 0
				tmp_dict['Haber'] = abs(d['amount_sign'])
			tmp_dict['Saldo'] = float(format(balance, '.2f'))
			records.append(tmp_dict)

		return excel.make_response_from_records(records, 'xlsx', file_name='CtaCte')


@login_required
def downloadtxt(request):
	if 'algoritmo_code' in request.session:
		data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_2')
		
		balance = 0
		records = []
		for d in data:
			balance += d['amount_sign']
			tmp_dict = OrderedDict()
			tmp_dict['Fecha Vencimiento'] = d['date_1']
			tmp_dict['Comprobante'] = d['voucher']
			tmp_dict['Observaciones'] = d['concept']
			tmp_dict['Fecha Emision'] = d['date_2']
			if d['movement_type'] == 'Debito':
				tmp_dict['Debe'] = d['amount_sign']
				tmp_dict['Haber'] = 0
			else:
				tmp_dict['Debe'] = 0
				tmp_dict['Haber'] = abs(d['amount_sign'])
			tmp_dict['Saldo'] = float(format(balance, '.2f'))
			records.append(tmp_dict)

		return excel.make_response_from_records(records, 'plain', file_name='CtaCte')


@login_required
def importcc(request, typecc):

	# bulk_create have a limit of 999 objects per batch for SQLite
	BULK_SIZE = 999

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

	def importCtaCteP(file):
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

		# break batch in small batches of 999 objects
		for j in range(0, len(record), BULK_SIZE):
			CtaCte.objects.bulk_create(record[j:j+BULK_SIZE])


	def importCtaCteKg(file):
		record = []
		r = 0
		for line in f:
			# Delete new line character
			line = line.replace('\n', '')
			if len(line) > 0:
				data = re.split('\t+', line)
				print r
				record.append(
					CtaCteKilos(
						algoritmo_code = evalInt(data[0]),
						name = evalText(data[1]),
						indicator = evalText(data[2]),
						species = evalText(data[3]),
						harvest = evalText(data[4]),
						species_description = evalText(data[5]),
						field = evalText(data[6]),
						field_description = evalText(data[7]),
						date = evalText(data[8]),
						voucher = evalText(data[9]),
						gross_kg = evalText(data[10]),
						humidity_percentage = evalText(data[11]),
						humidity_reduction = evalFloat(data[12]),
						humidity_kg = evalFloat(data[13]),
						shaking_reduction = evalFloat(data[14]),
						shaking_kg = evalInt(data[15]),
						volatile_reduction = evalFloat(data[16]),
						volatile_kg = evalText(data[17]),
						price_per_yard = evalText(data[18]),
						driver_code = evalDate(data[19]),
						driver_name = evalDate(data[20]),
						factor = evalText(data[21]),
						grade = evalText(data[22]),
						gluten = evalFloat(data[23]),
						number_1116A = evalFloat(data[24]),
						km = evalText(data[25]),
						charge_carry = evalFloat(data[26]),
						external_voucher_code = evalFloat(data[27]),
						external_voucher_branch = evalDate(data[28]),
						external_voucher_number = evalDate(data[29]),
						aeration_reduction = evalDate(data[30]),
						aeration_kg = evalFloat(data[31]),
						quality_reduction = evalText(data[32]),
						quality_kg = evalText(data[33]),
						zone = evalText(data[34]),
						zone_description = evalText(data[35]),
						plant_code = evalText(data[36]),
						service_billing_code = evalText(data[37]),
						service_billing_branch = evalText(data[38]),
						service_billing_number = evalText(data[39]),
						service_billing_date = evalText(data[40]),
						service_billing = evalText(data[41]),
						carrier_code = evalText(data[42]),
						carrier_name = evalText(data[43]),
						exclude_charge_expenses = evalText(data[44]),
						to_date = evalFloat(data[45]),
						observations = evalText(data[46]),
						follow_destination = evalText(data[47]),
						destination_code = evalText(data[48]),
						net_weight = evalInt(data[49]),
						tare = evalText(data[50]),
						gross_weight_recognized = evalInt(data[51]),
						plant_description = evalText(data[52]),
						gross_kg_var = evalInt(data[53]),
						gross_kg_2 = evalText(data[54]),
						blank_1 = evalText(data[55]),
						blank_2 = evalText(data[56]),
						blank_3 = evalInt(data[57]),
						blank_4 = evalInt(data[58]),
						allotment = evalInt(data[59]),
						allotment_description = evalText(data[60]),
						blank_5 = evalInt(data[61]),
						blank_6 = evalText(data[62]),
						kg_cnv = evalText(data[63]),
						kg_cnv_2 = evalFloat(data[64]),
						kg_cnv_3 = evalFloat(data[65]),
						blank_7 = evalFloat(data[66]),
						blank_8 = evalFloat(data[67]),
						blank_9 = evalFloat(data[68]),
						blank_10 = evalFloat(data[69]),
						gross_kg_3 = evalText(data[70]),
						unknown_1 = evalText(data[71]),
						unknown_2,
						gross_kg_4,
						rate,
						net_weight_2,
						humidity_kg_2,
						blank_11,
						blank_12,
						blank_13,
						blank_14,
						ctg
					)
				)
			r = r + 1

		# break batch in small batches of 999 objects
		for j in range(0, len(record), BULK_SIZE):
			CtaCte.objects.bulk_create(record[j:j+BULK_SIZE])


	if typecc <> 'pesos' and typecc <> 'kilos':
		raise Http404()
	else:
		# Read file and delete existing objects
		if typecc == 'pesos':
			file = os.path.join(settings.BASE_DIR, 'FTP', 'CtaCteP.txt')
			# Check if the file exists before deleteing all objects
			if os.path.isfile(file):
				# Delete all objects if there is 1 or more model objects
				if CtaCte.objects.count() > 0:
					CtaCte.objects.all().delete()
		else:
			file = os.path.join(settings.BASE_DIR, 'FTP', 'Web.txt')
			if os.path.isfile(file):
				if CtaCteKilos.objects.count() > 0:
					CtaCte.objects.all().delete()


		with open(file, 'r') as f:

			if typecc == 'pesos':


				

	return render(request, '__ctacte.html')