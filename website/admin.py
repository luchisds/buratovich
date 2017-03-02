from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from django.forms import ModelForm
from django import forms

from website.models import UserInfo
from website.models import CtaCte
from website.models import Notifications
from website.models import ViewedNotifications
from website.models import Currencies
from website.models import Board
from website.models import City
from website.models import Rain
from website.models import RainDetail


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
	exclude = ('account_confirmed', 'random_password',)


class UserAdmin(BaseUserAdmin):
	inlines = (UserInline, )
	add_form = UserCreateForm
	
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email',)}
		),
	)


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


# class RainForm(ModelForm):
# 	class Meta:
# 		model = RainDetail
# 		fields=('city', 'mm',)
		# error_messages = {
		# 	NON_FIELD_ERRORS: {
		# 		'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
		# 	}
		# }

# 	def clean(self):
# 		cleaned_data = self.cleaned_data

# 		try:
# 			RainDetail.objects.get(city=cleaned_data['city'], rain=cleaned_data['rain'])
# 			print cleaned_data['city'], cleaned_data['rain']
# 		except RainDetail.DoesNotExist:
# 			pass
# 		else:
# 			raise ValidationError('Errorrrrrrrrrrr')

# 		# Always return cleaned_data
# 		return cleaned_data


class RainDetailInline(admin.StackedInline):
	model = RainDetail
	#add_form = RainForm
	can_delete = False
	extra = 1
	verbose_name = 'Detalle de Lluvias'


class RainAdmin(admin.ModelAdmin):
	inlines = (RainDetailInline, )


# Register models
admin.site.register(User, UserAdmin)
admin.site.register(CtaCte)
admin.site.register(Notifications)
admin.site.register(ViewedNotifications)
admin.site.register(Currencies, CurrenciesAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(City)
admin.site.register(Rain, RainAdmin)