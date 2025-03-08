from django.db import models

# Create your models here.

class Cafe(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    opening_hours = models.CharField(max_length=255)
    about = models.TextField()
    menu = models.TextField()
    services = models.JSONField()
    social_media = models.JSONField()


    def __str__(self):
        return self.name
