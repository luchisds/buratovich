from django import template

register = template.Library()

@register.assignment_tag
def get_analysis(ticket_analysis, analysis_detail, voucher):
	analysis = ticket_analysis.get(voucher)
	detail = analysis_detail.get(analysis)
	return detail