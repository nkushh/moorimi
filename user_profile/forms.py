from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# Blog app ModelForm
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ("farm_name", "address", "phone_no")
