from django.db import models
from django.apps import apps


# Create your models here.

class Cafe(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    opening_hours = models.CharField(max_length=255)
    about = models.TextField()
    menu = models.TextField()
    services = models.JSONField()
    social_media = models.JSONField()
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
