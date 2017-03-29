# Signals
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
# User and make password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Email send and errors
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
import smtplib
from django.template.loader import render_to_string

from tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode

from models import AccessLog


# Signal sent after a user is created
@receiver(post_save, sender=User, dispatch_uid='website.signals.postSave_User')
def postSave_User(sender, instance, created, **kwargs):
	if created == True:
		token = account_activation_token.make_token(instance)
		uidb64 = urlsafe_base64_encode(str(instance.pk))

		# Send email
		subject = 'Correo de prueba'
		from_email = 'notificaciones@buratovich.com'

		data = {
			'company_name': instance.userinfo.company_name,
			'username': instance.username,
			'password': instance._pswd,
			'uidb64': uidb64,
			'token': token
		}
		message = render_to_string('email_new_user.html', {'data':data})

		try:
			mail = EmailMessage(subject, message, to=[instance.email], from_email=from_email)
			mail.content_subtype = 'html'
			mail.send()
		except BadHeaderError:
			print 'Invalid header found.'
		except smtplib.SMTPException:
			print 'Error: Unable to send email'


# Signal sent before a user is created
@receiver(pre_save, sender=User, dispatch_uid='website.signals.preSave_User')
def preSave_User(sender, instance, **kwargs):
	# If instance have a 'pk' then is not a new user
	if instance.pk is None:
		# Create a random password 8 char length
		password = User.objects.make_random_password(8)
		instance._pswd = password
		instance.password = make_password(password)
		instance.is_active = False

@receiver(user_logged_in)
def userLogged_In(sender, request, user, **kwargs):
	if not user.is_staff:
		AccessLog.objects.create(user=user, algoritmo_code=user.userinfo.algoritmo_code)