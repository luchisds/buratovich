# Signals
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



# Signal sent after a user is created
@receiver(post_save, sender=User, dispatch_uid='website.signals.postSave_User')
def postSave_User(sender, instance, **kwargs):
	token = account_activation_token.make_token(instance)
	uidb64 = urlsafe_base64_encode(str(instance.pk))
	if token:
		print uidb64
		print token
	else:
		'No se genero token'

	# Send email
	subject = 'Correo de prueba'
	from_email = 'notificaciones@buratovich.com'

	data = {
		'username': instance.username,
		'password': instance.password,
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
	if not instance.pk:
		# Create a random password 8 char length
		password = User.objects.make_random_password(8)
		instance.password = make_password(password)
		instance.is_active = False