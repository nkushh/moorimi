from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cattle, Milk, MilkSale, Cattle_sale, Mortality
from breeding.models import Breed, Breeding
import datetime, calendar

# Create your views here.

# Renders the dashboard template with all the data needed
@login_required(login_url='login')
def dashboard(request):
	account = request.user
	cattle = Cattle.objects.filter(account=account).count()
	milk = Milk.objects.filter(account=account).aggregate(Sum('amount'))

	today = datetime.datetime.now()
	mwaka = today.year
	last_month = today.month - 1

	milk_produced_graph = Milk.objects.filter(account=account, milking_date__year=mwaka, milking_date__month=today.month).values('milking_date').annotate(total_graph_milk=Sum('amount'))

	# Milk produced
	current_month_milk = Milk.objects.filter(account=account, milking_date__year=mwaka, milking_date__month=today.month).aggregate(current_month=Sum('amount'))
	previous_month_milk = Milk.objects.filter(account=account, milking_date__year=mwaka, milking_date__month=last_month).aggregate(previous_month=Sum('amount'))
	current_year_milk = Milk.objects.filter(account=account, milking_date__year=mwaka).aggregate(current_year=Sum('amount'))

	# Milk sold
	current_month_sales = MilkSale.objects.filter(account=account, date_sold__year=mwaka, date_sold__month=today.month).aggregate(curr_month_sales=Sum('amount'))
	previous_month_sales = MilkSale.objects.filter(account=account, date_sold__year=mwaka, date_sold__month=last_month).aggregate(prev_month_sales=Sum('amount'))
	current_year_sales = MilkSale.objects.filter(account=account, date_sold__year=mwaka).aggregate(curr_year_sales=Sum('amount'))

	total_milk_sold = MilkSale.objects.filter(account=account, date_sold__year=mwaka).aggregate(total_sold=Sum('milk'))

	if not(total_milk_sold['total_sold']):
		total_milk_sold['total_sold'] = 0

	if not(current_year_milk['current_year']):
		current_year_milk['current_year'] = 0

	consumed_milk = current_year_milk['current_year'] - total_milk_sold['total_sold']

	users = User.objects.count()
	context = {
		'total_cattle' : cattle,
		'total_accounts' : users,
		'total_milk' : milk,
		'current_month_milk' : current_month_milk,
		'previous_month_milk' : previous_month_milk,
		'current_year_milk' : current_year_milk,
		'current_month_sales' : current_month_sales,
		'previous_month_sales' : previous_month_sales,
		'current_year_sales' : current_year_sales,
		'total_milk_sold' : total_milk_sold,
		'consumed_milk' : consumed_milk,
		'milk_produced_graph' : milk_produced_graph,
	}

	return render(request, 'dairy/dashboard.html', context)


# Gets all cattle stored in the database
@login_required(login_url='login')
def fetch_cattle(request):
	account=request.user
	cattle = Cattle.objects.filter(account=account, cattle_status=0)
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
	}
	return render(request, 'dairy/cattle-list.html', context)


@login_required(login_url='login')
def add_cattle(request):
	breeds = Breed.objects.all()
	context = {
		'breeds' : breeds,
	}
	return render(request, 'dairy/add-cattle.html', context)


@login_required(login_url='login')
def new_cattle(request):
	if request.method == "POST":
		account = request.user
		tag_no = request.POST['tag_no']
		name = request.POST['name']
		breed = request.POST['breed']
		sex = request.POST['sex']
		dob = request.POST['dob']
		gotten_through = request.POST['gotten_through']
		stage = request.POST['stage']
		sire = request.POST['sire']
		conception_method = request.POST['conception_method']


		if Cattle.objects.filter(account=account, tag_no=tag_no).exists():
			messages.warning(request, "Error! That tag number exists. Enter a new one.")
			return redirect('dairy:cattle-list')
		else:
			cattle = Cattle(
					account=account, 
					name=name,
					tag_no=tag_no,  
					breed=breed,
					sex=sex,
					dob=dob,
					gotten_through=gotten_through,
					stage=stage,
					sire=sire,
					conception_method=conception_method
					).save()

			# Check whether you are recording a calf and the breeding record id is set.
			# If True, set the birth_status field in breeding table to 1
			try:
				pk = request.POST['breeding_id']
				record = get_object_or_404(Breeding, pk=pk)
				record.birth_status = 1
				record.save()

				# Get the calf's mother details and set it's stage to.. 
				# Lactating now that it has given birth.
				dam_stage = get_object_or_404(Cattle, pk=record.cattle.pk)
				dam_stage.stage = 'Lactating'
				dam_stage.save()
			except:
				messages.success(request, "Success! {}'s' details successfully recorded.".format(name))

			messages.success(request, "Success! {}'s' details successfully recorded.".format(name))
			return redirect('dairy:cattle-list')
	else:
		messages.error(request, "Error! Cattle details were not recorded.")
		return redirect('dairy:cattle-list')


@login_required(login_url='login')
def cattle_detail(request, cattle_id):
	account=request.user
	cow = get_object_or_404(Cattle, pk=cattle_id)
	milk = Milk.objects.filter(account=account, cattle=cow).values('milking_date').annotate(total_milk=Sum('amount')).order_by('-milking_date')
	context = {
		'cow' : cow,
		'milk' : milk,
	}

	return render(request, 'dairy/cattle-detail.html', context)


@login_required(login_url='login')
def edit_cattle(request, cattle_id):
	cattle = get_object_or_404(Cattle, pk=cattle_id)
	context = {
		'cattle' : cattle,
	}

	return render(request, 'dairy/edit-cattle.html', context)


@login_required(login_url='login')
def update_cattle(request, cattle_id):
	if request.method == "POST":
		cattle = get_object_or_404(Cattle, pk=cattle_id)
		cattle.account = request.user
		cattle.tag_no = request.POST['tag_no']
		cattle.name = request.POST['name']
		cattle.breed = request.POST['breed']
		cattle.save()

		messages.success(request, "Success! Cattle details successfully updated.")
		return redirect('dairy:cattle-detail', cattle_id=cattle.pk)
	else:
		messages.error(request, "Error! Cattle details were not updated.")
		return redirect('dairy:cattle-detail', cattle_id=cattle.pk)



#Fetch records of cattle sold
@login_required(login_url='login')
def sold_cattle(request):
	account = request.user
	records = Cattle_sale.objects.filter(account=account)
	page = request.GET.get('page', 1)

	paginator = Paginator(records, 10)

	try:
		records = paginator.page(page)
	except PageNotAnInteger:
		records = paginator.page(1)
	except EmptyPage:
		records = paginator.page(paginator.num_pages)

	context = {
		'records' : records,
	}

	return render(request, "dairy/sold-cattle.html", context)


@login_required(login_url='login')
def sell_cattle(request, cattle_id):
	cattle = get_object_or_404(Cattle, pk=cattle_id)

	context = {
		'cattle' : cattle,
	}

	return render(request, "dairy/cattle-sale.html", context)

@login_required(login_url='login')
def record_cattle_sale(request):
	account = request.user
	if request.method == 'POST':
		account = account
		cattle = get_object_or_404(Cattle, pk=request.POST['cattle'])
		amount = request.POST['amount']
		sold_to = request.POST['sold_to']
		date_sold = request.POST['date_sold']

		
		if not(Cattle_sale.objects.filter(account=account, cattle=cattle).exists()):
			sale = Cattle_sale(account=account, cattle=cattle, amount=amount, sold_to=sold_to, date_sold=date_sold).save()
			cattle.cattle_status = 1
			cattle.save()
			messages.success(request, "Success! Sale of {} has been recorded successfully".format(cattle.name))
			return redirect('dairy:sold-cattle')
		else:
			messages.error(request, "Error! Sale record of {} already exists".format(cattle.name))
			return redirect('dairy:sold-cattle')
	else:
		messages.warning(request, "Warning! No data was posted")
		return redirect('dairy:cattle-list')


@login_required(login_url='login')
def cattle_death(request, cattle_id):
	cattle = get_object_or_404(Cattle, pk=cattle_id)

	context = {
		'cattle' : cattle,
	}

	return render(request, "dairy/record-death.html", context)

@login_required(login_url='login')
def record_cattle_death(request):
	account = request.user
	if request.method == "POST":
		cattle = get_object_or_404(Cattle, pk=request.POST['cattle'])
		date_of_death = request.POST['died_on']
		postmortem_report = request.POST['postmortem_report']
		# Calculate age
		leo = datetime.date.today()
		dob = cattle.dob
		# if leo.year==dob.year
		# 	age = leo.month
		# else:
		age = (leo.year-dob.year)

		record =  Mortality(account=account, cattle=cattle, age=age, postmortem_report=postmortem_report, died_on=date_of_death).save()
		cattle.cattle_status = 2
		cattle.save()
		messages.success(request, "Success! {}'s death recorded successfully.".format(cattle.name))
		return redirect('dairy:cattle-list')
	else:
		messages.warning(request, "Warning! No data was posted.")
		return redirect('dairy:cattle-list')




@login_required(login_url='login')
def delete_cattle(request, cattle_id):
	cattle = get_object_or_404(Cattle, pk=cattle_id)
	cattle.delete()
	messages.success(request, "Success! Cattle details successfully deleted.")
	return redirect('dairy:cattle-list')



# Milk related functions

# Method to load/render the template to add milk records
@login_required(login_url='login')
def add_milk(request):
	cattle = Cattle.objects.filter(account=request.user, stage="Lactating")
	context = {
		'cattle' : cattle,
	}
	return render(request, 'dairy/add-milk.html', context)

# Method that reads current month milk production records from database and displays in the template
@login_required(login_url='login')
def milk_records(request):
	account = request.user
	today = datetime.datetime.now()
	mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	cattle = Cattle.objects.filter(account=account)
	milk = Milk.objects.filter(account=account, milking_date__year=mwaka, milking_date__month=today.month).values('cattle').annotate(total_milk=Sum('amount')).order_by('-total_milk')
	context = {
		'cattle' : cattle,
		'months_choices' : months_choices,
		'milk' : milk,
	}
	return render(request, 'dairy/milk-records.html', context)

# Method to record milk produced per session by each cattle
@login_required(login_url='login')
def record_milk_produced(request):
	account = request.user
	today = datetime.date.today()
	if request.method == "POST":
		account = account
		cattle = get_object_or_404(Cattle, pk=request.POST['cattle'])
		session = request.POST['session']
		amount = request.POST['amount']

		if Milk.objects.filter(account=account, cattle=cattle, session=session, milking_date=today).exists():
			messages.warning(request, "Error! {}'s {} Milk record for today already exist.".format(cattle, session))
			return redirect('dairy:milk-records')
		else:
			milk = Milk(account=account, cattle=cattle, session=session, amount=amount).save()
			messages.success(request, "Success! {}'s {} Milk record submitted.".format(cattle, session))
			return redirect('dairy:milk-records')
	else:
		return redirect('dairy:milk-records')

# Method to record milk produced by a cattle when in their profile page
@login_required(login_url='login')
def record_cattle_milk(request):
	today = datetime.date.today()

	if request.method == "POST":
		account = request.user
		cattle = get_object_or_404(Cattle, pk=request.POST['cattle'])
		session = request.POST['session']
		amount = request.POST['amount']
		if Milk.objects.filter(account=account, cattle=cattle, session=session, milking_date=today).exists():
			messages.warning(request, "Error! {}'s {} Milk record for today already exist.".format(cattle, session))
			return redirect('dairy:cattle-detail', cattle_id=cattle.pk)
		else:
			milk = Milk(account=account, cattle=cattle, session=session, amount=amount).save()
			messages.success(request, "Success! Milk record submitted.")
			return redirect('dairy:cattle-detail', cattle_id=cattle.pk)



# Method that reads specified month milk production records from database and displays in the template
@login_required(login_url='login')
def monthly_milk_records(request, month):
	account = request.user
	today = datetime.datetime.now()
	mwaka = today.year
	if not month:
		month = today.month

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))


	cattle = Cattle.objects.filter(account=account)
	milk = Milk.objects.filter(account=account, milking_date__year=mwaka, milking_date__month=month).values('cattle').annotate(total_milk=Sum('amount')).order_by('-total_milk')
	query_month = calendar.month_name[int(month)]

	context = {
		'milk' : milk,
		'cattle' : cattle,
		'months_choices' : months_choices,
		'query_month' : query_month,
	}
	return render(request, 'dairy/milk-records.html', context)

# Method that reads current month milk production grouped by day and displays in the template
@login_required(login_url='login')
def daily_milk_records(request):
	account = request.user
	today = datetime.datetime.now()
	mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))


	milk = Milk.objects.filter(account=account, milking_date__year=mwaka, milking_date__month=today.month).values('milking_date').annotate(total_milk=Sum('amount')).order_by('-milking_date')
	query_month = calendar.month_name[int(today.month)]

	context = {
		'milk' : milk,
		'months_choices' : months_choices,
	}
	return render(request, 'dairy/daily-milk-records.html', context)

# Method that takes in an argument of the month the user wants to view milk production of and groups that data by day.
@login_required(login_url='login')
def daily_milk_production(request, month):
	account = request.user
	today = datetime.datetime.now()
	mwaka = today.year
	if not month:
		month = today.month

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))


	milk = Milk.objects.filter(account=account, milking_date__year=mwaka, milking_date__month=month).values('milking_date').annotate(total_milk=Sum('amount')).order_by('-milking_date')
	query_month = calendar.month_name[int(month)]

	context = {
		'milk' : milk,
		'months_choices' : months_choices,
		'query_month' : query_month,
	}
	return render(request, 'dairy/daily-milk-records.html', context)


# Renders a template with data for current month milk sale records
@login_required(login_url='login')
def milk_sale_records(request):
	account = request.user
	sales = MilkSale.objects.filter(account=account).order_by('-date_sold')

	today = datetime.datetime.now()
	mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	context = {
		'sales' : sales,
		'months_choices' : months_choices,
	}
	return render(request, 'dairy/milk-sale.html', context)


# Records new milk sale data to the database
@login_required(login_url='login')
def record_milk_sale(request):
	if request.method == "POST":
		account = request.user
		milk = float(request.POST['milk'])
		amount = milk * float(request.POST['amount'])
		date_sold = request.POST['date_sold'] 
		sale = MilkSale(account=account, milk=milk, amount=amount, date_sold=date_sold).save()
		return redirect('dairy:milk-sale-records')


# Renders a template containing specified month milk sale data
@login_required(login_url='login')
def monthly_milk_sales(request, month):
	account = request.user
	today = datetime.datetime.now()
	mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))


	sales = MilkSale.objects.filter(account=account, date_sold__year=mwaka, date_sold__month=month).order_by('-date_sold')
	context = {
		'sales' : sales,
		'months_choices' : months_choices,
	}
	return render(request, 'dairy/milk-sale.html', context)

# Reads milk sale records for the current year
@login_required(login_url='login')
def annual_milk_sales(request):
	account = request.user
	sales = MilkSale.objects.filter(account=account, date_sold__year=today.year).values('date_sold.month').annotate(total_sales=Sum('amount')).order_by('-date_sold.month')
	context = {
		'sales' : sales,
	}
	return render(request, 'dairy/milk-sale.html', context)



