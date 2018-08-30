from django import template

register = template.Library()

@register.assignment_tag
def get_analysis(ticket_analysis, voucher):
	return [ticket for ticket in ticket_analysis if ticket['ticket'] == voucher]