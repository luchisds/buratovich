from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from website.models import UserInfo
from website.models import CtaCte
from website.models import Notifications
from website.models import NotificationByUser


class UserInline(admin.StackedInline):
	model = UserInfo
	can_delete = False
	verbose_name = 'Informacion Algoritmo'
	verbose_name_plural = 'Informacion Algoritmo'

class UserAdmin(BaseUserAdmin):
	inlines = (UserInline, )


# Unregister models
admin.site.unregister(User)
admin.site.unregister(Group)

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(CtaCte)
admin.site.register(Notifications)
admin.site.register(NotificationByUser)