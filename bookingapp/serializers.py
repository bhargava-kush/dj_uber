from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

from allauth.account.adapter import get_adapter

from dj_uber.users.models import User
from bookingapp.models import Passenger, Driver, Location

class MyRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=(('DRIVER', 'Driver'),('PASSENGER', 'Passenger')),required=True,write_only=True)

    def get_cleaned_data(self):
        super(MyRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'role': self.validated_data.get('role', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        user.role = self.cleaned_data.get('role')
        if user.role == "DRIVER":
            Driver.objects.create(user=user)
        else:
            Passenger.objects.create(user=user)
        user.save()
        return user


class TokenSerializers(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ['key','role']

    def get_role(self,obj):
        return obj.user.role


# {"current" :
#      {"lang":"3","long":"56", "name":"jk", "type":"current"},
#  "destination": {"lang":"3","long":"56", "name":"jk", "type":"destination"}
#  }

class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = '__all__'

    def create(self, validated_data, user_obj):
        try:
            current_location = Location.objects.create(longitude=validated_data.get('current')['longitude'],
                                    latitude=validated_data.get('current')['latitude'],
                                    location_name=validated_data.get('current')['location_name'],
                                    type=validated_data.get('current')['type'])

            destination_location = Location.objects.create(longitude=validated_data.get('destination')['longitude'],
                                    latitude=validated_data.get('destination')['latitude'],
                                    location_name=validated_data.get('destination')['location_name'],
                                    type=validated_data.get('destination')['type'])

            passenger_obj = Passenger.objects.get(pk=user_obj.pk)
            passenger_obj.phone_number=validated_data.get('phone_number')
            passenger_obj.current_location=current_location
            passenger_obj.destination_location=destination_location
            passenger_obj.save()

            return passenger_obj
        except:
            raise serializers.ValidationError({"response": {
                'success': False,
                'msg': "Data invalid", }
            })
