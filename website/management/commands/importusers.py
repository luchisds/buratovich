#-*- coding: utf-8 -*-

import os
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from website.signals import postSave_User, preSave_User
from website.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode

from website.models import UserInfo


class Command(BaseCommand):
	help = 'Import users from txt file'

	def handle(self, *args, **options):

		# Disconnect signals
		pre_save.disconnect(receiver= preSave_User, sender=User, dispatch_uid='website.signals.preSave_User')
		post_save.disconnect(receiver= postSave_User, sender=User, dispatch_uid='website.signals.postSave_User')

		txt = os.path.join(settings.BASE_DIR, 'cuentas.txt')

		new_accounts = open(os.path.join(settings.BASE_DIR, 'new_accounts.txt'), 'a')
		new_accounts.write('Codigo' + '\t' + 'Nombre' + '\t'+ 'Usuario' + '\t' + 'Email' + '\t' + 'Password' + '\t' + 'Token' + '\t' + 'UID' + '\n')

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
					# Get the first email account
					email = data[5].replace('"', '')
					email = re.split(';', email)
					email = email[0]
					try:
						# User
						passw = User.objects.make_random_password(8)
						print cod, name, user, email, passw
						user = User.objects.create_user(user, email, passw)
						print "user created"
						user.is_staff = False
						user.is_active = False
						user.save()
						print "user saved"

						# UserInfo
						userinfo = UserInfo(user_id=user.id)
						userinfo.algoritmo_code = cod
						userinfo.company_name = name
						userinfo.account_confirmed = False
						userinfo.random_password = True
						userinfo.save()
						print "userinfo created"

						# Token
						token = account_activation_token.make_token(user)
						uidb64 = urlsafe_base64_encode(str(user.pk))

						new_line = cod + '\t' + name + '\t' + user.username + '\t' + email + '\t' + passw + '\t' + token + '\t' + uidb64 + '\n'
						new_accounts.write(new_line)

						self.stdout.write(self.style.SUCCESS('Successfully created user "%s"' % name))
					except IntegrityError:
						print 'Error', name

		new_accounts.close()