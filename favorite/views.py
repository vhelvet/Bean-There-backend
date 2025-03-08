from rest_framework import generics, permissions, status
from rest_framework.response import Response
from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer, CreateFavoriteSerializer
from cafe.models import Cafe
from django.shortcuts import get_object_or_404


class FavoriteListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]  # Temporarily AllowAny for testing
   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateFavoriteSerializer
        return FavoriteSerializer
   
    def get_queryset(self):
        # For testing: show all favorites if not authenticated
        if not self.request.user.is_authenticated:
            return Favorite.objects.all().select_related('cafe')[:10]  # Limit to 10
        return Favorite.objects.filter(user=self.request.user).select_related('cafe')
   
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            # For testing: use a default user if not authenticated
            from accounts.models import CustomUser
            user = CustomUser.objects.first()  # Change this as needed
        else:
            user = self.request.user
        serializer.save(user=user)


class FavoriteDetailView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]  # Temporarily AllowAny for testing
    queryset = Favorite.objects.all()
    lookup_field = 'pk'
   
    def get_object(self):
        obj = get_object_or_404(Favorite, pk=self.kwargs['pk'])
        # Skip ownership check for testing
        return obj
   
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'detail': 'Favoriteremoved successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
