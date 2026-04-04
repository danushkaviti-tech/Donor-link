import django_filters
from .models import Donor

class DonorFilter(django_filters.FilterSet):
    class Meta:
        model = Donor
        fields = ['blood_group', 'location']