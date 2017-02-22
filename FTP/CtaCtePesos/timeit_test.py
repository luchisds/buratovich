from timeit import timeit
import glob
import os

vouchers = {
	'LC': {'codigo': ['C',], 'separator': ' '},
	'IC': {'codigo': ['C',], 'separator': ' '},
	'LB': {'codigo': ['B',], 'separator': ' '},
	'IB': {'codigo': ['B',], 'separator': ' '},
	'ND': {'codigo': ['HNDCER','HNDE','NDE','NDECAJ','NDECER','NDEPER',], 'separator': '_'},
	'NC': {'codigo': ['HNCCER','HNCR','NCR','NCRCER','NCRDEV','NCSCER',], 'separator': '_'},
	'FC': {'codigo': ['FAC','FACCER','FACD','FACSER','FASCER','HFAC','HFACER',], 'separator': '_'},
}

def search1():
	voucher = 'FC 0013 00004392'
	voucher_list = voucher.split(' ')
	if vouchers.get(voucher_list[0], None) is None:
		return None
	else:
		separator = vouchers[voucher_list[0]]['separator']
		for c in vouchers[voucher_list[0]]['codigo']:
			file_name = c + separator + voucher_list[1] + separator + voucher_list[2] + '.pdf'
			if os.path.isfile(file_name):
				return file_name
			else:
				return None

def search2():
	voucher = 'FC 0013 00004392'
	voucher_list = voucher.split(' ')
	if vouchers.get(voucher_list[0], None) is None:
		return None
	else:
		separator = vouchers[voucher_list[0]]['separator']
		search_text = os.path.join('*' + voucher_list[1] + separator + voucher_list[2] + '.pdf')
		result = glob.glob(search_text)
		if result:
			return result
		else:
			return None

print timeit('search1()', 'from __main__ import search1', number=10000)
print timeit('search2()', 'from __main__ import search2', number=10000)