from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cafe
from .serializers import CafeSerializer
from .filters import CafeFilter
# Create your views here.

class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

    # Enable search and filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CafeFilter  #filter 
    search_fields = ['name', 'about', 'menu', 'address']  # Allow text search
    ordering_fields = ['name']  # Enable ordering by name
        