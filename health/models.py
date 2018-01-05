from django.db import models
from dairy.models import Cattle

# Create your models here.
class Health_record(models.Model):
	account = account = models.ForeignKey('auth.User', default=1, null=True)
	animal = models.ForeignKey(Cattle)
	symptoms = models.TextField()
	diagnosis = models.CharField(max_length=200)
	treatment_date = models.DateField()

	def __str__(self):
		return self.animal.name

class Treatment(models.Model):
	account = models.ForeignKey('auth.User', default=1, null=True)
	record = models.ForeignKey(Health_record)
	treatment = models.TextField()
	result = models.CharField(max_length=200, blank=True)
	vet = models.CharField(max_length=200, blank=True)
	cost = models.FloatField()
	remarks = models.TextField(blank=True)
	start_date = models.DateField()
	end_date = models.DateField()


	def __str__(self):
		return self.record.animal.name

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

	def __str__(self):
		return self.vaccine.vaccine



class Scheduled_deworming(models.Model):
	account = models.ForeignKey('auth.User', default=1, null=True)
	scheduled_date = models.DateField()
	status = models.IntegerField(default=0)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.scheduled_date

class Dewormed_animals(models.Model):
	account = account = models.ForeignKey('auth.User', default=1, null=True)
	deworming_event = models.ForeignKey(Scheduled_deworming)
	cattle = models.ForeignKey(Cattle)

	def __str__(self):
		return self.deworming_event.scheduled_date




