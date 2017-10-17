from django.contrib import admin

from .models import Breed, Breeding, Heat_records

# Register your models here.
admin.site.register(Breed)
admin.site.register(Breeding)
admin.site.register(Heat_records)