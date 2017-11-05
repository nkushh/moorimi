from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import UserProfileForm
from .models import UserProfile

# Create your views here.
@login_required(login_url='login')
def get_profile(request):
	user = request.user
	profile = get_object_or_404(UserProfile, user=user)
	context = {
		'user' : user,
		'profile' : profile,
		'page-title' : 'User Profile',
	}

	return render(request, 'user_profile/profile.html', context)


@login_required(login_url='login')
def update_profile(request):
	user = request.user
	profile = get_object_or_404(UserProfile, user=user)

	if request.method=="POST":
		form = UserProfileForm(request.POST, instance=profile)
		if form.is_valid():
			user_profile = form.save(commit=False)
			phone = request.POST['phone_no']

			# Check whether the phone number doesn't start with area code. 
			# If true, format the number to have the area code
			if phone.startswith('0'):
				phone = phone.lstrip('0')
				phone = '+254'+phone
			user_profile.phone_no = phone
			user_profile.last_updated = timezone.now()
			user_profile.save()

			messages.success(request, "Success! Profile details have been updated.")
			return redirect('user_profile:profile')
	else:
		form = UserProfileForm(instance=profile)
		context = {
			'form' : form,
		}
	return render(request, 'user_profile/edit-profile.html', context)

