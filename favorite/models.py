from django.db import models
from accounts.models import CustomUser
from cafe.models import Cafe  


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'cafe')  # Prevent duplicate favorites
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.user.username} favorites {self.cafe.name}"


