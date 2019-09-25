from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from dj_uber.users.models import User


class Location(models.Model):
    TYPES = (
        ('CURRENT', 'current'),
        ('DESTINATION', 'destination'),
    )
    longitude = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    location_name = models.CharField(max_length=70)
    type = models.CharField(choices=TYPES, max_length=20)

    def __unicode__(self):
        return self.location_name

    def __str__(self):
        return self.location_name

    class Meta:
        verbose_name_plural = "Locations"


class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passenger')
    phone_number = PhoneNumberField(null=True, blank=True)
    current_location = models.ForeignKey('Location', related_name='passenger_current_location', on_delete=models.CASCADE,
                                         null=True, blank=True)
    destination_location = models.ForeignKey('Location', related_name='passenger_destination_location', on_delete=models.CASCADE,
                                             null=True, blank=True)
    is_searching = models.BooleanField(default=False)

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
    current_location = models.ForeignKey('Location', related_name='driver_current_location', on_delete=models.CASCADE,
                                         null=True, blank=True)

    def __unicode__(self):
        return self.user.email

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Drivers"


class Trip(models.Model):
    TRIP_STATUS = (('IS_ACTIVE', 'is_active'),
                   ('IS_CANCELED', 'is_cancelled'),
                   ('FINISHED', 'finished'))

    status = models.CharField(choices=TRIP_STATUS, max_length=20)
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True)
    start_location = models.ForeignKey('Location', related_name='start_location', on_delete=models.CASCADE, null=True, blank=True)
    end_location = models.ForeignKey('Location', related_name='end_location', on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self):
        return self.passenger.user.email

    def __str__(self):
        return self.passenger.user.email

    class Meta:
        verbose_name_plural = "Trips"



