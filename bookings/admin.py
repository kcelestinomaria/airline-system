from django.contrib import admin
from .models import Flight, Passenger, Booking

# Register your models here.
admin.site.register([Flight, Passenger, Booking])