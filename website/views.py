#-*- coding: utf-8 -*-

import math
import os
import re
import datetime
from collections import OrderedDict

from django.core import serializers
import json

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Q
from django.db.models import Sum
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

import django_excel as excel
import requests
from requests.auth import HTTPBasicAuth

from forms import CP
from models import CtaCte
from models import Deliveries
from models import Sales
from models import Applied
from models import UserInfo
from models import Notifications
from models import ViewedNotifications
from models import Currencies
from models import Board
from models import Analysis
from models import Remittances
from models import City
from models import Rain
from models import RainDetail
from tokens import account_activation_token

from bh.settings import RS_USER, RS_PASS


def handler404(request):
	return render(request, '404.html')


def handler500(request):
	return render(request, '500.html')


def cp(request):

	def handle_uploaded_file(f):
		fs = FileSystemStorage()
		filename = fs.save(os.path.join('cponline',f.name), f)
		# print fs.url(filename)

	if request.method == 'POST':
		form = CP(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['cp'])
			return HttpResponseRedirect('/')
	else:
		form = CP()
	return render(request, 'cp.html', {'form': form})


def index(request):
	currency = Currencies.objects.order_by('-date')[:1]
	board = Board.objects.order_by('-date')[:1]
	rain = Rain.objects.order_by('-date')[:1]
	rain = RainDetail.objects.filter(rain=rain).order_by('city__city')

	return render(request, 'index.html', {'currency': currency, 'board': board, 'rain': rain})


def get_currency(request):
	if request.POST:
		if request.POST.get('cDate'):
			currency = Currencies.objects.filter(date=request.POST.get('cDate'))

			if currency:
				return JsonResponse({'data': serializers.serialize('json',currency)})
			else:
				return JsonResponse({'data': None})

def get_board(request):
	if request.POST:
		if request.POST.get('bDate'):
			board = Board.objects.filter(date=request.POST.get('bDate'))

			if board:
				return JsonResponse({'data': serializers.serialize('json',board)})
			else:
				return JsonResponse({'data': None})

def get_rain(request):
	if request.POST:
		if request.POST.get('rDate'):
			rain = RainDetail.objects.filter(rain=request.POST.get('rDate')).values('rain', 'city__city', 'mm').order_by('city__city')
			data = []
			for r in rain:
				temp = {}
				temp['date'] = str(r['rain'])
				temp['city'] = r['city__city']
				temp['mm'] = r['mm']
				data.append(temp)

			if rain:
				return JsonResponse({'data': json.dumps(data)})
			else:
				return JsonResponse({'data': None})


def historic_rain(request):
	# Filter City = 1 only por Arrecifes
	rain = RainDetail.objects.filter(city=1).extra(select={'month':connection.ops.date_trunc_sql('month', '"website_raindetail"."rain_id"'), 'year':connection.ops.date_trunc_sql('year', '"website_raindetail"."rain_id"')}).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')
	history = OrderedDict()
	month_avg = OrderedDict()
	prev_year = 0
	prev_month = 0

	for r in rain:
		year = datetime.datetime.strptime(r['year'], "%Y-%m-%d").date().year
		month = datetime.datetime.strptime(r['month'], "%Y-%m-%d").date().month

		if history.get(year, None) is None:
			history[year] = OrderedDict()
			history[year]['rain'] = OrderedDict()
			history[year]['total'] = 0

		if month_avg.get(month, None) is None:
			month_avg[month] = OrderedDict()
			month_avg[month]['sum'] = 0
			month_avg[month]['count'] = 0

		if year == prev_year or prev_year == 0:
			if prev_month + 1 == month or prev_month == 0:
				history[year]['rain'][month] = r['mmsum']
				history[year]['total'] += r['mmsum']
				month_avg[month]['sum'] += r['mmsum']
				month_avg[month]['count'] += 1
			else:
				for i in range(prev_month+1, month):
					history[year]['rain'][datetime.datetime(year,i,1).date().month] = 0
					if month_avg.get(datetime.datetime(year,i,1).date().month, None) is None:
						month_avg[datetime.datetime(year,i,1).date().month] = OrderedDict()
						month_avg[datetime.datetime(year,i,1).date().month]['sum'] = 0
						month_avg[datetime.datetime(year,i,1).date().month]['count'] = 0
					month_avg[datetime.datetime(year,i,1).date().month]['count'] += 1
				history[year]['rain'][month] = r['mmsum']
				history[year]['total'] += r['mmsum']
				month_avg[month]['sum'] += r['mmsum']
				month_avg[month]['count'] += 1
		else:
			history[year]['rain'][month] = r['mmsum']
			history[year]['total'] += r['mmsum']
			month_avg[month]['sum'] += r['mmsum']
			month_avg[month]['count'] += 1

		prev_year = year
		prev_month = month

	return render(request, 'historic_rain.html', {'history':history, 'month_avg':month_avg})


def company(request):
	return render(request, 'company.html')


def gallery(request):
	return render(request, 'gallery.html')


def contact(request):
	return render(request, 'contact.html')


def taxes(request):
	return render(request, 'taxes.html')


def units(request):
	return render(request, 'units.html')


def cv(request):
	return render(request, 'cv.html')


def auth_activate_account(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		# Search user account
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	# Check token, mark account as active and confirm account
	if user is not None and account_activation_token.check_token(user, token):
		user.userinfo.account_confirmed = True
		user.userinfo.save()
		user.is_active = True
		user.save()

		# Set backend for user instead authenticate() function
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)

		request.session['algoritmo_code'] = user.userinfo.algoritmo_code

		return render(request, 'change_password.html', {'account_confirmed': True})
	else:
		return redirect(reverse('login_invalid'))


def auth_login(request):
	# If receive data via POST (login form)
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		# Authenticate user first
		user = authenticate(username=username, password=password)
		# Check if user is active
		if user is not None:
			if user.is_active == True:
				login(request, user)

				user_code = User.objects.get(username=request.POST['username'])
				algoritmo_code = UserInfo.objects.get(user=user_code.id)
				# Save algoritmo_code on session
				request.session['algoritmo_code'] = algoritmo_code.algoritmo_code

				return redirect(settings.LOGIN_REDIRECT_URL)
			else:
				return redirect(reverse('login_inactive_account'))
		else:
			return redirect(reverse('login_invalid'))
	else:
		# If data is received via GET and user is already authenticated redirect to /extranet/
		if request.user.is_authenticated():
			return redirect(settings.LOGIN_REDIRECT_URL)
		else:
			return render(request, 'login.html', {'login': True})


def auth_login_invalid(request):
	return render(request, 'login.html', {'login_invalid': True})


def auth_login_required(request):
	return render(request, 'login.html', {'login_required': True})


def auth_login_inactive_account(request):
	return render(request, 'login.html', {'inactive_account': True})


@login_required
def change_password(request):
	if request.POST:
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		if password1 is not None and password1 == password2:
			try:
				request.user.set_password(password1)
				# If current password is the original random password then mark as random password as False
				if request.user.userinfo.random_password == True:
					request.user.userinfo.random_password = False
					request.user.userinfo.save()
				request.user.save()

				user = authenticate(username=request.user.username, password=password1)
				if user is not None and user.is_active == True:
					login(request, user)
					request.session['algoritmo_code'] = request.user.userinfo.algoritmo_code
					return render(request, 'change_password.html', {'changed':'changed'})
				else:
					print 'Usuario no encontrado'
			except:
				print 'No se pudede cambiar el password'
	else:
		return render(request, 'change_password.html')


@login_required
def auth_logout(request):
	logout(request)
	return redirect('/')


@login_required
def extranet(request):
	notifications = Notifications.objects.filter(active=True, date_to__gte=datetime.date.today())
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
		return redirect(reverse('extranet'))
	else:
		return redirect('/')


@login_required
def ctacte(request):

	vouchers = ['LC', 'IC', 'LB', 'IB', 'ND', 'NC', 'FC']

	# If exists 'algoritmo_code' variable in session
	if 'algoritmo_code' in request.session:
		# Queryset with cta cte data
		data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_2')
		# If exist data
		if data:
			# Total amount
			total_sum = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).aggregate(Sum('amount_sign'))

			#### Add balance for every record in "data" queryset
			balance = 0
			records = []
			for d in data:
				balance += d['amount_sign']
				tmp_dict = {}
				tmp_dict['obj'] = d
				#tmp_dict['file'] = search_file(d['voucher'])
				if d['voucher'].split(' ')[0] in vouchers:
					tmp_dict['file'] = d['voucher']
				else:
					tmp_dict['file'] = None
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
		else:
			return render(request, 'ctacte.html')


@login_required
def deliveries(request):
	if 'algoritmo_code' in request.session:

		if request.POST:
			current_species = request.POST.getlist('checks')
			request.session['current_species'] = current_species
		else:
			current_species = ''

		# Dict with [harvest]-->[species]-->[species description]
		species = Deliveries.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('species', 'harvest', 'speciesharvest', 'species_description').order_by('-harvest','species').distinct()
		# If exist species
		if species:
			species_description = []
			species_by_harvest = OrderedDict()
			for s in species:
				if species_by_harvest.get(s['harvest'], None) is None:
					species_by_harvest[s['harvest']] = OrderedDict()
				species_by_harvest[s['harvest']][s['species']] = OrderedDict()
				species_by_harvest[s['harvest']][s['species']]['description'] = s['species_description'].replace('COSECHA ', '')
				# Set attr TRUE if current harvest-species is in request to render checked checkboxes in template
				if s['speciesharvest'] in current_species:
					species_by_harvest[s['harvest']][s['species']]['checked'] = True
				else:
					species_by_harvest[s['harvest']][s['species']]['checked'] = False
				species_description.append((s['species_description'].replace('COSECHA ', ''), s['species']+s['harvest']))


			if request.POST:
				# Create a filter by species / harvest using Q function and OR statement (|)
				speciesharvest_filter = Q()
				for item in current_species:
					speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=item)

				## Total kg for selected species_description
				total_kg = Deliveries.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).aggregate(Sum('net_weight'))

				# Dict with [species description]-->[field]-->[tickets]
				fields = Deliveries.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).values('field', 'field_description', 'species_description').distinct()
				tickets = Deliveries.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).values('date', 'voucher', 'gross_kg', 'humidity_percentage', 'humidity_kg', 'shaking_reduction', 'shaking_kg', 'volatile_reduction', 'volatile_kg', 'net_weight', 'factor', 'grade', 'number_1116A', 'external_voucher_number', 'driver_name', 'field', 'species_description').order_by('date')

				tickets_by_field = {}
				tickets_for_analysis = []
				for s in species_description:
					# Description
					sd = s[0]
					# Species Harvest
					sh = s[1]
					if sh in current_species:
						if tickets_by_field.get(sd, None) is None:
							tickets_by_field[sd] = OrderedDict()
						for f in fields:
							if f['species_description'].replace('COSECHA ', '') == sd:
								if tickets_by_field[sd].get(f['field'], None) is None:
									tickets_by_field[sd][f['field']] = OrderedDict()
									tickets_by_field[sd][f['field']]['number'] = f['field']
									tickets_by_field[sd][f['field']]['name'] = f['field_description']
								tickets_by_field[sd][f['field']]['tickets'] = OrderedDict()
								total_gross = 0
								total_hum = 0
								total_sha = 0
								total_vol = 0
								total_net = 0
								tickets_count = 0
								for t in tickets:
									if t['species_description'].replace('COSECHA ', '') == sd and t['field'] == f['field']:
										tickets_by_field[sd][f['field']]['tickets'][t['voucher']] = t
										total_gross += t['gross_kg']
										total_hum += t['humidity_kg']
										total_sha += t['shaking_kg']
										total_vol += t['volatile_kg']
										total_net += t['net_weight']
										tickets_count += 1
										# Ticket number (voucher) for Analysis filter
										tickets_for_analysis.append(t['voucher'])
									tickets_by_field[sd][f['field']]['total_gross'] = total_gross
									tickets_by_field[sd][f['field']]['total_hum'] = total_hum
									tickets_by_field[sd][f['field']]['total_sha'] = total_sha
									tickets_by_field[sd][f['field']]['total_vol'] = total_vol
									tickets_by_field[sd][f['field']]['total_net'] = total_net
									tickets_by_field[sd][f['field']]['tickets_count'] = tickets_count

				# Get ticket and analysis
				remittances = Remittances.objects.filter(ticket__in = tickets_for_analysis).values('ticket', 'analysis')
				# dict [Ticket] --> [Analysis]
				ticket_analysis = {}
				# dict [Analysis] --> [Analysis detail]
				analysis_detail = {}
				for i in remittances:
					ticket_analysis[i['ticket']] = i['analysis']
					if analysis_detail.get(i['analysis'], None) is None:
						analysis = Analysis.objects.filter(analysis = i['analysis']).exclude(percentage=0).values('analysis', 'date', 'protein', 'analysis_costs', 'gluten', 'analysis_item', 'percentage', 'bonus', 'reduction', 'item_descripcion').order_by('analysis', 'item_descripcion')
						analysis_detail[i['analysis']] = analysis

				return render(request, 'deliveries.html', {'species':species_by_harvest, 'tickets':tickets_by_field, 'total': total_kg, 'ticket_analysis': ticket_analysis, 'analysis_detail': analysis_detail})

			else:
				# If request is GET
				return render(request, 'deliveries.html', {'species':species_by_harvest})
		else:
			return render(request, 'deliveries.html')


@login_required
def sales(request):
	if 'algoritmo_code' in request.session:

		if request.POST:
			current_species = request.POST.getlist('checks')
			request.session['current_species'] = current_species
		else:
			current_species = ''

		# Dict with [harvest]-->[species]-->[species description]
		species = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('species', 'harvest', 'speciesharvest', 'species_description').order_by('-harvest','species').distinct()
		# If exist species
		if species:

			species_description = []
			species_by_harvest = OrderedDict()
			for s in species:
				if species_by_harvest.get(s['harvest'], None) is None:
					species_by_harvest[s['harvest']] = OrderedDict()
				species_by_harvest[s['harvest']][s['species']] = OrderedDict()
				species_by_harvest[s['harvest']][s['species']]['description'] = s['species_description'].replace('COSECHA ', '')
				# Set attr TRUE if current harvest-species is in request to render checked checkboxes in template
				if s['speciesharvest'] in current_species:
					species_by_harvest[s['harvest']][s['species']]['checked'] = True
				else:
					species_by_harvest[s['harvest']][s['species']]['checked'] = False
				species_description.append((s['species_description'].replace('COSECHA ', ''), s['species']+s['harvest']))

			if request.POST:
				# Create a filter by species / harvest using Q function and OR statement (|)
				speciesharvest_filter = Q()
				for item in current_species:
					speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=item)


				## Total kg for selected species_description
				total_kg = {}
				total_kg['sales'] = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code'], indicator='2').filter(speciesharvest_filter).aggregate(Sum('net_weight'))
				total_kg['to_set'] = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code'], indicator='2B').filter(speciesharvest_filter).aggregate(Sum('net_weight'))
				total_kg['other'] = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code'], indicator='3').filter(speciesharvest_filter).aggregate(Sum('net_weight'))


				# Dict with [species description]-->[sales]
				voucher = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).values('id', 'date', 'voucher', 'field_description', 'service_billing_date', 'to_date', 'gross_kg', 'service_billing_number', 'number_1116A', 'price_per_yard', 'grade', 'driver_name', 'observations', 'species_description', 'indicator').order_by('date')


				sales = {}
				for s in species_description:
					# Description
					sd = s[0]
					# Species Harvest
					sh = s[1]
					if sh in current_species:
						if sales.get(sd, None) is None:
							sales[sd] = OrderedDict()
							total_g_sales = 0
							total_p_sales = 0
							total_l_sales = 0
							count_sales = 0
							total_g_to_set = 0
							count_to_set = 0
							total_i_others = 0
							total_o_others = 0
							count_others = 0
							for v in voucher:
								if v['species_description'].replace('COSECHA ', '') == sd:
									if v['indicator'] == '2':
										if sales[sd].get('sales', None) is None:
											sales[sd]['sales'] = OrderedDict()
											sales[sd]['sales']['vouchers'] = OrderedDict()
										sales[sd]['sales']['vouchers'][v['id']] = v
										total_g_sales += v['gross_kg']
										total_p_sales += v['service_billing_number']
										total_l_sales += v['number_1116A']
										count_sales += 1
									elif v['indicator'] == '2B':
										if sales[sd].get('to_set', None) is None:
											sales[sd]['to_set'] = OrderedDict()
											sales[sd]['to_set']['vouchers'] = OrderedDict()
										sales[sd]['to_set']['vouchers'][v['voucher']] = v
										total_g_to_set += v['gross_kg']
										count_to_set += 1
									else:
										if sales[sd].get('others', None) is None:
											sales[sd]['others'] = OrderedDict()
											sales[sd]['others']['vouchers'] = OrderedDict()
										sales[sd]['others']['vouchers'][v['voucher']] = v
										if v['gross_kg'] > 0:
											total_i_others += v['gross_kg']
										else:
											total_o_others += v['gross_kg']
										count_others += 1

									if sales[sd].get('sales', None) <> None:
										sales[sd]['sales']['total_g_sales'] = total_g_sales
										sales[sd]['sales']['total_p_sales'] = total_p_sales
										sales[sd]['sales']['total_l_sales'] = total_l_sales
										sales[sd]['sales']['count_sales'] = count_sales
									if sales[sd].get('to_set', None) <> None:
										print count_to_set
										print total_g_to_set
										sales[sd]['to_set']['total_g_to_set'] = total_g_to_set
										sales[sd]['to_set']['count_to_set'] = count_to_set
									if sales[sd].get('others', None) <> None:
										sales[sd]['others']['total_i_others'] = total_i_others
										sales[sd]['others']['total_o_others'] = total_o_others
										sales[sd]['others']['count_others'] = count_others

				return render(request, 'sales.html', {'species':species_by_harvest, 'total':total_kg, 'sales':sales})

			else:
				# If request is GET
				return render(request, 'sales.html', {'species':species_by_harvest})
		else:
			return render(request, 'sales.html')


@login_required
def applied(request):
	if 'algoritmo_code' in request.session:
		# Queryset with cta cte data
		data = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('expiration_date')
		# If no data
		if data:
			# Total amount
			total_sum = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code']).aggregate(Sum('amount_sign'))

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
			applied_ctacte = []

			page_records = total_records
			while page_records >= 0:
				if page_records - limit < 0:
					tmp = records[0:page_records]
				else:
					tmp = records[page_records-limit:page_records]

				for obj in tmp:
					applied_ctacte.append(obj)

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

			return render(request, 'applied.html', {'applied': applied_ctacte, 'total_sum': total_sum, 'page_balance': page_balance})
		else:
			return render(request, 'applied.html')


def downloadRainExcel(request):
	rain = RainDetail.objects.filter(city=1).extra(select={'month':connection.ops.date_trunc_sql('month', '"website_raindetail"."rain_id"'), 'year':connection.ops.date_trunc_sql('year', '"website_raindetail"."rain_id"')}).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')

	history = OrderedDict()
	prev_year = 0
	prev_month = 0

	for r in rain:
		year = datetime.datetime.strptime(r['year'], "%Y-%m-%d").date().year
		month = datetime.datetime.strptime(r['month'], "%Y-%m-%d").date().month

		if history.get(year, None) is None:
			history[year] = OrderedDict()
			history[year]['rain'] = OrderedDict()
			history[year]['total'] = 0

		if year == prev_year or prev_year == 0:
			if prev_month + 1 == month or prev_month == 0:
				history[year]['rain'][month] = r['mmsum']
				history[year]['total'] += r['mmsum']
			else:
				for i in range(prev_month+1, month):
					history[year]['rain'][datetime.datetime(year,i,1).date().month] = 0
				history[year]['rain'][month] = r['mmsum']
				history[year]['total'] += r['mmsum']
		else:
			history[year]['rain'][month] = r['mmsum']
			history[year]['total'] += r['mmsum']

		prev_year = year
		prev_month = month

	records = []
	for k, v in history.items():
		tmp_dict = OrderedDict()
		tmp_dict[u'Año'] = k
		tmp_dict['Ene'] = v['rain'].get(1, 0)
		tmp_dict['Feb'] = v['rain'].get(2, 0)
		tmp_dict['Mar'] = v['rain'].get(3, 0)
		tmp_dict['Abr'] = v['rain'].get(4, 0)
		tmp_dict['May'] = v['rain'].get(5, 0)
		tmp_dict['Jun'] = v['rain'].get(6, 0)
		tmp_dict['Jul'] = v['rain'].get(7, 0)
		tmp_dict['Ago'] = v['rain'].get(8, 0)
		tmp_dict['Sep'] = v['rain'].get(9, 0)
		tmp_dict['Oct'] = v['rain'].get(10, 0)
		tmp_dict['Nov'] = v['rain'].get(11, 0)
		tmp_dict['Dic'] = v['rain'].get(12, 0)
		tmp_dict['Total'] = v['total']
		records.append(tmp_dict)

	filename = 'Lluvias Historico'

	return excel.make_response_from_records(records, 'xlsx', file_name=filename)


@login_required
def downloadPDFExtranet(request):

	vouchers = {
		'LC': {'codigo': ['C',], 'separator': ' ', 'url':''},
		'IC': {'codigo': ['C',], 'separator': ' ', 'url':''},
		'LB': {'codigo': ['B',], 'separator': ' ', 'url':''},
		'IB': {'codigo': ['B',], 'separator': ' ', 'url':''},
		'ND': {'codigo': ['HNDCER','HNDE','NDE','NDECAJ','NDECER','NDEPER',], 'separator': '_', 'url':'ventas/'},
		'NC': {'codigo': ['HNCCER','HNCR','NCR','NCRCER','NCRDEV','NCSCER',], 'separator': '_', 'url':'ventas/'},
		'FC': {'codigo': ['FAC','FACCER','FACD','FACSER','FASCER','HFAC','HFACER',], 'separator': '_', 'url':'ventas/'},
	}

	def search_file(voucher):
		voucher = voucher.split(' ')
		if vouchers.get(voucher[0], None) is None:
			return None
		else:
			separator = vouchers[voucher[0]]['separator']
			url = vouchers[voucher[0]]['url']
			for c in vouchers[voucher[0]]['codigo']:
				file_name = c + separator + voucher[1] + separator + voucher[2] + '.pdf'
				r = requests.get('http://190.92.102.226:1500/'+url+file_name, auth=HTTPBasicAuth(RS_USER, RS_PASS))
				if r.status_code == 200:
					return {'file':r, 'filename':file_name}

	if 'algoritmo_code' in request.session:
		f = request.GET['f']
		file = search_file(f)

		if file:
			length = file['file'].headers['Content-Length']
			response = StreamingHttpResponse(file['file'].content, content_type="application/pdf")
			response['Content-Length'] = length
			response['Content-Disposition'] = "attachment; filename='%s'" % file['filename']
			return response
		else:
			raise Http404

	# def search_file(voucher):
	# 	voucher_list = voucher.split(' ')
	# 	if vouchers.get(voucher_list[0], None) is None:
	# 		return None
	# 	else:
	# 		separator = vouchers[voucher_list[0]]['separator']
	# 		for c in vouchers[voucher_list[0]]['codigo']:
	# 			file_name = c + separator + voucher_list[1] + separator + voucher_list[2] + '.pdf'
	# 			file = os.path.join(settings.BASE_DIR, 'FTP', 'CtaCtePesos', file_name)
	# 			if os.path.isfile(file):
	# 				return file_name

	# if 'algoritmo_code' in request.session:
	# 	f = request.GET['f']
	# 	filename = f+'.pdf'
	# 	r = requests.get('http://190.92.102.226:1500/'+f+'.pdf', auth=HTTPBasicAuth(RS_USER, RS_PASS))
	# 	if r.status_code == 200:
	# 		length = r.headers['Content-Length']
	# 		response = StreamingHttpResponse(r.content, content_type="application/pdf")
	# 		response['Content-Length'] = length
	# 		response['Content-Disposition'] = "attachment; filename='%s'" % filename
	# 		return response
	# 	else:
	# 		raise Http404


@login_required
def downloadexcel(request, module):

	def getPesosExcel():
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

		filename = 'CtaCte Pesos'
		return records, filename

	def getAppliedExcel():
		data = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('expiration_date')
		
		balance = 0
		records = []
		for d in data:
			balance += d['amount_sign']
			tmp_dict = OrderedDict()
			tmp_dict['Fecha Vencimiento'] = d['expiration_date']
			tmp_dict['Comprobante'] = d['voucher']
			tmp_dict['Observaciones'] = d['concept']
			tmp_dict['Fecha Emision'] = d['issue_date']
			if d['movement_type'] == 'Debito':
				tmp_dict['Debe'] = d['amount_sign']
				tmp_dict['Haber'] = 0
			else:
				tmp_dict['Debe'] = 0
				tmp_dict['Haber'] = abs(d['amount_sign'])
			tmp_dict['Saldo'] = float(format(balance, '.2f'))
			records.append(tmp_dict)

		filename = 'CtaCte Aplicada'
		return records, filename

	def getDeliveriesExcel(species):
		speciesharvest_filter = Q()
		for s in species:
			speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=s)

		tickets = Deliveries.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).values('date', 'voucher', 'gross_kg', 'humidity_percentage', 'humidity_kg', 'shaking_reduction', 'shaking_kg', 'volatile_reduction', 'volatile_kg', 'net_weight', 'factor', 'grade', 'number_1116A', 'external_voucher_number', 'driver_name', 'field', 'field_description', 'species_description').order_by('field_description', 'date')

		records = []
		for t in tickets:
			tmp_dict = OrderedDict()
			tmp_dict['Especie y Cosecha'] = t['species_description']
			tmp_dict['Campo'] = t['field']
			tmp_dict['Nombre del Campo'] = t['field']
			tmp_dict['Fecha'] = t['date']
			tmp_dict['Comprobante'] = t['voucher']
			tmp_dict['Kg. Brutos'] = t['gross_kg']
			tmp_dict['Hum. (%)'] = t['humidity_percentage']
			tmp_dict['Hum. (Kg)'] = t['humidity_kg']
			tmp_dict['Zarandeo (Merma)'] = t['shaking_reduction']
			tmp_dict['Zarandeo (Kg)'] = t['shaking_kg']
			tmp_dict['Volatil (Merma)'] = t['volatile_reduction']
			tmp_dict['Volatil (Kg)'] = t['volatile_kg']
			tmp_dict['Kg. Netos'] = t['net_weight']
			tmp_dict['Factor'] = t['factor']
			tmp_dict['Grado'] = t['grade']
			tmp_dict['Numero 1116A'] = t['number_1116A']
			tmp_dict['Carta de Porte'] = t['external_voucher_number']
			tmp_dict['Chofer'] = t['driver_name']
			records.append(tmp_dict)

		filename = 'Entregas'
		return records, filename

	def getSalesExcel(species):
		speciesharvest_filter = Q()
		for s in species:
			speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=s)

		sales = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).values('date', 'voucher', 'field_description', 'service_billing_date', 'to_date', 'gross_kg', 'service_billing_number', 'number_1116A', 'price_per_yard', 'grade', 'species_description').order_by('species_description', 'date')

		records = []
		for s in sales:
			tmp_dict = OrderedDict()
			tmp_dict['Especie y Cosecha'] = s['species_description']
			tmp_dict['Fecha'] = s['date']
			tmp_dict['Comprobante'] = s['voucher']
			tmp_dict['Destino'] = s['field_description']
			tmp_dict['Fecha de Entrega Desde'] = s['service_billing_date']
			tmp_dict['Fecha de Entrega Hasta'] = s['to_date']
			tmp_dict['Kilos'] = s['gross_kg']
			tmp_dict['Pend. TC'] = s['service_billing_number']
			tmp_dict['Liquidados'] = s['number_1116A']
			tmp_dict['Precio por QQ.'] = s['price_per_yard']
			tmp_dict['Moneda'] = s['grade']
			records.append(tmp_dict)

		filename = 'Ventas'
		return records, filename

	if 'algoritmo_code' in request.session:
		if module == 'pesos':
			records, filename = getPesosExcel()
		elif module == 'applied':
			records, filename = getAppliedExcel()
		elif module == 'deliveries':
			records, filename = getDeliveriesExcel(request.session['current_species'])
		elif module == 'sales':
			records, filename = getSalesExcel(request.session['current_species'])
		else:
			raise Http404()

		return excel.make_response_from_records(records, 'xlsx', file_name=filename)


@login_required
@staff_member_required
def importdata(request, datatype):

	# bulk_create have a limit of 999 objects per batch for SQLite
	BULK_SIZE = 999

	def evalDate(date):
		# Catch format error in date
		try:
			return datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
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


	def importRemittances(file):
		record = []
		r = 0
		# Exclude header
		file.next()
		for line in file:
			# Delete new line character
			line = line.replace('\n', '').replace('\r', '')
			if len(line) > 0:
				data = re.split('\t', line)
				print r
				# Certified True or False
				if evalText(data[20]) == 'Sí':
					is_certified = True
				else:
					is_certified = False
				record.append(
					Remittances(
						entry_point = evalInt(data[0]),
						analysis_number = evalInt(data[1]),
						analysis = evalText(data[2]),
						date = evalDate(data[3]),
						entry_point_ticket = evalInt(data[18]),
						ticket_number = evalInt(data[19]),
						certified = is_certified,
						ticket = 'TK ' + evalText(data[21][:5]+data[21][7:]),
						ticket_date = evalDate(data[22]),
						net_kg = evalInt(data[23])
					)
				)
			r = r + 1

		# break batch in small batches of 999 objects
		for j in range(0, len(record), BULK_SIZE):
			Remittances.objects.bulk_create(record[j:j+BULK_SIZE])


	def importAnalysis(file):
		record = []
		r = 0
		# Exclude header
		file.next()
		for line in file:
			# Delete new line character
			line = line.replace('\n', '').replace('\r', '')
			if len(line) > 0:
				data = re.split('\t', line)
				print r
				record.append(
					Analysis(
						entry_point = evalInt(data[0]),
						analysis_number = evalInt(data[1]),
						analysis = evalText(data[2]),
						date = evalDate(data[3]),
						newsletter_number = evalText(data[4]),
						field = evalInt(data[5]),
						lot = evalText(data[6]),
						field_description = evalText(data[7]),
						species = evalText(data[8]),
						harvest = evalText(data[9]),
						protein = evalFloat(data[11]),
						grade = evalInt(data[12]),
						factor = evalFloat(data[13]),
						analysis_costs = evalFloat(data[14]),
						gluten = evalInt(data[15]),
						analysis_item = evalInt(data[18]),
						percentage = evalFloat(data[19]),
						bonus = evalFloat(data[20]),
						reduction = evalFloat(data[21]),
						item_descripcion = evalText(data[22])
					)
				)
			r = r + 1

		# break batch in small batches of 999 objects
		for j in range(0, len(record), BULK_SIZE):
			Analysis.objects.bulk_create(record[j:j+BULK_SIZE])


	def importApplied(file):
		record = []
		r = 0
		for line in file:
			# Delete new line character
			line = line.replace('\n', '').replace('\r', '')
			if len(line) > 0:
				data = re.split('\t', line)
				print r
				record.append(
					Applied(
						entity_type = evalInt(data[0]),
						algoritmo_code = evalInt(data[1]),
						name = evalText(data[2]),
						address_street = evalText(data[3]),
						address_number = evalText(data[4]),
						address_floor = evalText(data[5]),
						address_apartment = evalText(data[6]),
						postal_code = evalText(data[7]),
						postal_sufix = evalText(data[8]),
						location = evalText(data[9]),
						state = evalText(data[10]),
						tel = evalText(data[11]),
						amount = evalFloat(data[12]),
						movement_type = evalText(data[13]),
						account_balance = evalFloat(data[14]),
						affected_voucher_balance = evalInt(data[15]),
						voucher = evalText(data[16]),
						afected_voucher = evalText(data[17]),
						voucher_date = evalDate(data[18]),
						afected_date = evalDate(data[19]),
						expiration_date = evalDate(data[20]),
						issue_date = evalDate(data[21]),
						concept = evalText(data[22]),
						cta_cte = evalText(data[23]),
						cta_cte_description = evalText(data[24]),
						cta_cte_detail = evalText(data[25]),
						amount_usd = evalFloat(data[26]),
						modify_balance = evalText(data[27]),
						account_balance_usd = evalFloat(data[28]),
						affected_balance_usd = evalFloat(data[29]),
						link = evalText(data[30]),
						currency = evalText(data[31]),
						cuit = evalText(data[32]),
						cbu = evalText(data[33]),
						zone = evalInt(data[34]),
						zone_name = evalText(data[35]),
						amount_sign = evalFloat(data[36]),
						numeric_voucher = evalText(data[37]),
						internal_contract = evalText(data[38]),
						export_contract = evalText(data[39]),
						exporter = evalInt(data[40]),
						exporter_name = evalText(data[41]),
						exporter_group1 = evalInt(data[42]),
						exporter_name_group1 = evalText(data[43]),
						exporter_group2 = evalInt(data[44]),
						exporter_name_group2 = evalText(data[45]),
						exchange_rate = evalFloat(data[46]),
						debit_amount_pes = evalFloat(data[47]),
						credit_amount_pes = evalFloat(data[48]),
						debit_amount_usd = evalFloat(data[49]),
						credit_amount_usd = evalFloat(data[50])
					)
				)
			r = r + 1

		# break batch in small batches of 999 objects
		for j in range(0, len(record), BULK_SIZE):
			Applied.objects.bulk_create(record[j:j+BULK_SIZE])


	def importCtaCteP(file):
		record = []
		r = 0
		for line in file:
			# Delete new line character
			line = line.replace('\n', '').replace('\r', '')
			if len(line) > 0:
				data = re.split('\t', line)
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


	def importKilos(file):
		record_deliveries = []
		record_sales = []
		r = 0
		for line in file:
			# Delete new line character
			line = line.replace('\n', '').replace('\r', '')
			if len(line) > 0:
				data = re.split('\t', line)
				print r
				if data[2] == '1':
					record_deliveries.append(
						Deliveries(
							algoritmo_code = evalInt(data[0]),
							name = evalText(data[1]),
							indicator = evalText(data[2]),
							species = evalText(data[3]),
							harvest = evalText(data[4]),
							speciesharvest = evalText(data[3]) + evalText(data[4]),
							species_description = evalText(data[5]),
							field = evalInt(data[6]),
							field_description = evalText(data[7]),
							date = evalDate(data[8]),
							voucher = evalText(data[9]),
							gross_kg = evalInt(data[10]),
							humidity_percentage = evalFloat(data[11]),
							humidity_reduction = evalFloat(data[12]),
							humidity_kg = evalInt(data[13]),
							shaking_reduction = evalFloat(data[14]),
							shaking_kg = evalInt(data[15]),
							volatile_reduction = evalFloat(data[16]),
							volatile_kg = evalInt(data[17]),
							price_per_yard = evalFloat(data[18]),
							driver_code = evalInt(data[19]),
							driver_name = evalText(data[20]),
							factor = evalFloat(data[21]),
							grade = evalInt(data[22]),
							gluten = evalInt(data[23]),
							number_1116A = evalInt(data[24]),
							km = evalInt(data[25]),
							charge_carry = evalText(data[26]),
							external_voucher_code = evalText(data[27]),
							external_voucher_branch = evalInt(data[28]),
							external_voucher_number = evalInt(data[29]),
							aeration_reduction = evalFloat(data[30]),
							aeration_kg = evalInt(data[31]),
							quality_reduction = evalFloat(data[32]),
							quality_kg = evalInt(data[33]),
							zone = evalText(data[34]),
							zone_description = evalText(data[35]),
							plant_code = evalInt(data[36]),
							service_billing_code = evalText(data[37]),
							service_billing_branch = evalInt(data[38]),
							service_billing_number = evalInt(data[39]),
							service_billing_date = evalDate(data[40]),
							service_billing = evalText(data[41]),
							carrier_code = evalInt(data[42]),
							carrier_name = evalText(data[43]),
							exclude_charge_expenses = evalText(data[44]),
							to_date = evalDate(data[45]),
							observations = evalText(data[46]),
							follow_destination = evalText(data[47]),
							destination_code = evalText(data[48]),
							net_weight = evalInt(data[49]),
							tare = evalInt(data[50]),
							gross_weight_recognized = evalInt(data[51]),
							plant_description = evalText(data[52]),
							gross_kg_var = evalInt(data[53]),
							gross_kg_2 = evalInt(data[54]),
							blank_1 = evalText(data[55]),
							blank_2 = evalText(data[56]),
							blank_3 = evalText(data[57]),
							blank_4 = evalText(data[58]),
							allotment = evalText(data[59]),
							allotment_description = evalText(data[60]),
							blank_5 = evalInt(data[61]),
							blank_6 = evalText(data[62]),
							kg_cnv = evalInt(data[63]),
							kg_cnv_2 = evalInt(data[64]),
							kg_cnv_3 = evalInt(data[65]),
							blank_7 = evalText(data[66]),
							blank_8 = evalText(data[67]),
							blank_9 = evalText(data[68]),
							blank_10 = evalText(data[69]),
							gross_kg_3 = evalInt(data[70]),
							unknown_1 = evalInt(data[71]),
							unknown_2 = evalInt(data[72]),
							gross_kg_4 = evalInt(data[73]),
							rate = evalFloat(data[74]),
							net_weight_2 = evalInt(data[75]),
							humidity_kg_2 = evalInt(data[76]),
							blank_11 = evalText(data[77]),
							blank_12 = evalText(data[78]),
							blank_13 = evalText(data[79]),
							blank_14 = evalText(data[80]),
							ctg = evalInt(data[81])
						)
					)
				else:
					record_sales.append(
						Sales(
							algoritmo_code = evalInt(data[0]),
							name = evalText(data[1]),
							indicator = evalText(data[2]),
							species = evalText(data[3]),
							harvest = evalText(data[4]),
							speciesharvest = evalText(data[3]) + evalText(data[4]),
							species_description = evalText(data[5]),
							field = evalInt(data[6]),
							field_description = evalText(data[7]),
							date = evalDate(data[8]),
							voucher = evalText(data[9]),
							gross_kg = evalInt(data[10]),
							humidity_percentage = evalFloat(data[11]),
							humidity_reduction = evalFloat(data[12]),
							humidity_kg = evalInt(data[13]),
							shaking_reduction = evalFloat(data[14]),
							shaking_kg = evalInt(data[15]),
							volatile_reduction = evalFloat(data[16]),
							volatile_kg = evalInt(data[17]),
							price_per_yard = evalFloat(data[18]),
							driver_code = evalInt(data[19]),
							driver_name = evalText(data[20]),
							factor = evalFloat(data[21]),
							grade = evalInt(data[22]),
							gluten = evalInt(data[23]),
							number_1116A = evalInt(data[24]),
							km = evalInt(data[25]),
							charge_carry = evalText(data[26]),
							external_voucher_code = evalText(data[27]),
							external_voucher_branch = evalInt(data[28]),
							external_voucher_number = evalInt(data[29]),
							aeration_reduction = evalFloat(data[30]),
							aeration_kg = evalInt(data[31]),
							quality_reduction = evalFloat(data[32]),
							quality_kg = evalInt(data[33]),
							zone = evalText(data[34]),
							zone_description = evalText(data[35]),
							plant_code = evalInt(data[36]),
							service_billing_code = evalText(data[37]),
							service_billing_branch = evalInt(data[38]),
							service_billing_number = evalInt(data[39]),
							service_billing_date = evalDate(data[40]),
							service_billing = evalText(data[41]),
							carrier_code = evalInt(data[42]),
							carrier_name = evalText(data[43]),
							exclude_charge_expenses = evalText(data[44]),
							to_date = evalDate(data[45]),
							observations = evalText(data[46]),
							follow_destination = evalText(data[47]),
							destination_code = evalText(data[48]),
							net_weight = evalInt(data[49]),
							tare = evalInt(data[50]),
							gross_weight_recognized = evalInt(data[51]),
							plant_description = evalText(data[52]),
							gross_kg_var = evalInt(data[53]),
							gross_kg_2 = evalInt(data[54]),
							blank_1 = evalText(data[55]),
							blank_2 = evalText(data[56]),
							blank_3 = evalText(data[57]),
							blank_4 = evalText(data[58]),
							allotment = evalText(data[59]),
							allotment_description = evalText(data[60]),
							blank_5 = evalInt(data[61]),
							blank_6 = evalText(data[62]),
							kg_cnv = evalInt(data[63]),
							kg_cnv_2 = evalInt(data[64]),
							kg_cnv_3 = evalInt(data[65]),
							blank_7 = evalText(data[66]),
							blank_8 = evalText(data[67]),
							blank_9 = evalText(data[68]),
							blank_10 = evalText(data[69]),
							gross_kg_3 = evalInt(data[70]),
							unknown_1 = evalInt(data[71]),
							unknown_2 = evalInt(data[72]),
							gross_kg_4 = evalInt(data[73]),
							rate = evalFloat(data[74]),
							net_weight_2 = evalInt(data[75]),
							humidity_kg_2 = evalInt(data[76]),
							blank_11 = evalText(data[77]),
							blank_12 = evalText(data[78]),
							blank_13 = evalText(data[79]),
							blank_14 = evalText(data[80]),
							ctg = evalInt(data[81])
						)
					)
			r = r + 1

		# break batch in small batches of 999 objects
		for j in range(0, len(record_deliveries), BULK_SIZE):
			Deliveries.objects.bulk_create(record_deliveries[j:j+BULK_SIZE])

		# break batch in small batches of 999 objects
		for j in range(0, len(record_sales), BULK_SIZE):
			Sales.objects.bulk_create(record_sales[j:j+BULK_SIZE])


	# Read file and delete existing objects
	if datatype == 'ctacte':
		file = os.path.join(settings.BASE_DIR, 'FTP', 'CtaCteP.txt')
		# Check if the file exists before deleteing all objects
		if os.path.isfile(file):
			# Delete all objects if there is 1 or more model objects
			if CtaCte.objects.count() > 0:
				CtaCte.objects.all().delete()
	elif datatype == 'kilos':
		file = os.path.join(settings.BASE_DIR, 'FTP', 'Web.txt')
		if os.path.isfile(file):
			if Deliveries.objects.count() > 0:
				Deliveries.objects.all().delete()
			if Sales.objects.count() > 0:
				Sales.objects.all().delete()
	elif datatype == 'applied':
		file = os.path.join(settings.BASE_DIR, 'FTP', 'APLICADA.txt')
		if os.path.isfile(file):
			if Applied.objects.count() > 0:
				Applied.objects.all().delete()
	elif datatype == 'analysis':
		file = os.path.join(settings.BASE_DIR, 'FTP', 'Analisis.txt')
		if os.path.isfile(file):
			if Analysis.objects.count() > 0:
				Analysis.objects.all().delete()
	elif datatype == 'remittances':
		file = os.path.join(settings.BASE_DIR, 'FTP', 'Remesas.txt')
		if os.path.isfile(file):
			if Remittances.objects.count() > 0:
				Remittances.objects.all().delete()
	else:
		raise Http404()

	with open(file, 'r') as f:
		if datatype == 'ctacte':
			importCtaCteP(f)
		elif datatype == 'kilos':
			importKilos(f)
		elif datatype == 'applied':
			importApplied(f)
		elif datatype == 'analysis':
			importAnalysis(f)
		elif datatype == 'remittances':
			importRemittances(f)

	return render(request, '__ctacte.html')