from __future__ import unicode_literals

from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class WebsiteConfig(AppConfig):
	name = 'website'
	verbose_name = _('website')

	def ready(self):
		import website.signals
