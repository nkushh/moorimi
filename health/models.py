from django.db import models
from dairy.models import Cattle

# Create your models here.
class Health_record(models.Model):
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
