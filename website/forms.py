#-*- coding: utf-8 -*-

from datetime import datetime
from django import forms

class CP(forms.Form):

	harvests = ()
	date = datetime.now().year
	for year in range(date-3,date+1):
		harvests += ((str(year)[-2:] + str(year+1)[-2:], str(year)[-2:] + '/' + str(year+1)[-2:]),)

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

	ownership_line = forms.BooleanField()
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
	harvest = forms.ChoiceField(choices=harvests)
	species = forms.ChoiceField(choices=SPECIES)
	species_type = forms.CharField()
