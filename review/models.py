from django.db import models
from accounts.models import CustomUser
from cafe.models import Cafe



# Create your models here.
class Review(models.Model):
    cafe = models.ForeignKey(Cafe, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

 
    def __str__(self):
        return f' Review by {self.user.username} for {self.cafe.name}'