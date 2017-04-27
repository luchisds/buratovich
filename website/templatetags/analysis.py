from django import template

register = template.Library()

@register.assignment_tag
def get_analysis(ticket_analysis, voucher):
	detail = ticket_analysis.get(voucher)
	#print voucher, detail
	return detail