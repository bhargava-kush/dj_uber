from django.conf.urls import url
from bookingapp import views
from django.urls import include, path

app_name = "bookingapp"

urlpatterns = [
    path('set-location/', views.LocationSetView.as_view(), name='set_location'),
    path('availabe-rides/', views.available_ride, name='available-rides'),
    path('accept-ride/', views.accept_ride, name='accept-ride'),
    path('request-ride/', views.request_ride, name='request-ride'),
    path('ride-accepted/', views.is_ride_accepted, name='ride-accepted'),
]
