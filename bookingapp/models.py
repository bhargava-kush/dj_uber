from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from dj_uber.users.models import User

# Create your models here.
class Category(models.Model):
    pickup_location = models.CharField(max_length=20)
    destination_location = models.CharField(max_length=20)

    def __unicode__(self):
        return self.pickup_location

    def __str__(self):
        return self.pickup_location

    class Meta:
        verbose_name_plural = "Categories"


class Location(models.Model):
    longitude = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    location_name = models.CharField(max_length=20)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.location_name

    def __str__(self):
        return self.location_name

    class Meta:
        verbose_name_plural = "Locations"


class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passenger')
    phone_number = PhoneNumberField(null=True, blank=True)
    current_location = models.ForeignKey('Location', related_name='current_location', on_delete=models.CASCADE,
                                         null=True)
    destination_location = models.ForeignKey('Location', related_name='destination_location', on_delete=models.CASCADE,
                                             null=True, blank=True)

    def __unicode__(self):
        return self.user.email

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Passengers"


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    phone_number = PhoneNumberField(null=True, blank=True)
    cab_number_plate = models.CharField(max_length=20, null=True, blank=True)
    seats = models.CharField(max_length=2, null=True, blank=True)
    pickup_location = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self):
        return self.user.email

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Drivers"




