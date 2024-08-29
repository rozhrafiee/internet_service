from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_provider = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)