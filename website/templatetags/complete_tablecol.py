from django import template

register = template.Library()

@register.assignment_tag
def complete_tablecol(row_length, total_cols):
	td = ''
	for i in range(row_length, total_cols):
		td += '<td></td>'
	return td