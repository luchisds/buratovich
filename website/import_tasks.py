#-*- coding: utf-8 -*-

import codecs
import datetime
import os
import re

from django.conf import settings

# from django.db import connection

from models import TicketsAnalysis
from models import CtaCte
from models import Deliveries
from models import Sales
from models import Applied


# bulk_create have a limit of 999 objects per batch for SQLite
BULK_SIZE = 999

def evalDate(date):
	# Catch format error in date
	try:
		return datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
	except ValueError:
		return None

def evalDateHour(date):
	try:
		return datetime.datetime.strptime(date, "%d/%m/%Y %I:%M:%S %p").strftime("%Y-%m-%d")
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

def evalTextUTF8(text):
	return unicode(text.strip(' ').decode('utf-8'))


def importTicketsAnalysis():
	txt = os.path.join(settings.EXTRANET_DIR, 'Analisis_Tickets.txt')
	try:
		with open(txt, 'r') as file:
			if TicketsAnalysis.objects.count() > 0:
				TicketsAnalysis.objects.all().delete()
			record = []
			r = 0
			# Exclude header
			file.next()
			for line in file:
				# Delete new line character
				line = line.replace('\n', '').replace('\r', '')
				if len(line) > 0:
					data = re.split('\t', line)
					# print r
					record.append(
						TicketsAnalysis(
							entry_point = evalInt(data[0]),
							entry_number = evalInt(data[1]),
							entry_point_ticket = evalInt(data[2]),
							ticket_number = evalInt(data[3]),
							ticket_date = evalDateHour(data[4]),
							ticket = 'TK ' + evalText(data[5]),
							field = evalInt(data[6]),
							lot = evalText(data[7]),
							field_description = evalText(data[8]),
							species = evalText(data[9]),
							harvest = evalText(data[10]),
							grade = evalInt(data[11]),
							factor = evalFloat(data[12]),
							analysis_costs = evalFloat(data[13]),
							gluten = evalInt(data[14]),
							analysis_item = evalInt(data[15]),
							percentage = evalFloat(data[16]),
							bonus = evalFloat(data[17]),
							reduction = evalFloat(data[18]),
							item_descripcion = evalTextUTF8(data[19])
						)
					)
				r = r + 1

			# break batch in small batches of 999 objects
			for j in range(0, len(record), BULK_SIZE):
				TicketsAnalysis.objects.bulk_create(record[j:j+BULK_SIZE])

	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)


def importApplied():
	txt = os.path.join(settings.EXTRANET_DIR, 'Aplicada.TXT')
	try:
		with open(txt, 'r') as file:
			if Applied.objects.count() > 0:
				Applied.objects.all().delete()
			record = []
			r = 0
			for line in file:
				# Delete new line character
				line = line.replace('\n', '').replace('\r', '')
				if len(line) > 0:
					data = re.split('\t', line)
					#print r
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

	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)


def importCtaCteP():
	txt = os.path.join(settings.EXTRANET_DIR, 'CtaCteP.TXT')
	try:
		with open(txt, 'r') as file:
			if CtaCte.objects.count() > 0:
				CtaCte.objects.all().delete()
			record = []
			r = 0
			for line in file:
				# Delete new line character
				line = line.replace('\n', '').replace('\r', '')
				if len(line) > 0:
					data = re.split('\t', line)
					#print r
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

	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)


def importKilos():
	txt = os.path.join(settings.EXTRANET_DIR, 'Web.TXT')
	try:
		with open(txt, 'r') as file:
			if Deliveries.objects.count() > 0:
				Deliveries.objects.all().delete()
			if Sales.objects.count() > 0:
				Sales.objects.all().delete()
			record_deliveries = []
			record_sales = []
			r = 0
			for line in file:
				# Delete new line character
				line = line.replace('\n', '').replace('\r', '')
				if len(line) > 0:
					data = re.split('\t', line)
					#print r
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

	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
