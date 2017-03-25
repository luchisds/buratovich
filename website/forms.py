#-*- coding: utf-8 -*-

from datetime import datetime
from django import forms

class CP(forms.Form):

	harvest_list = ()
	date = datetime.now().year
	for year in range(date-3,date+1):
		harvest_list += ((str(year)[-2:] + str(year+1)[-2:], str(year)[-2:] + '/' + str(year+1)[-2:]),)

	SPECIES = (
			('ALGO', 'Algodón'), 
			('AVEN', 'Avena'),
			('CART', 'Cártamo'),
			('CEBA', 'Cebada'),
			('CECE', 'Cebada Cervecera'),
			('COLZ', 'Colza'),
			('COL0', 'Colza Doble 00'),
			('CUAR', 'Cuarta de Cebada'),
			('GIRA', 'Girasol'),
			('LINO', 'Lino'),
			('MAIZ', 'Maíz'),
			('MAMA', 'Maíz Mav'),
			('MAPI', 'Maíz Pisingallo'),
			('MANI', 'Maní'),
			('SOJA', 'Soja'),
			('SORG', 'Sorgo'),
			('TRIG', 'Trigo'),
			('TRIC', 'Trigo Candeal'),
			('TRIP', 'Trigo Pan'),
			('OTRO', 'Otro...'),
	)

	QUALITY = (
		('DECLARACION', 'Declaración de Calidad'),
		('CONFORME', 'Conforme'),
		('CONDICIONAL', 'Condicional'),
	)

	FREIGHT = (
		('PAGADO', 'Flete Pagado'),
		('APAGAR', 'Flete A Pagar'),
	)

	ownership_line = forms.BooleanField(label='Marcar si el Titular contiene 2 lineas')
	load_date = forms.DateField()
	ctg = forms.CharField()
	intermediary = forms.CharField()
	intermediary_cuit = forms.CharField()
	sender = forms.CharField()
	sender_cuit = forms.CharField()
	broker = forms.CharField()
	broker_cuit = forms.CharField()
	representative = forms.CharField()
	representative_cuit = forms.CharField()
	addressee = forms.CharField()
	addressee_cuit = forms.CharField()
	destination = forms.CharField()
	destination_cuit = forms.CharField()
	carrier = forms.CharField()
	carrier_cuit = forms.CharField()
	driver = forms.CharField()
	driver_cuit = forms.CharField()
	harvest = forms.ChoiceField(choices=harvest_list)
	species = forms.ChoiceField(choices=SPECIES)
	species_type = forms.CharField()
	contract = forms.CharField()
	destination_load = forms.BooleanField()
	estimated_kg = forms.CharField()
	quality = forms.ChoiceField(choices=QUALITY, widget=forms.RadioSelect)
	gross_kg = forms.CharField()
	tare_kg = forms.CharField()
	net_kg = forms.CharField()
	observations = forms.CharField(widget=forms.Textarea)
	stablishment = forms.CharField()
	address = forms.CharField()
	city = forms.CharField()
	state = forms.CharField()
	destination_address = forms.CharField()
	destination_city = forms.CharField()
	destination_state = forms.CharField()
	freight_payer = forms.CharField()
	truck = forms.CharField()
	trailer = forms.CharField()
	km = forms.CharField()
	freight = forms.ChoiceField(choices=FREIGHT, widget=forms.RadioSelect)
	ref_rate = forms.CharField()
	rate = forms.CharField()
	cp = forms.FileField()