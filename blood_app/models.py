from django.db import models
from django.contrib.auth.models import User
from math import radians, cos, sin, asin, sqrt

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor')
    blood_group = models.CharField(max_length=5)
    location = models.CharField(max_length=100)
    # --- ADD THIS LINE BELOW ---
    phone = models.CharField(max_length=15, null=True, blank=True) 
    # ---------------------------
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def get_distance_from(self, h_lat, h_lon):
        if not all([self.latitude, self.longitude, h_lat, h_lon]):
            return 999.9
        lon1, lat1, lon2, lat2 = map(radians, [self.longitude, self.latitude, h_lon, h_lat])
        dlon, dlat = lon2 - lon1, lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        return round(2 * asin(sqrt(a)) * 6371, 2)

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital')
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # ADD THIS LINE:
    is_verified = models.BooleanField(default=False)


class DonationRequest(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']