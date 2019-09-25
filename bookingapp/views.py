from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)

from django.conf import settings
from haversine import haversine

from bookingapp.serializers import PassengerSerializer
from .models import Driver, Location, Passenger, Trip


# Create your views here.

class LocationSetView(APIView):
    """
    Set passenger location
    """
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        obj = request.user
        request_data = request.data
        serializer = PassengerSerializer(request_data, obj)
        serializer.create(request_data, obj)
        response = {"response": {
            'success': True,
            'msg': 'Passenger location'}
        }
        return Response(response, status=HTTP_200_OK)


@api_view(['GET'])
@authentication_classes
def available_ride(request):
    """
    Driver checking for availabe rides within some radius
    :param request:
    :return:
    """
    driver_obj = request.user
    driver_tuple = (driver_obj.current_location.longtitude,
                    driver_obj.current_location.latitude)

    passengers = Passenger.objects.filter(is_searching=True)
    vicinity_distances = []
    for passenger in passengers:
        passenger_tuple = (passenger.current_location.longtitude,
                           passenger.current_location.latitude)
        distance = haversine(passenger_tuple, driver_tuple)
        if distance <= settings.ALLOWED_VICINITY_DISTANCE:
            vicinity_distances.append(passenger)

    serializer = PassengerSerializer(vicinity_distances, many=True)
    import pdb;pdb.set_trace();

    response = {"response": {
        'data': serializer.data,
        'msg': 'Passenger location'}
    }
    return Response(response, status=HTTP_200_OK)


@authentication_classes
@api_view(['POST'])
def accept_ride(request):
    """
    Creating trip object and setting passenger is_searching to false
    :param request:
    :return:
    """
    data = request.data
    driver_obj = request.user
    passenger_obj = Passenger.objects.get(pk=data['passenger_id'])

    trip_obj = Trip.objects.create(passenger=passenger_obj, driver=driver_obj,
                                   start_location=passenger_obj.current_location,
                                   end_location=passenger_obj.destination_location,
                                   status="IS_ACTIVE")

    passenger_obj.is_searching = False
    passenger_obj.save()

    response = {"response": {
        'success': True,
        'msg': 'Trip started'}
    }

    return Response(response, status=HTTP_200_OK)


@authentication_classes
@api_view(['GET'])
def request_ride(request):
    """
    Passenger requesting for ride by setting is_searching to true
    :param request:
    :return:
    """
    passenger_obj = request.user
    if Trip.objects.filter(passenger=passenger_obj).last().status == 'IS_ACTIVE':
        response = {"response": {
            'success': False,
            'msg': 'Currently ride in process'}
        }
        return Response(response, status=HTTP_400_BAD_REQUEST)

    passenger_obj.is_searching = True
    passenger_obj.save()
    response = {"response": {
        'success': True,
        'msg': 'Requesting ride'}
    }
    return Response(response, status=HTTP_200_OK)


@authentication_classes
@api_view(['GET'])
def is_ride_accepted(request):
    """
    Checking if ride is accepted or not
    :param request:
    :return:
    """
    passenger_obj = request.user
    last_trip = Trip.objects.filter(passenger=passenger_obj).last()

    if last_trip and last_trip.status == 'IS_ACTIVE':
        response = {"response": {
            'success': True,
            'msg': 'Ride is in progress'}
        }
        return Response(response, status=HTTP_200_OK)  # ride in progress
    elif passenger_obj.is_searching:
        response = {"response": {
            'success': True,
            'msg': 'Searching'}
        }
        return Response(response, status=HTTP_200_OK)  # searching
    else:
        response = {"response": {
            'success': True,
            'msg': 'No ongoing trip nor searching.'}
        }
        return Response(response, status=HTTP_200_OK)
