from django import template
from django.utils.text import Truncator

register = template.Library()

@register.assignment_tag
def truncate_chars(text, length):
	if len(text) > length:
		# Add 3 for ellipsis addition (...) and get all except last 3 chars
		length += 3
		new_text = Truncator(text).chars(length)[:-3]
		return new_text
	else:
		return text