from django.conf.urls import url
from . import views


app_name = 'authentication'
urlpatterns = [
	url(r'^accounts/$', views.all_accounts, name='accounts'),
	url(r'^register-user/$', views.register_user, name='register_user'),
	url(r'^register/$', views.create_account, name='register'),
	url(r'^deactivate-account/(?P<account>\d+)/$', views.deactivate_account, name='deactivate-account'),
	url(r'^activate-account/(?P<account>\d+)/$', views.activate_account, name='activate-account'),
	url(r'^delete-account/(?P<account>\d+)/$', views.delete_account, name='delete-account'),
]