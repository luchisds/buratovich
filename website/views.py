#-*- coding: utf-8 -*-

import math
import os
import re
import datetime
import cStringIO
from io import BytesIO
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
from django.db.models import Sum, Count
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

import django_excel as excel
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
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
from models import TicketsAnalysis
from models import City
from models import Rain
from models import RainDetail
from tokens import account_activation_token
import import_tasks

from bh.settings import RS_USER, RS_PASS

# def email(request):
# 	return render(request, 'email_new_user.html')

def handler404(request):
	return render(request, '404.html')


def handler500(request):
	return render(request, '500.html')


def cp(request):

	def proccess_cp(file, form):

		#CONST
		species_dict = {
			'0000': '------',
			'ALGO': 'Algodón', 
			'AVEN': 'Avena',
			'CART': 'Cártamo',
			'CEBA': 'Cebada',
			'CECE': 'Cebada Cervecera',
			'COLZ': 'Colza',
			'COL0': 'Colza Doble 00',
			'CUAR': 'Cuarta de Cebada',
			'GIRA': 'Girasol',
			'LINO': 'Lino',
			'MAIZ': 'Maíz',
			'MAMA': 'Maíz Mav',
			'MAPI': 'Maíz Pisingallo',
			'MANI': 'Maní',
			'SOJA': 'Soja',
			'SORG': 'Sorgo',
			'TRIG': 'Trigo',
			'TRIC': 'Trigo Candeal',
			'TRIP': 'Trigo Pan',
		}

		harvest_dict = {'0000': '------'}
		date = datetime.datetime.now().year
		for year in range(date-3,date+1):
			harvest_dict[str(year)[-2:] + str(year+1)[-2:]] = str(year)[-2:] + '/' + str(year+1)[-2:]

		# Init InMemory PDF file & canvas
		packet = cStringIO.StringIO()
		can = canvas.Canvas(packet, pagesize=A4)

		# Init fields through form data
		ownership_line = form.get('ownership_line', None)
		if ownership_line:
			ownership_height = 20
		else:
			ownership_height = 0

		destination_load = form.get('destination_load', None)

		species = species_dict.get(form['species'], None)

		harvest = harvest_dict.get(form['harvest'], None)

		fcarga_year = str(datetime.datetime.strptime(form['load_date'], "%Y-%m-%d").date().year)
		fcarga_month = ('0'+str(datetime.datetime.strptime(form['load_date'], "%Y-%m-%d").date().month))[-2:]
		fcarga_day = ('0'+str(datetime.datetime.strptime(form['load_date'], "%Y-%m-%d").date().day))[-2:]

		observations = can.beginText()
		observations.setTextOrigin(400, 459 - ownership_height)
		observations.textLines(form['observations'])

		# Write form fields to canvas
		can.setFont('Helvetica', 12)
		can.drawString(235, 753, form['ctg'])
		can.setFont('Helvetica', 10)
		can.drawString(506, 761, fcarga_day)
		can.drawString(524, 761, fcarga_month)
		can.drawString(541, 761, fcarga_year)
		can.drawString(156, 663 - ownership_height, form['intermediary'])
		can.drawString(156, 643 - ownership_height, form['sender'])
		can.drawString(156, 623 - ownership_height, form['broker'])
		can.drawString(156, 603 - ownership_height, form['representative'])
		can.drawString(156, 583 - ownership_height, form['addressee'])
		can.drawString(156, 563 - ownership_height, form['destination'])
		can.drawString(156, 544 - ownership_height, form['carrier'])
		can.drawString(156, 524 - ownership_height, form['driver'])
		can.drawString(471, 664 - ownership_height, form['intermediary_cuit'])
		can.drawString(471, 644 - ownership_height, form['sender_cuit'])
		can.drawString(471, 624 - ownership_height, form['broker_cuit'])
		can.drawString(471, 604 - ownership_height, form['representative_cuit'])
		can.drawString(471, 584 - ownership_height, form['addressee_cuit'])
		can.drawString(471, 564 - ownership_height, form['destination_cuit'])
		can.drawString(471, 545 - ownership_height, form['carrier_cuit'])
		can.drawString(471, 526 - ownership_height, form['driver_cuit'])
		can.drawString(458, 504 - ownership_height, harvest)
		can.drawString(98, 486 - ownership_height, species.upper())
		can.drawString(266, 486 - ownership_height, form['species_type'])
		can.drawString(458, 487 - ownership_height, form['contract'])
		if destination_load:
			can.drawString(130, 461 - ownership_height, 'X')
		can.drawString(102, 436 - ownership_height, form['estimated_kg'])
		if form['quality'] == 'DECLARACION':
			can.drawString(249, 469 - ownership_height, 'X')
		elif form['quality'] == 'CONFORME':
			can.drawString(249, 452 - ownership_height, 'X')
		else:
			can.drawString(249, 436 - ownership_height, 'X')
		can.drawString(345, 469 - ownership_height, form['gross_kg'])
		can.drawString(345, 452 - ownership_height, form['tare_kg'])
		can.drawString(345, 436 - ownership_height, form['net_kg'])
		can.drawText(observations)
		can.drawString(415, 420 - ownership_height, form['stablishment'])
		can.drawString(415, 403 - ownership_height, form['city'])
		can.drawString(415, 385 - ownership_height, form['state'])
		can.drawString(80, 394 - ownership_height, form['address'])
		can.drawString(415, 349 - ownership_height, form['destination_city'])
		can.drawString(415, 332 - ownership_height, form['destination_state'])
		can.drawString(80, 340 - ownership_height, form['destination_address'])
		can.drawString(345, 311 - ownership_height, form['freight_payer'])
		can.drawString(95, 294 - ownership_height, form['truck'])
		can.drawString(95, 277 - ownership_height, form['trailer'])
		can.drawString(95, 260 - ownership_height, form['km'])
		if form['freight'] == 'PAGADO':
			can.drawString(195, 294 - ownership_height, 'X')
		else:
			can.drawString(277, 294 - ownership_height, 'X')
		can.drawString(242, 277 - ownership_height, form['ref_rate'])
		can.drawString(242, 260 - ownership_height, form['rate'])
		can.save()

		# Move to the beginning of the StringIO buffer
		packet.seek(0)
		new_pdf = PdfFileReader(packet)
		# Get the canvas content
		new_pdf_page = new_pdf.getPage(0)

		existing_pdf = PdfFileReader(file)
		output = PdfFileWriter()
		for numpage in range(0, existing_pdf.getNumPages()):
			page = existing_pdf.getPage(numpage)
			# Merge uploaded PDF page with canvas content
			page.mergePage(new_pdf_page)
			page.compressContentStreams()
			# Save pages to new PDF
			output.addPage(page)

		# Write final PDF to buffer
		output.write(packet)

		# Return buffer stream
		return packet.getvalue()


	if request.method == 'POST':
		form = CP(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['cp']
			cp = proccess_cp(file, request.POST)
			name = file.name
			response = StreamingHttpResponse(cp, content_type='application/pdf')
			# response['Content-Length'] = cp.len
			response['Content-Disposition'] = 'attachment; filename="%s"' % name

			return response
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
	months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
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
				# history[year]['rain'][month] = r['mmsum']
				history[year]['rain'][month] = OrderedDict()
				history[year]['rain'][month]['name'] = months[month-1]
				history[year]['rain'][month]['mm'] = r['mmsum']

				history[year]['total'] += r['mmsum']
				month_avg[month]['sum'] += r['mmsum']
				month_avg[month]['count'] += 1
			else:
				for i in range(prev_month+1, month):
					# history[year]['rain'][datetime.datetime(year,i,1).date().month] = 0
					history[year]['rain'][datetime.datetime(year,i,1).date().month] = OrderedDict()
					history[year]['rain'][datetime.datetime(year,i,1).date().month]['name'] = months[datetime.datetime(year,i,1).date().month - 1]
					history[year]['rain'][datetime.datetime(year,i,1).date().month]['mm'] = 0

					if month_avg.get(datetime.datetime(year,i,1).date().month, None) is None:
						month_avg[datetime.datetime(year,i,1).date().month] = OrderedDict()
						month_avg[datetime.datetime(year,i,1).date().month]['sum'] = 0
						month_avg[datetime.datetime(year,i,1).date().month]['count'] = 0
					month_avg[datetime.datetime(year,i,1).date().month]['count'] += 1
				# history[year]['rain'][month] = r['mmsum']
				history[year]['rain'][month] = OrderedDict()
				history[year]['rain'][month]['name'] = months[month-1]
				history[year]['rain'][month]['mm'] = r['mmsum']

				history[year]['total'] += r['mmsum']
				month_avg[month]['sum'] += r['mmsum']
				month_avg[month]['count'] += 1
		else:
			# history[year]['rain'][month] = r['mmsum']
			history[year]['rain'][month] = OrderedDict()
			history[year]['rain'][month]['name'] = months[month-1]
			history[year]['rain'][month]['mm'] = r['mmsum']

			history[year]['total'] += r['mmsum']
			month_avg[month]['sum'] += r['mmsum']
			month_avg[month]['count'] += 1

		prev_year = year
		prev_month = month

	return render(request, 'historic_rain.html', {'history':history, 'month_avg':month_avg, 'months': months})


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
				if not algoritmo_code.is_commercial:
					# Save algoritmo_code on session if user is not commercial
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
					if not user.userinfo.is_commercial:
						request.session['algoritmo_code'] = request.user.userinfo.algoritmo_code
					return redirect(reverse('extranet'))
				else:
					print 'Usuario no encontrado'
			except:
				print 'No se pudede cambiar el password'
		else:
			return render(request, 'change_password.html', {'account_confirmed': True, 'pass_not_match': True})
	else:
		return render(request, 'change_password.html')


@login_required
def auth_logout(request):
	logout(request)
	return redirect('/')


@login_required
def extranet(request):
	# Notifications list
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

	if request.user.userinfo.is_commercial:
		clients = User.objects.filter(is_staff=False, userinfo__is_commercial=False).values('userinfo__algoritmo_code', 'userinfo__company_name').order_by('userinfo__company_name')
		if request.POST:
			if request.POST.get('client'):
				client_selected = UserInfo.objects.filter(algoritmo_code=request.POST.get('client')).values('algoritmo_code', 'company_name')
				for d in client_selected:
					request.session['algoritmo_code'] = d['algoritmo_code']
					request.session['company_name'] = d['company_name']
				return render(request, 'extranet.html', {'notifications': notifications_list, 'clients': clients})
			else:
				return render(request, 'extranet.html', {'notifications': notifications_list, 'clients': clients, 'errors': 'Debe seleccionar un Cliente'})
		else:
			return render(request, 'extranet.html', {'notifications': notifications_list, 'clients': clients})
	else:
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
def ctacte(request, ctacte_type):

	if ctacte_type <> 'vencimiento' and ctacte_type <> 'emision':
		raise Http404


	#Initialize variables

	vouchers_pdf = ['LC', 'IC', 'LB', 'IB', 'ND', 'NC', 'FC', 'PC', 'OP', 'RE']
	# Dates for print on template
	from_date_print = None
	to_date_print = None
	# Initial balance
	ib = 0
	data = None

	# If exists 'algoritmo_code' variable in session
	if 'algoritmo_code' in request.session:
		# Get dates from request
		from_date = request.GET.get('from')
		to_date = request.GET.get('to')

		if from_date and to_date:
			# Convert date if Firefox or IE --> Input Type="Text" = 'dd/mm/yyyy' --> Input Type="Date" = 'yyyy-mm-dd'
			try:
				d = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
			except ValueError:
				from_date = datetime.datetime.strptime(from_date, '%d/%m/%Y').date()
				to_date = datetime.datetime.strptime(to_date, '%d/%m/%Y').date()
			# Format dates for template
			from_date_print = str(from_date)[-2:]+'/'+str(from_date)[5:7]+'/'+str(from_date)[0:4]
			to_date_print = str(to_date)[-2:]+'/'+str(to_date)[5:7]+'/'+str(to_date)[0:4]
			# Request data

			if ctacte_type == 'vencimiento':
				data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code'], date_1__range=[from_date, to_date]).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_1')
				ib_sum = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code'], date_1__lt=from_date).aggregate(Sum('amount_sign'))
				if ib_sum['amount_sign__sum']:
					ib = ib_sum['amount_sign__sum']
				total_sum = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code'], date_1__lte=to_date).aggregate(Sum('amount_sign'))
			elif ctacte_type == 'emision':
				data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code'], date_2__range=[from_date, to_date]).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_2', 'voucher')
				ib_sum = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code'], date_2__lt=from_date).aggregate(Sum('amount_sign'))
				if ib_sum['amount_sign__sum']:
					ib = ib_sum['amount_sign__sum']
				total_sum = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code'], date_2__lte=to_date).aggregate(Sum('amount_sign'))
		elif not from_date and not to_date:
			if ctacte_type == 'vencimiento':
				data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_1')
			elif ctacte_type == 'emision':
				data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_2', 'voucher')
			total_sum = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).aggregate(Sum('amount_sign'))

		# If exist data
		if data:

			#### Add balance for every record in "data" queryset
			balance = ib
			records = []
			for d in data:
				balance += d['amount_sign']
				tmp_dict = {}
				tmp_dict['obj'] = d
				if d['voucher'].split(' ')[0] in vouchers_pdf:
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
			# Add initial balance
			initial_balance.append(ib)
			page_balance = []
			while ib_records < total_records:
				if ib_records == 0 and remainder > 0:
					tmp = records[0:remainder]
					ib_records += remainder
				else:
					tmp = records[0:ib_records+limit]
					ib_records += limit

				# Assign inicial balance to partial_balance (if there is no date filter will be 0, otherwise will be the initial balance at from date)
				partial_balance = ib
				for obj in tmp:
					partial_balance += obj['obj']['amount_sign']

				initial_balance.append(partial_balance)

			# Scroll the list from first item to last-1 (is the cta cte total amount)
			for n in range(0,len(initial_balance)-1):
				tmp_dict = {}
				tmp_dict['page'] = len(initial_balance)-1-n
				tmp_dict['balance'] = initial_balance[n]
				page_balance.append(tmp_dict)


			return render(request, 'ctacte.html', {'ctacte': ctacte, 'total_sum': total_sum, 'page_balance': page_balance, 'from_date': from_date_print, 'to_date': to_date_print, 'ctacte_type':ctacte_type})
		else:
			if (from_date and to_date and from_date < to_date) or (not from_date and not to_date):
				return render(request, 'ctacte.html', {'from_date': from_date_print, 'to_date': to_date_print, 'ctacte_type':ctacte_type})
			else:
				return render(request, 'ctacte.html', {'from_date': from_date_print, 'to_date': to_date_print, 'error': 'Rango inválido de fechas', 'ctacte_type':ctacte_type})
	else:
		return render(request, 'ctacte.html', {'ctacte_type':ctacte_type})


@login_required
def applied(request):

	#Initialize variables

	# Dates for print on template
	from_date_print = None
	to_date_print = None
	# Initial balance
	ib = 0
	data = None

	# If exists 'algoritmo_code' variable in session
	if 'algoritmo_code' in request.session:
		# Get dates from request
		from_date = request.GET.get('from')
		to_date = request.GET.get('to')

		if from_date and to_date:
			# Convert date if Firefox or IE --> Input Type="Text" = 'dd/mm/yyyy' --> Input Type="Date" = 'yyyy-mm-dd'
			try:
				d = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
			except ValueError:
				from_date = datetime.datetime.strptime(from_date, '%d/%m/%Y').date()
				to_date = datetime.datetime.strptime(to_date, '%d/%m/%Y').date()
			# Format dates for template
			from_date_print = str(from_date)[-2:]+'/'+str(from_date)[5:7]+'/'+str(from_date)[0:4]
			to_date_print = str(to_date)[-2:]+'/'+str(to_date)[5:7]+'/'+str(to_date)[0:4]
			# Request data
			data = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code'], expiration_date__range=[from_date, to_date]).values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('expiration_date')
			ib_sum = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code'], expiration_date__lte=from_date).aggregate(Sum('amount_sign'))
			if ib_sum['amount_sign__sum']:
				ib = ib_sum['amount_sign__sum']
			total_sum = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code'], expiration_date__lte=to_date).aggregate(Sum('amount_sign'))
		elif not from_date and not to_date:
			data = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('expiration_date')
			total_sum = Applied.objects.filter(algoritmo_code=request.session['algoritmo_code']).aggregate(Sum('amount_sign'))

		# If exist data
		if data:

			#### Add balance for every record in "data" queryset
			balance = ib
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
			# Add initial balance
			initial_balance.append(ib)
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

			return render(request, 'applied.html', {'applied': applied_ctacte, 'total_sum': total_sum, 'page_balance': page_balance, 'from_date': from_date_print, 'to_date': to_date_print})
		else:
			if (from_date and to_date and from_date < to_date) or (not from_date and not to_date):
				return render(request, 'applied.html', {'from_date': from_date_print, 'to_date': to_date_print})
			else:
				return render(request, 'applied.html', {'from_date': from_date_print, 'to_date': to_date_print, 'error': 'Rango inválido de fechas'})
	else:
		return render(request, 'applied.html')


@login_required
def deliveries(request):
	if 'algoritmo_code' in request.session:

		if request.GET.get('checks'):
			current_species = request.GET.getlist('checks')
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

			if current_species:
				# Create a filter by species / harvest using Q function and OR statement (|)
				speciesharvest_filter = Q()
				for item in current_species:
					speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=item)

				## Total kg for selected species_description
				total_kg = Deliveries.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).aggregate(Sum('net_weight'), Count('voucher'), Sum('humidity_kg'), Sum('shaking_kg'), Sum('volatile_kg'), Sum('gross_kg'))

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

				# Get ticket analysis
				remittances = TicketsAnalysis.objects.filter(ticket__in = tickets_for_analysis).values('ticket').distinct()
				# dict [Ticket] --> [Analysis]
				ticket_analysis = {}
				for i in remittances:
					analysis = TicketsAnalysis.objects.filter(ticket = i['ticket']).values('analysis_costs', 'gluten', 'analysis_item', 'percentage', 'bonus', 'reduction', 'item_descripcion').order_by('item_descripcion')
					ticket_analysis[i['ticket']] = analysis

				return render(request, 'deliveries.html', {'species':species_by_harvest, 'tickets':tickets_by_field, 'total': total_kg, 'ticket_analysis': ticket_analysis})
			else:
				# If no species selected
				return render(request, 'deliveries.html', {'species':species_by_harvest})
		else:
			return render(request, 'deliveries.html')
	else:
		return render(request, 'deliveries.html')


@login_required
def sales(request):

	if 'algoritmo_code' in request.session:

		# PDF files
		vouchers_pdf = ['VT', 'VF']

		if request.GET.get('checks'):
			current_species = request.GET.getlist('checks')
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

			if current_species:
				# Create a filter by species / harvest using Q function and OR statement (|)
				speciesharvest_filter = Q()
				for item in current_species:
					speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=item)

				## Total kg for selected species_description
				total_kg = {}
				total_kg['sales'] = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code'], indicator='2').filter(speciesharvest_filter).aggregate(Sum('net_weight'))
				total_kg['to_set'] = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code'], indicator='2B').filter(speciesharvest_filter).aggregate(Sum('net_weight'))
				total_kg['other'] = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code'], indicator='3').filter(speciesharvest_filter).aggregate(Sum('net_weight'))
				total_kg['settled'] = Sales.objects.filter(algoritmo_code=request.session['algoritmo_code']).filter(speciesharvest_filter).aggregate(Sum('number_1116A'))


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
										sales[sd]['sales']['vouchers'][v['id']] = OrderedDict()
										sales[sd]['sales']['vouchers'][v['id']]['obj'] = v
										if v['voucher'].split(' ')[0] in vouchers_pdf:
											sales[sd]['sales']['vouchers'][v['id']]['file'] = v['voucher']
										else:
											sales[sd]['sales']['vouchers'][v['id']]['file'] = None
										total_g_sales += v['gross_kg']
										total_p_sales += v['service_billing_number']
										total_l_sales += v['number_1116A']
										count_sales += 1
									elif v['indicator'] == '2B':
										if sales[sd].get('to_set', None) is None:
											sales[sd]['to_set'] = OrderedDict()
											sales[sd]['to_set']['vouchers'] = OrderedDict()
										# sales[sd]['to_set']['vouchers'][v['voucher']] = v
										sales[sd]['to_set']['vouchers'][v['id']] = OrderedDict()
										sales[sd]['to_set']['vouchers'][v['id']]['obj'] = v
										if v['voucher'].split(' ')[0] in vouchers_pdf:
											sales[sd]['to_set']['vouchers'][v['id']]['file'] = v['voucher']
										else:
											sales[sd]['to_set']['vouchers'][v['id']]['file'] = None
										total_g_to_set += v['gross_kg']
										count_to_set += 1
									else:
										if sales[sd].get('others', None) is None:
											sales[sd]['others'] = OrderedDict()
											sales[sd]['others']['vouchers'] = OrderedDict()
										# sales[sd]['others']['vouchers'][v['voucher']] = v
										sales[sd]['others']['vouchers'][v['id']] = OrderedDict()
										sales[sd]['others']['vouchers'][v['id']]['obj'] = v
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
										#print count_to_set
										#print total_g_to_set
										sales[sd]['to_set']['total_g_to_set'] = total_g_to_set
										sales[sd]['to_set']['count_to_set'] = count_to_set
									if sales[sd].get('others', None) <> None:
										sales[sd]['others']['total_i_others'] = total_i_others
										sales[sd]['others']['total_o_others'] = total_o_others
										sales[sd]['others']['count_others'] = count_others

				return render(request, 'sales.html', {'species':species_by_harvest, 'total':total_kg, 'sales':sales})
			else:
				# Ifno species selected
				return render(request, 'sales.html', {'species':species_by_harvest})
		else:
			return render(request, 'sales.html')
	else:
		return render(request, 'sales.html')


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
		'PC': {'codigo': ['PC',], 'separator': '_', 'url':'tesoreria/'},
		'OP': {'codigo': ['OP',], 'separator': '_', 'url':'tesoreria/'},
		'RE': {'codigo': ['RE',], 'separator': '_', 'url':'tesoreria/'},
		'VT': {'codigo': ['VT',], 'separator': '_', 'url':'cnv/'},
		'VF': {'codigo': ['VF',], 'separator': '_', 'url':'cnv/'},
	}

	def merge_pdf(file1, file2):
		
		def append_pdf(input,output):
			[output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

		# Create instance por Write new PDF
		output = PdfFileWriter()
		pdf1 = PdfFileReader(cStringIO.StringIO(file1))
		pdf2 = PdfFileReader(cStringIO.StringIO(file2))
		append_pdf(pdf1,output)
		append_pdf(pdf2,output)
		# Init InMemory PDF file
		new_file = cStringIO.StringIO()

		# Write PDF to buffer
		output.write(new_file)

		# Return buffer stream
		return new_file.getvalue()

	def search_file(voucher, voucher_date):
		voucher = voucher.split(' ')
		if vouchers.get(voucher[0], None) is None:
			return None
		else:
			separator = vouchers[voucher[0]]['separator']
			url = vouchers[voucher[0]]['url']

			for c in vouchers[voucher[0]]['codigo']:
				file_name = c+separator+voucher[1]+separator+voucher[2]+'.pdf'

				if 'tesoreria' in url:
					file_url = 'http://190.92.102.226:1500/'+url+voucher_date+'/C'+str(request.session['algoritmo_code'])+separator+file_name
				else:
					file_url = 'http://190.92.102.226:1500/'+url+file_name
				
				r = requests.get(file_url, auth=HTTPBasicAuth(RS_USER, RS_PASS))
				if r.status_code == 200:
					##### FASCER Tickets Detail
					if c == 'FASCER':
						tickets_file_url = 'http://190.92.102.226:1500/'+'DETTK'+separator+voucher[1]+separator+voucher[2]+'.pdf'
						rtk = requests.get(tickets_file_url, auth=HTTPBasicAuth(RS_USER, RS_PASS))
						if rtk.status_code == 200:
							r = merge_pdf(r.content, rtk.content)
							# If DETTK exists then return the new file
							return {'file':r, 'filename':file_name}
					#####

					# If voucher is not FASCER or there is no DETTK then return the response content (file)
					return {'file':r.content, 'filename':file_name}

	if 'algoritmo_code' in request.session:
		f = request.GET['f']
		d = request.GET['d']
		file = search_file(f, d)

		if file:
			#length = file['file'].headers['Content-Length']
			response = StreamingHttpResponse(file['file'], content_type='application/pdf')
			#response['Content-Length'] = length
			response['Content-Disposition'] = "attachment; filename='%s'" % file['filename']
			return response
		else:
			raise Http404


@login_required
def downloadexcel(request, module):

	def getPesosExcel():
		data = CtaCte.objects.filter(algoritmo_code=request.session['algoritmo_code']).values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign').order_by('date_1')

		balance = 0
		records = []
		for d in data:
			balance += d['amount_sign']
			tmp_dict = OrderedDict()
			tmp_dict['Fecha Vencimiento'] = d['date_2']
			tmp_dict['Comprobante'] = d['voucher']
			tmp_dict['Observaciones'] = d['concept']
			tmp_dict['Fecha Emision'] = d['date_1']
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

	if datatype == 'ctacte':
		import_tasks.importCtaCteP()
	elif datatype == 'kilos':
		import_tasks.importKilos()
	elif datatype == 'applied':
		import_tasks.importApplied()
	elif datatype == 'analysis':
		import_tasks.importTicketsAnalysis()
	elif datatype == 'all':
		import_tasks.importCtaCteP()
		import_tasks.importKilos()
		import_tasks.importApplied()
		import_tasks.importTicketsAnalysis()
	else:
		raise Http404()

	return render(request, 'update_extranet.html')