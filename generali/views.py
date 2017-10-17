from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Max, Avg
from django.shortcuts import render, get_object_or_404, redirect
from dairy.models import Cattle, Milk, MilkSale
import datetime, calendar

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
	admin = request.user

	if admin.is_superuser:
		cattle = Cattle.objects.count()
		milk = Milk.objects.aggregate(Sum('amount'))

		today = datetime.datetime.now()
		mwaka = today.year
		last_month = today.month - 1

		milk_produced_graph = Milk.objects.filter(milking_date__year=mwaka, milking_date__month=today.month).values('milking_date').annotate(total_graph_milk=Sum('amount'))

		# Milk produced
		current_month_milk = Milk.objects.filter(milking_date__year=mwaka, milking_date__month=today.month).aggregate(current_month=Sum('amount'))
		previous_month_milk = Milk.objects.filter(milking_date__year=mwaka, milking_date__month=last_month).aggregate(previous_month=Sum('amount'))
		current_year_milk = Milk.objects.filter(milking_date__year=mwaka).aggregate(current_year=Sum('amount'))

		# Milk sold
		current_month_sales = MilkSale.objects.filter(date_sold__year=mwaka, date_sold__month=today.month).aggregate(curr_month_sales=Sum('amount'))
		previous_month_sales = MilkSale.objects.filter(date_sold__year=mwaka, date_sold__month=last_month).aggregate(prev_month_sales=Sum('amount'))
		current_year_sales = MilkSale.objects.filter(date_sold__year=mwaka).aggregate(curr_year_sales=Sum('amount'))

		total_milk_sold = MilkSale.objects.filter(date_sold__year=mwaka).aggregate(total_sold=Sum('milk'))

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
	else:
		message.warning(request, 'Super-user access required.')
		return redirect('login')





@login_required(login_url='login')
def account_dashboard(request, account):
	admin = request.user
	if admin.is_superuser:
	 	farm = get_object_or_404(User, pk=account)
	 	cattle = Cattle.objects.filter(account=farm).count()
	 	milk = Milk.objects.filter(account=farm).aggregate(Sum('amount'))

	 	today = datetime.datetime.now()
	 	mwaka = today.year
	 	last_month = today.month - 1

	 	milk_produced_graph = Milk.objects.filter(account=farm, milking_date__year=mwaka, milking_date__month=today.month).values('milking_date').annotate(total_graph_milk=Sum('amount'))
	 	
	 	# Milk produced
	 	current_month_milk = Milk.objects.filter(account=farm, milking_date__year=mwaka, milking_date__month=today.month).aggregate(current_month=Sum('amount'))
	 	previous_month_milk = Milk.objects.filter(account=farm, milking_date__year=mwaka, milking_date__month=last_month).aggregate(previous_month=Sum('amount'))
	 	current_year_milk = Milk.objects.filter(account=farm, milking_date__year=mwaka).aggregate(current_year=Sum('amount'))

	 	# Milk sold
	 	current_month_sales = MilkSale.objects.filter(account=farm, date_sold__year=mwaka, date_sold__month=today.month).aggregate(curr_month_sales=Sum('amount'))
	 	previous_month_sales = MilkSale.objects.filter(account=farm, date_sold__year=mwaka, date_sold__month=last_month).aggregate(prev_month_sales=Sum('amount'))
	 	current_year_sales = MilkSale.objects.filter(account=farm, date_sold__year=mwaka).aggregate(curr_year_sales=Sum('amount'))

	 	total_milk_sold = MilkSale.objects.filter(account=farm, date_sold__year=mwaka).aggregate(total_sold=Sum('milk'))

	 	if not(total_milk_sold['total_sold']):
	 		total_milk_sold['total_sold'] = 0

	 	if not(current_year_milk['current_year']):
	 		current_year_milk['current_year'] = 0

	 	consumed_milk = current_year_milk['current_year'] - total_milk_sold['total_sold']

	 	users = User.objects.count()

	 	context = {
	 		'farm' : farm,
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

	 	return render(request, 'generali/farm-dashboard.html', context)
	else:
		message.warning(request, 'Super-user access required.')
		return redirect('login')


@login_required(login_url='login')
def fetch_cattle(request, account):
	admin=request.user

	if admin.is_superuser:
		cattle = Cattle.objects.filter(account=account)
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
	else:
		message.warning(request, 'Super-user access required.')
		return redirect('login')
