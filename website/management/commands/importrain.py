#-*- coding: utf-8 -*-

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from website.models import City, Rain, RainDetail

class Command(BaseCommand):
	help = 'Import historic rain from csv file'

	def handle(self, *args, **options):
		file = os.path.join(settings.BASE_DIR, 'lluvias.csv')
		with open(file, 'r') as rain:

			reader = csv.reader(rain, delimiter=';')
			# First line is header
			reader.next()

			for row in reader:
				date = row[2]
				city_cod = row[3]
				mm = row[4].replace(',','.')
				try:
					rain = Rain.objects.create(date=date)
					city = City.objects.get(id=city_cod)
					raindetail = RainDetail.objects.create(rain=rain, city=city, mm=mm)
				except IntegrityError:
					print date, rain

				self.stdout.write(self.style.SUCCESS('Successfully created rain "%s"' % date))