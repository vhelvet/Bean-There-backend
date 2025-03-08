from django.urls import path
from favorite import views


urlpatterns = [
    path('', views.FavoriteListCreateView.as_view(), name='favorite-list'),
    path('<int:cafe_id>/', views.FavoriteDetailView.as_view(), name='favorite-detail'),
]
