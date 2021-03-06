from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from user_profile.models import UserProfile
from .forms import UserRegistrationForm, UserUpdateForm

# Create your views here.
@login_required(login_url='login')
def all_accounts(request):
	users = User.objects.all()
	context = {
		'users' : users,
	}
	return render(request, 'authentication/accounts.html', context)

@login_required(login_url='login')
def register_user(request):
	if request.method=='POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email = userObj['email']
			password = userObj['password']

			if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				user = User.objects.create_user(username, email, password)

				# Create a blank profile for the new user
				UserProfile.objects.create(user=user)
				messages.success(request, "Success! Account detail successfully recorded.")
				return redirect('authentication:accounts')
			else:
				messages.warning(request, "Error! Username with that email already exists")
				return redirect('authentication:register_user')

	else:
		form = UserRegistrationForm()
	return render(request, 'authentication/register-user.html', {'form' : form})

def create_account(request):
	if request.method=='POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email = userObj['email']
			password = userObj['password']

			if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				user = User.objects.create_user(username, email, password)

				# Create a blank profile for the new user
				UserProfile.objects.create(user=user)

				messages.success(request, "Success! {} your account was successfully created. Login!".format(username))
				return redirect('login')
			else:
				messages.warning(request, "Error! Username with that email already exists")
				return redirect('authentication:register')

	else:
		form = UserRegistrationForm()
	return render(request, 'authentication/create-account.html', {'form' : form})


@login_required(login_url='login')
def update_account(request):
	account = request.user
	getAcc = get_object_or_404(User, pk=account.pk)
	if request.method=='POST':
		form = UserUpdateForm(request.POST, instance=getAcc)
		if form.is_valid():
			acc = form.save()
			acc.set_password(request.POST['password'])
			update_session_auth_hash(request, account)
			acc.save()

			messages.success(request, "Success! Account detail successfully updated.")
			return redirect('user_profile:profile')

	else:
		form = UserUpdateForm(instance=getAcc)
	return render(request, 'authentication/edit-account.html', {'form' : form})

@login_required(login_url='login')
def deactivate_account(request, account):
	farm = get_object_or_404(User, pk=account)
	farm.is_active = False
	farm.save()
	messages.success(request, 'Account successfully deactivated')
	return redirect('authentication:accounts')

@login_required(login_url='login')
def activate_account(request, account):
	farm = get_object_or_404(User, pk=account)
	farm.is_active = True
	farm.save()
	messages.success(request, 'Account successfully re-activated')
	return redirect('authentication:accounts')


@login_required(login_url='login')
def delete_account(request, account):
	farm = get_object_or_404(User, pk=account)
	farm.delete()
	messages.success(request, 'Account successfully deleted')
	return redirect('authentication:accounts')

