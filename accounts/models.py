from django.db import models


# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    barangay = models.CharField(max_length=255, blank=True, null=True)   
    # Add custom fields here, if needed


    def __str__(self):
        return self.username
   


''' What This Does:


AbstractUser: Django’s default user model. We’re extending it to add custom fields.


email = models.EmailField(unique=True): Ensures each user has a unique email.


__str__: Defines how the user is displayed (e.g., in the admin panel).'''
