import csv
from django.contrib.auth.models import User
from auth.models import UserProfile
from website.models import UserInfo
from django.db import IntegrityError

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	help = 'Import users from csv file'

	def handle(self, *args, **options):
		members = open('eclub_data.csv', "rU")
		data = csv.DictReader(members)
		default_password = 'tsc_eclub'

		for row in data:
			email = row['Email']
			if email_re.match(email):
				tokens = email.split('@')
				username = tokens[0]  
				try:
					user = User.objects.create_user(username, email, default_password)
					user.is_staff = False
					user.save()
					profile = UserProfile(user_id=user.id)
					profile.save()
					self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
				except IntegrityError:
					print username