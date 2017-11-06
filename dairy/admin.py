from django.contrib import admin
from .models import Cattle, Milk, MilkSale, Cattle_sale, Mortality

# Register your models here.
admin.site.register(Cattle)
admin.site.register(Milk)
admin.site.register(MilkSale)
admin.site.register(Cattle_sale)
admin.site.register(Mortality)