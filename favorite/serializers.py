from rest_framework import serializers
from favorite.models import Favorite
from cafe.models import Cafe  # Add this import
from cafe.serializers import CafeSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    cafe = CafeSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Show user ID


    class Meta:
        model = Favorite
        fields = ['id', 'user', 'cafe', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CreateFavoriteSerializer(serializers.ModelSerializer):
    cafe = serializers.PrimaryKeyRelatedField(
        queryset=Cafe.objects.all(),  # This makes the field appear in DRF form
        help_text="ID of the cafe to favorite"
    )


    class Meta:
        model = Favorite
        fields = ['cafe']  # Only need cafe ID when creating


    def validate(self, data):
        if Favorite.objects.filter(user=self.context['request'].user, cafe=data['cafe']).exists():
            raise serializers.ValidationError("You've already favorited this cafe.")
        return data
