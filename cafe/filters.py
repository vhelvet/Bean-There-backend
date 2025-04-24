import re
from datetime import datetime
from django.db.models import Q
import django_filters
from django_filters.rest_framework import FilterSet
from .models import Cafe

class CafeFilter(FilterSet):
    services = django_filters.CharFilter(method='filter_services')
    opening_hours = django_filters.CharFilter(method='filter_opening_hours')

    class Meta:
        model = Cafe
        fields = ['opening_hours', 'services']  # Allow filtering by opening_hours and services

    def filter_opening_hours(self, queryset, name, value):
        # Parse the target time (e.g., '9AM') to compare with the opening_hours
        target_time = self.parse_time(value)
        
        # Build a Q object to check if any cafe is open at the target_time
        filters = Q()
        for cafe in queryset:
            try:
                opening_time, closing_time = self.parse_opening_hours(cafe.opening_hours)
            except ValueError:
                continue  # Skip cafes with invalid opening hours format

            # Check if the target time is within the opening and closing times
            if self.is_time_within_range(target_time, opening_time, closing_time):
                filters |= Q(id=cafe.id)  # Add this cafe to the filter condition

        # Return filtered queryset with cafes that match the target_time
        return queryset.filter(filters)

    def is_time_within_range(self, target_time, opening_time, closing_time):
        """
        Check if the target time falls within the opening and closing times.
        Handle cases like cafes opening before midnight and closing after midnight.
        """
        # If closing time is before opening time, the cafe is open past midnight
        if closing_time <= opening_time:
            return opening_time <= target_time or target_time <= closing_time
        return opening_time <= target_time <= closing_time

    def parse_opening_hours(self, opening_hours):
        """
        Parse the opening_hours string into start and end time objects.
        Example: '7AM - 12MN' -> (datetime.time(7, 0), datetime.time(12, 0))
        """
        try:
            # Extract start and end times from the opening_hours string (e.g., '7AM - 12MN')
            match = re.match(r'(\d{1,2}[APM]{2})\s*-\s*(\d{1,2}[APM]{2})', opening_hours)
            if not match:
                raise ValueError("Invalid opening hours format.")
            
            start_time_str, end_time_str = match.groups()

            # Parse both start and end times
            start_time = self.parse_time(start_time_str)
            end_time = self.parse_time(end_time_str)
            
            # Handle case where the end time is after midnight (e.g., '12MN' as 12AM)
            if end_time <= start_time:
                # Adjust to a valid range (closing time should be after opening time)
                end_time = datetime.strptime("11:59PM", "%I:%M%p").time()
            
            return start_time, end_time
        except ValueError as e:
            raise ValueError(f"Invalid opening hours format: {e}")

    def parse_time(self, time_str):
        """
        Convert 12-hour format time string (e.g., '9AM') into a 24-hour format time object.
        Example: '9AM' -> datetime.time(9, 0)
        """
        # Use the strptime method to parse the time into a datetime object, then extract the time part
        try:
            time_obj = datetime.strptime(time_str, '%I%p')
            return time_obj.time()
        except ValueError:
            raise ValueError(f"Invalid time format for {time_str}. Expected 'HHAM' or 'HHPM'.")

    def filter_services(self, queryset, name, value):
        # Filter cafes by services if a service value is provided
        return queryset.filter(services__icontains=value)
