from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.db.models.signals import pre_save

from django.dispatch import receiver


@receiver(post_save, sender=User, dispatch_uid='website.signals.postSave_User')
def postSave_User(sender, instance, **kwargs):
	print "usuario ya creado"


@receiver(pre_save, sender=User, dispatch_uid='website.signals.preSave_User')
def preSave_User(sender, instance, **kwargs):
	if not instance.pk:
		password = User.objects.make_random_password(8)
		print password
		instance.password = make_password(password)