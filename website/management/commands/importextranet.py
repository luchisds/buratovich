#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from website import import_tasks

class Command(BaseCommand):
	help = 'Import txt data to update extranet'

	def handle(self, *args, **options):
		try:
			import_tasks.importCtaCteP()
			self.stdout.write(self.style.SUCCESS('Successfully updated Cta Cte Pesos'))
		except:
			self.stdout.write(self.style.ERROR('Could not update Cta Cte Pesos'))

		try:
			import_tasks.importApplied()
			self.stdout.write(self.style.SUCCESS('Successfully updated Cta Cte Aplicada'))
		except:
			self.stdout.write(self.style.ERROR('Could not update Cta Cte Aplicada'))

		try:
			import_tasks.importKilos()
			self.stdout.write(self.style.SUCCESS('Successfully updated Cta Cte Kilos'))
		except:
			self.stdout.write(self.style.ERROR('Could not update Cta Cte Kilos'))

		try:
			import_tasks.importTicketsAnalysis()
			self.stdout.write(self.style.SUCCESS('Successfully updated Analisis de Calidad'))
		except:
			self.stdout.write(self.style.ERROR('Could not update Analisis de Calidad'))