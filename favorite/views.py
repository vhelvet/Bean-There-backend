from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer
from cafe.models import Cafe


class FavoriteToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, cafe_id):
        user = request.user
        try:
            cafe = Cafe.objects.get(id=cafe_id)
        except Cafe.DoesNotExist:
            return Response({"detail": "Cafe not found."}, status=status.HTTP_404_NOT_FOUND)


        favorite, created = Favorite.objects.get_or_create(user=user, cafe=cafe)
        if not created:
            # Already favorited, so unfavorite
            favorite.delete()
            return Response({"detail": "Cafe unfavorited."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Cafe favorited."}, status=status.HTTP_201_CREATED)


class UserFavoritesListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer


    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user).order_by('-created_at')