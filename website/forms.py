#-*- coding: utf-8 -*-

from datetime import datetime
from django import forms
from django.core.validators import DecimalValidator, RegexValidator

# Widget for input type date
class DateInput(forms.DateInput):
	input_type = 'date'

class CP(forms.Form):

	harvest_list = (('0000', '------'),)
	date = datetime.now().year
	for year in range(date-3,date+1):
		harvest_list += ((str(year)[-2:] + str(year+1)[-2:], str(year)[-2:] + '/' + str(year+1)[-2:]),)

	SPECIES = (
			('0000', '------'),
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
			#('OTRO', 'Otro...'),
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

	numeric = RegexValidator(r'^[0-9]*$', 'Solo se permiten numeros')

	ownership_line = forms.BooleanField(label='Titular Carta de Porte')
	load_date = forms.DateField(label='Fecha de Carga', widget=DateInput)
	ctg = forms.CharField(label='C.T.G. Nro.', max_length=8, strip=True, validators=[numeric])
	intermediary = forms.CharField(label='Intermediario', max_length=45, strip=True)
	intermediary_cuit = forms.CharField(label='CUIT', max_length=11, strip=True)
	sender = forms.CharField(label='Remitente Comercial', max_length=45, strip=True)
	sender_cuit = forms.CharField(label='CUIT', max_length=11, strip=True)
	broker = forms.CharField(label='Corredor', max_length=45, strip=True)
	broker_cuit = forms.CharField(label='CUIT', max_length=11, strip=True)
	representative = forms.CharField(label='Entregador', max_length=45, strip=True)
	representative_cuit = forms.CharField(label='CUIT', max_length=11, strip=True)
	addressee = forms.CharField(label='Destinatario', max_length=45, strip=True)
	addressee_cuit = forms.CharField(label='CUIT', max_length=11, strip=True)
	destination = forms.CharField(label='Destino', max_length=45, strip=True)
	destination_cuit = forms.CharField(label='CUIT', max_length=11, strip=True)
	carrier = forms.CharField(label='Transportista', max_length=45, strip=True)
	carrier_cuit = forms.CharField(label='CUIT', max_length=11, strip=True)
	driver = forms.CharField(label='Chofer', max_length=45, strip=True)
	driver_cuit = forms.CharField(label='CUIT/CUIL', max_length=11, strip=True)
	harvest = forms.ChoiceField(label='Cosecha', choices=harvest_list)
	species = forms.ChoiceField(label='Grano/Especie', choices=SPECIES)
	species_type = forms.CharField(label='Tipo', max_length=18, strip=True)
	contract = forms.CharField(label='Contrato Nro.', max_length=17, strip=True)
	destination_load = forms.BooleanField(label='Peso en destino?')
	estimated_kg = forms.CharField(label='Kilos Estimados', max_length=7, strip=True)
	quality = forms.ChoiceField(label='Calidad', choices=QUALITY, widget=forms.RadioSelect)
	gross_kg = forms.CharField(label='Peso Bruto (Kgrs.)', max_length=7, strip=True)
	tare_kg = forms.CharField(label='Peso Tara (Kgrs.)', max_length=7, strip=True)
	net_kg = forms.CharField(label='Peso Neto (Kgrs.)', max_length=7, strip=True)
	observations = forms.CharField(label='Observaciones', widget=forms.Textarea)
	stablishment = forms.CharField(label='Establecimiento', max_length=23, strip=True)
	address = forms.CharField(label='Dirección', max_length=45, strip=True)
	city = forms.CharField(label='Localidad', max_length=23, strip=True)
	state = forms.CharField(label='Provincia', max_length=23, strip=True)
	destination_address = forms.CharField(label='Dirección', max_length=45, strip=True)
	destination_city = forms.CharField(label='Localidad', max_length=23, strip=True)
	destination_state = forms.CharField(label='Provincia', max_length=23, strip=True)
	freight_payer = forms.CharField(label='Pagador del Flete', max_length=39, strip=True)
	truck = forms.CharField(label='Camión', max_length=7, strip=True)
	trailer = forms.CharField(label='Acoplado', max_length=7, strip=True)
	km = forms.CharField(label='Km a recorrer', max_length=4, strip=True)
	freight = forms.ChoiceField(label='Flete', choices=FREIGHT, widget=forms.RadioSelect)
	ref_rate = forms.CharField(label='Tarifa de Referencia', max_length=7, strip=True)
	rate = forms.CharField(label='Tarifa', max_length=7, strip=True)
	cp = forms.FileField(label='Carta de Porte')