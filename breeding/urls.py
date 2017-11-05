from django.conf.urls import url

from . import views

app_name = 'breeding'

urlpatterns = [
	url(r'^served-cattle/$', views.served_cattle, name='served_cattle'),
	url(r'^serve-cattle/$', views.serve_cattle, name='serve_cattle'),
	url(r'^service-details/(?P<pk>\d+)/$', views.cattle_to_serve, name='cattle_to_serve'),
	url(r'^cattle-onheat/$', views.cattle_onheat, name='onheat'),
	url(r'^record-heat/$', views.record_heat, name='record_heat'),
	url(r'^calve/(?P<pk>\d+)/$', views.calve, name='calve'),
]