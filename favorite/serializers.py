from rest_framework import serializers
from favorite.models import Favorite
from cafe.serializers import CafeSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    cafe = CafeSerializer(read_only=True)


    class Meta:
        model = Favorite
        fields = ['id', 'cafe', 'created_at']
