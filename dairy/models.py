from django.db import models
from datetime import date

# Create your models here.
class Cattle(models.Model):
	account = models.ForeignKey('auth.User', default=1, null=True)
	name = models.CharField(max_length=20)
	tag_no = models.CharField(max_length=10)
	breed = models.CharField(max_length = 30, blank=True)
	sex = models.CharField(max_length=20)
	dob = models.DateField()
	gotten_through = models.CharField(max_length=20, blank=True)
	stage = models.CharField(max_length=20, blank=True)
	dam = sire = models.CharField(max_length=200, blank=True)
	sire = models.CharField(max_length=200, blank=True)
	conception_method = models.CharField(max_length=50)
	date_added = models.DateField(default = date.today)

	def __str__(self):
		return self.name


class Milk(models.Model):
	account = models.ForeignKey('auth.User', default=1, null=True)
	cattle = models.ForeignKey(Cattle)
	session = models.CharField(max_length=20)
	amount = models.FloatField()
	milking_date = models.DateField(default = date.today)

	def __str__(self):
		return '{}'.format(self.amount)

class MilkSale(models.Model):
	account = models.ForeignKey('auth.User', default=1, null=True)
	milk = models.FloatField()
	amount = models.FloatField()
	date_sold = models.DateField()

	def __str__(self):
		return "{}".format(self.milk)
