from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from models import User

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('algoritmo_code',)


# class CustomUserChangeForm(UserChangeForm):

# 	class Meta(UserChangeForm.Meta):
# 		model = User
# 		fields = UserChangeForm.Meta.fields + ('algoritmo_code',)