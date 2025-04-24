from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    barangay = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg')   
    # Add custom fields here, if needed

    def __str__(self):
        return self.username
   


''' What This Does:


AbstractUser: Django’s default user model. We’re extending it to add custom fields.


email = models.EmailField(unique=True): Ensures each user has a unique email.


__str__: Defines how the user is displayed (e.g., in the admin panel).'''
