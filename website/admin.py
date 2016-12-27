from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from website.forms import CustomUserCreationForm
# website.forms import CustomUserChangeForm
from website.models import User
from website.models import CtaCte

class UserAdmin(BaseUserAdmin):
	#form = CustomUserChangeForm
	add_form = CustomUserCreationForm

	list_display = ('user', 'password', 'algoritmo_code',)

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(CtaCte)

# Unregister models
admin.site.unregister(Group)