from django.conf.urls import url 

from . import views

app_name = 'user_profile'

urlpatterns = [
	url(r'^$', views.get_profile, name='profile'),
	url(r'^update-profile/$', views.update_profile, name='update_profile'),
]