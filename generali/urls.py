from django.conf.urls import url

from . import views

app_name = 'generali'

urlpatterns = [
	url(r'^$', views.dashboard, name='admin-dashboard'),
	url(r'^account/(?P<account>\d+)/detail/$', views.account_dashboard, name='account-detail'),
]