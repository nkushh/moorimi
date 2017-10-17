from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(forms.Form):
	username = forms.CharField(required=True, label='Username', max_length=32)
	email = forms.EmailField(required=True, label='Email', max_length=200)
	password = forms.CharField(required=True, label='Password', max_length=32, widget=forms.PasswordInput())

class CustomAuthenticationForm(AuthenticationForm):
	def confirm_login_allowed(self, user):
		if not user.is_active or not user.is_validated:
			messages.warning(request, 'Account credentials not valid.')
