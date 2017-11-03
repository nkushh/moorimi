from django.contrib import admin
from .models import UserProfile

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'farm_name', 'address', 'phone_no']

admin.site.register(UserProfile, UserProfileAdmin)
