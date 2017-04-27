from django import template

register = template.Library()

@register.assignment_tag
def voucher(voucher, with_cod):
	voucher = voucher.split(' ')
	cod = voucher[0]
	suc = str(int(voucher[1]))
	nro = str(int(voucher[2]))

	if with_cod == True:
		return cod + ' ' + suc + '-' + nro
	else:
		return suc + '-' + nro