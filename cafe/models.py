from django.db import models
from django.apps import apps


# Create your models here.

class Cafe(models.Model):
    name = models.CharField(max_length=255)
    image = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    address = models.TextField(default="No address provided", blank=True, null=True)
    opening_hours = models.CharField(max_length=255, default="Not specified")
    about = models.TextField(blank=True, null=True)
    menu = models.TextField(blank=True, null=True)
    services = models.JSONField(blank=True, null=True)
    social_media = models.JSONField(blank=True, null=True)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    

    def update_rating(self):
        Review = apps.get_model('review', 'Review')
        reviews = Review.objects.filter(cafe=self)
        total_rating = sum([review.rating for review in reviews])
        self.total_reviews = reviews.count()
        self.average_rating = total_rating / self.total_reviews if self.total_reviews > 0 else 0.0
        self.save()



    def __str__(self):
        return self.name
