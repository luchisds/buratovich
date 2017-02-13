from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from website.models import UserInfo
from website.models import CtaCte
from website.models import Notifications
from website.models import ViewedNotifications
from website.models import Currencies
from website.models import Board


class UserInline(admin.StackedInline):
	model = UserInfo
	can_delete = False
	verbose_name = 'Informacion Algoritmo'
	verbose_name_plural = 'Informacion Algoritmo'

class UserAdmin(BaseUserAdmin):
	inlines = (UserInline, )


class CurrenciesAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('date',),
		}),
		('Compra', {
			'fields': (('dn_buy', 'dl_buy'),),
		}),
		('Venta', {
			'fields': (('dn_sell', 'dl_sell'),),
		}),
	)

class BoardAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('date',),
		}),
		('Rosario', {
			'fields': (('wheat_ros', 'wheat12_ros', 'corn_ros', 'sunflower_ros', 'soy_ros', 'sorghum_ros'),),
		}),
		('Buenos Aires', {
			'fields': (('wheat_bas', 'wheat12_bas', 'corn_bas', 'sunflower_bas', 'soy_bas', 'sorghum_bas'),),
		}),
		('Bahia Blanca', {
			'fields': (('wheat_bb', 'wheat12_bb', 'corn_bb', 'sunflower_bb', 'soy_bb', 'sorghum_bb'),),
		}),
		('Quequen', {
			'fields': (('wheat_qq', 'wheat12_qq', 'corn_qq', 'sunflower_qq', 'soy_qq', 'sorghum_qq'),),
		}),
	)


# Unregister models
admin.site.unregister(User)
admin.site.unregister(Group)

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(CtaCte)
admin.site.register(Notifications)
admin.site.register(ViewedNotifications)
admin.site.register(Currencies, CurrenciesAdmin)
admin.site.register(Board, BoardAdmin)