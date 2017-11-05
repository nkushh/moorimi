from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404, redirect

from .models import Breed, Breeding, Heat_records
from dairy.models import Cattle
import datetime, calendar

# Create your views here.
def cattle_to_serve(request, pk):
	record = get_object_or_404(Heat_records, pk=pk)
	breeds = Breed.objects.all()

	context = {
		'record' : record,
		'breeds' : breeds,
	}

	return render(request, "breeding/serve.html", context)



def served_cattle(request):
	account = request.user

	cattle = Breeding.objects.filter(account=account, birth_status=0).order_by('-delivery_due')
	cows = Heat_records.objects.filter(account=account, heat_status=0)
	breeds = Breed.objects.all()

	page = request.GET.get('page', 1)

	paginator = Paginator(cattle, 10)

	try:
		cattle = paginator.page(page)
	except PageNotAnInteger:
		cattle = paginator.page(1)
	except EmptyPage:
		cattle = paginator.page(paginator.num_pages)

	context = {
		'breeds' : breeds,
		'cattle' : cattle,
		'cows' : cows,
	}

	return render(request, "breeding/served-cattle.html", context)


def serve_cattle(request):
	account = request.user
	if request.method=="POST":
		cattle = get_object_or_404(Cattle, pk=request.POST['cattle']) 
		method = request.POST['method']
		sire = request.POST['sire']
		breed = get_object_or_404(Breed, pk=request.POST['breed']) 
		date_served = datetime.datetime.strptime(request.POST['date_served'], '%Y-%m-%d')
		delivery_due = date_served + datetime.timedelta(days=283)

		# Set cattle stage to expectant
		cattle.stage = "Expectant"
		cattle.save()

		# Update the heat record for the animal to show it has been served
		heat_record = get_object_or_404(Heat_records, cattle=cattle)
		heat_record.heat_status = 1
		heat_record.save()

		# Insert breeding exercise records into the database
		record = Breeding(account=account, cattle=cattle, method=method, sire=sire, breed=breed, date_served=date_served, delivery_due=delivery_due).save()
		messages.success(request, "Success! {} breeding exercise was recorded.".format(cattle.name))
		return redirect('breeding:served_cattle')
	else:
		return redirect('breeding:served_cattle')


def cattle_onheat(request):
	account = request.user
	cattle = Heat_records.objects.filter(account=account, heat_status=0).order_by('-date_noted')
	cows = Cattle.objects.all()

	page = request.GET.get('page', 1)

	paginator = Paginator(cattle, 10)

	try:
		cattle = paginator.page(page)
	except PageNotAnInteger:
		cattle = paginator.page(1)
	except EmptyPage:
		cattle = paginator.page(paginator.num_pages)

	context = {
		'cattle' : cattle,
		'cows' : cows,
	}

	return render(request, "breeding/on-heat.html", context)


def record_heat(request):
	account = request.user
	if request.method=="POST":
		cattle = get_object_or_404(Cattle, pk=request.POST['cattle'])
		date_noted = request.POST['date_noted']

		record = Heat_records(account=account, cattle=cattle, date_noted=date_noted).save()
		messages.success(request, "Success! Heat record for {} recorded.".format(cattle.name))
		return redirect('breeding:onheat')
	else:
		return redirect('breeding:onheat')


def calve(request, pk):
	record = get_object_or_404(Breeding, pk=pk)

	context = {
		'record' : record,
	}

	return render(request, "breeding/calve.html", context)






