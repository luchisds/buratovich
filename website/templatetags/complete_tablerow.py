from django import template

register = template.Library()

@register.assignment_tag
def complete_tablerow(row_length, total_cols, months):
	tr = ''
	for i in range(row_length, 12):
		tr += '<tr>'
		for j in range(0,total_cols):
			if j == 0:
				tr += '<td>' + months[i] + '</td>'
			else:
				tr += '<td></td>'
		tr += '</tr>'
	return tr