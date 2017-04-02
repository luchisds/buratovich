#-*- coding: utf-8 -*-

import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Email send and errors
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
import smtplib
from django.template.loader import render_to_string


class Command(BaseCommand):
	help = 'Send account activation email'

	def handle(self, *args, **options):

		txt = os.path.join(settings.BASE_DIR, 'new_accounts.txt')

		with open(txt, 'r') as accounts:

			# Exclude header
			accounts.next()

			for line in accounts:
				# Delete new line character
				line = line.replace('\n', '').replace('\r', '')
				if len(line) > 0:
					data = re.split('\t', line)
					cod = data[0]
					name = data[1]
					user = data[2]
					email = data[3]
					passw = data[4]
					token = data[5]
					uid = data[6]

					# Send email
					subject = 'Activación de Cuenta | Buratovich Hnos.'
					from_email = 'notificaciones@buratovich.com'

					data = {
						'company_name': name,
						'username': user,
						'password': passw,
						'uidb64': uid,
						'token': token
					}
					message = render_to_string('email_new_user.html', {'data':data})

					try:
						mail = EmailMessage(subject, message, to=[email], from_email=from_email)
						mail.content_subtype = 'html'
						mail.send()
						self.stdout.write(self.style.SUCCESS('Successfully sent email "%s"' % name))
					except BadHeaderError:
						self.stdout.write(self.style.ERROR('Invalid header found "%s"' % name))
					except smtplib.SMTPException:
						self.stdout.write(self.style.ERROR('Error: Unable to send email "%s"' % name))