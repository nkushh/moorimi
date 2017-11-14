from django.db import models
from dairy.models import Cattle

# Create your models here.
class Health_record(models.Model):
	account = account = models.ForeignKey('auth.User', default=1, null=True)
	animal = models.ForeignKey(Cattle)
	symptoms = models.TextField()
	diagnosis = models.CharField(max_length=200)
	treatment = models.TextField()
	result = models.CharField(max_length=200)
	vet = models.CharField(max_length=200)
	cost = models.FloatField()
	remarks = models.TextField()
	treatment_date = models.DateField()

	def __str__(self):
		return "{}".format(animal.name)

class Vaccinate_schedule(models.Model):
	account = account = models.ForeignKey('auth.User', default=1, null=True)
	vaccine = models.CharField(max_length=200)
	scheduled_date = models.DateField()
	status = models.IntegerField(default=0)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.vaccine

class Vaccinated_animals(models.Model):
	account = account = models.ForeignKey('auth.User', default=1, null=True)
	vaccine = models.ForeignKey(Vaccinate_schedule)
	cattle = models.ForeignKey(Cattle)
