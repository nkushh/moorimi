from django.contrib import admin
from .models import Cattle, Milk, MilkSale

# Register your models here.
admin.site.register(Cattle)
admin.site.register(Milk)
admin.site.register(MilkSale)