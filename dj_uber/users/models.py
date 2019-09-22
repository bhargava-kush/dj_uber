from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import CharField
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password, **kwargs):
        user = self.model(username=email, email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("Email Address"), max_length=80, unique=True)
    role = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
