from django.contrib import admin
from bookingapp.models import Driver, Passenger, Location, Category
# Register your models here.

admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Location)
admin.site.register(Category)
