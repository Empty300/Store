from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    country = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    telephone = models.CharField(max_length=256, null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)




