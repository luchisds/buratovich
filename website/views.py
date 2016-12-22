from django.shortcuts import render

def index(request):
	return render(request, 'index.html')


def company(request):
	return render(request, 'company.html')


def contact(request):
	return render(request, 'contact.html')


def ctacte(request):
	f = open('CtaCteP.TXT', 'r')
	file = f.read()
	print file

	return render(request, 'ctacte.html', {'file':file})