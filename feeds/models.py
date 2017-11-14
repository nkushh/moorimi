from django.db import models
from dairy.models import Cattle

# Create your models here.
class Feeds_inventory(models.Model):
	account = account = models.ForeignKey('auth.User', default=1, null=True)
	feed = models.CharField(max_length=200)
	feed_type = models.CharField(max_length=200)
	stock = models.FloatField()
	date_added = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now_add=False, null=True)

	def __str__(self):
		return self.feed

class Feed_consumption(models.Model):
	account = account = models.ForeignKey('auth.User', default=1, null=True)
	cattle = models.ForeignKey(Cattle)
	feed = models.ForeignKey(Feeds_inventory, on_delete=models.CASCADE)
	amount = models.FloatField()
	feeding_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.feed.feed

