from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewListCreateView.as_view(), name='review-list-create'),  # List & Create Reviews
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),  # Retrieve, Update, & Delete Review    
]

