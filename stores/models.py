from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    business_hours = models.CharField(max_length=255, blank=True)
    regular_holiday = models.CharField(max_length=100, blank=True)  
    has_parking = models.BooleanField(default=False)
    parking_comment = models.CharField(max_length=255, blank=True)
    is_closed = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name