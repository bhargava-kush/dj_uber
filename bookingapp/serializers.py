from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

from allauth.account.adapter import get_adapter

from dj_uber.users.models import User
from bookingapp.models import Passenger, Driver

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
