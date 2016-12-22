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
			# for line in f:
			# 	print re.split('\t+', line)
			line = f.readline()
			line = re.split('\t+', line)

	return render(request, 'ctacte.html', {'line': line})