from django.contrib import admin
from .models import Cars, Driver, Trips


# Register your models here.
admin.site.register(Cars)
admin.site.register(Driver)
admin.site.register(Trips)