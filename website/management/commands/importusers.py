import csv
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from website.models import UserInfo

class Command(BaseCommand):
	help = 'Import users from csv file'

	def handle(self, *args, **options):
		file = os.path.join(settings.BASE_DIR, 'cuentas.csv')
		with open(file, 'r') as accounts:

			reader = csv.reader(accounts, delimiter=';')
			# First line is header
			reader.next()

			for row in reader:
				cod = row[0]
				name = row[1]
				user = row[2]
				# passw = row[3]
				email = ''
				if passw:
					try:
						passw = User.objects.make_random_password(8)

						user = User.objects.create_user(user, email, passw)
						user.is_staff = False
						user.is_active = False
						user.save()

						userinfo = UserInfo(user_id=user.id)
						userinfo.algoritmo_code = cod
						userinfo.company_name = name
						userinfo.account_confirmed = False
						userinfo.random_password = True
						userinfo.save()
						self.stdout.write(self.style.SUCCESS('Successfully created user "%s"' % name))
					except IntegrityError:
						print name