from django.urls import path
from favorite.views import FavoriteToggleView, UserFavoritesListView


urlpatterns = [
    path('toggle/<int:cafe_id>/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('user/', UserFavoritesListView.as_view(), name='user-favorites'),
]
