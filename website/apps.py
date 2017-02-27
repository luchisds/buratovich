# Config file por 'website' app
from __future__ import unicode_literals

from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class WebsiteConfig(AppConfig):
	name = 'website'
	verbose_name = _('website')

	# In ready function import signals to be prepared to be fired since app is loaded
	def ready(self):
		import website.signals
