from django.db import models
from dairy.models import Cattle

# Create your models here.
class Breed(models.Model):
	breed_name = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.breed_name

class Breeding(models.Model):
	account = models.ForeignKey('auth.User', default=1, null=True)
	cattle = models.ForeignKey(Cattle)
	method = models.CharField(max_length=50)
	sire = models.CharField(max_length=200, blank=True)
	breed = models.ForeignKey(Breed)
	date_served = models.DateField()
	delivery_due = models.DateField()
	birth_status = models.IntegerField(default=0)
	date_recorded = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.cattle.name

class Heat_records(models.Model):
	account = models.ForeignKey('auth.User', default=1, null=True)
	cattle = models.ForeignKey(Cattle)
	date_noted = models.DateField()
	heat_status = models.IntegerField(default=0)
	date_recorded = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.cattle.name
