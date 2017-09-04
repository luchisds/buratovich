#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from django.forms import ModelForm
from django import forms

from website.models import UserInfo
#from website.models import CtaCte
from website.models import Notifications
from website.models import ViewedNotifications
from website.models import Currencies
from website.models import Board
from website.models import City
from website.models import Rain
from website.models import RainDetail

from tinymce.widgets import TinyMCE

# Unregister models
admin.site.unregister(User)
admin.site.unregister(Group)


class UserCreateForm(ModelForm):
	username = forms.CharField(required=True, label='Nombre de usuario')
	email = forms.EmailField(required=True, label='Direccion de email')

	class Meta:
		model = User
		fields = ('username', 'email',)


class UserInline(admin.StackedInline):
	model = UserInfo
	can_delete = False
	verbose_name = 'Informacion Algoritmo'
	verbose_name_plural = 'Informacion Algoritmo'
	exclude = ('account_confirmed', 'random_password', 'is_commercial')

	inline_classes = ('grp-collapse grp-open',)


class UserAdmin(BaseUserAdmin):
	inlines = (UserInline, )
	add_form = UserCreateForm

	list_display = ('username', 'email', 'get_company_name', 'get_algoritmo_code', 'get_is_commercial', 'is_active', 'is_staff',)
	empty_value_display = ''

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email',)}
		),
	)

	def get_is_commercial(self, obj):
		return obj.userinfo.is_commercial

	def get_company_name(self, obj):
		return obj.userinfo.company_name

	def get_algoritmo_code(self, obj):
		return obj.userinfo.algoritmo_code

	get_is_commercial.boolean = True
	get_is_commercial.short_description = 'Es Comercial'
	get_company_name.short_description = 'Razón Social'
	get_algoritmo_code.short_description = 'Código Algoritmo'
	get_is_commercial.admin_order_field = 'userinfo__is_commercial'
	get_company_name.admin_order_field = 'userinfo__company_name'
	get_algoritmo_code.admin_order_field = 'userinfo__algoritmo_code'


class CurrenciesAdmin(admin.ModelAdmin):
	list_display = ('date', 'get_dn_buy', 'get_dn_sell', 'get_dl_buy', 'get_dl_sell',)
	empty_value_display = ''
	date_hierarchy = 'date'

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

	def get_dn_buy(self, obj):
		return obj.dn_buy

	def get_dn_sell(self, obj):
		return obj.dn_sell

	def get_dl_buy(self, obj):
		return obj.dl_buy

	def get_dl_sell(self, obj):
		return obj.dl_sell

	get_dn_buy.short_description = 'Nación Compra'
	get_dn_sell.short_description = 'Nación Venta'
	get_dl_buy.short_description = 'Libre Compra'
	get_dl_sell.short_description = 'Libre Venta'
	get_dn_buy.admin_order_field = 'dn_buy'
	get_dn_sell.admin_order_field = 'dn_sell'
	get_dl_buy.admin_order_field = 'dl_buy'
	get_dl_sell.admin_order_field = 'dl_sell'


class BoardAdmin(admin.ModelAdmin):
	list_display = ('date',)
	empty_value_display = ''
	date_hierarchy = 'date'

	fieldsets = (
		(None, {
			'fields': ('date',),
		}),
		('Rosario', {
			'classes': ('species',),
			'fields': (('wheat_ros', 'corn_ros', 'sunflower_ros', 'soy_ros', 'sorghum_ros'),),
		}),
		('Buenos Aires', {
			'classes': ('species',),
			'fields': (('wheat_bas', 'corn_bas', 'sunflower_bas', 'soy_bas', 'sorghum_bas'),),
		}),
		('Bahia Blanca', {
			'classes': ('species',),
			'fields': (('wheat_bb', 'corn_bb', 'sunflower_bb', 'soy_bb', 'sorghum_bb'),),
		}),
		('Quequen', {
			'classes': ('species',),
			'fields': (('wheat_qq', 'corn_qq', 'sunflower_qq', 'soy_qq', 'sorghum_qq'),),
		}),
	)

	class Media:
		css = {
			'all': ('css/board.css',)
		}


class RainDetailInline(admin.StackedInline):
	model = RainDetail
	can_delete = False
	extra = 1
	verbose_name = 'Detalle de Lluvia'
	verbose_name_plural = 'Detalle de Lluvias'

	inline_classes = ('grp-collapse grp-open',)


class RainAdmin(admin.ModelAdmin):
	inlines = (RainDetailInline, )
	date_hierarchy = 'date'


class CityAdmin(admin.ModelAdmin):
	list_display = ('city', 'state',)
	empty_value_display = ''


class NotificationCreateForm(ModelForm):

	class Meta:
		model = Notifications
		fields = ('title', 'notification', 'active', 'date_from', 'date_to',)
		widgets = {
			'notification': TinyMCE(attrs={'cols': 80, 'rows': 30}),
		}


class NotificationsAdmin(admin.ModelAdmin):
	form = NotificationCreateForm
	list_display = ('title', 'notifications_html', 'active', 'date_from', 'date_to',)

	def notifications_html(self, obj):
		return obj.notification

	notifications_html.allow_tags = True


class ViewedNotificationsAdmin(admin.ModelAdmin):
	list_display = ('get_company_name', 'notification',)

	def get_company_name(self, obj):
		return obj.user.userinfo.company_name

	get_company_name.short_description = 'Razón Social'
	get_company_name.admin_order_field = 'user__userinfo__company_name'


# Register models
admin.site.register(User, UserAdmin)
#admin.site.register(CtaCte)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(ViewedNotifications, ViewedNotificationsAdmin)
admin.site.register(Currencies, CurrenciesAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Rain, RainAdmin)
