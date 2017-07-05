from django import template

register = template.Library()

@register.assignment_tag
def voucher(voucher, with_cod):

	def getVoucherNumber(vlist, n):
		if n > 2:
			# Suc / Num
			return str(int(voucher[1])) + '-' + str(int(voucher[2]))
		else:
			# Num
			return str(int(voucher[1]))

	voucher = voucher.split(' ')
	cod = voucher[0]
	nro = getVoucherNumber(voucher, len(voucher))

	if with_cod == 'S':
		return cod + ' ' + nro
	elif with_cod == 'N':
		return nro