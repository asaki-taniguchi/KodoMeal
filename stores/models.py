from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    phone = models.CharField(max_length=20, blank=True)
    holiday = models.CharField(max_length=100, blank=True)
    hours = models.CharField(max_length=100, blank=True)
    parking = models.CharField(max_length=255, blank=True)
    
    target_age = models.CharField(max_length=50, blank=True)
    
    has_kids_chair = models.BooleanField(default=False)
    is_stroller_ok = models.BooleanField(default=False)
    has_diapper = models.BooleanField(default=False)
    has_kids_space = models.BooleanField(default=False)
    has_kids_cutlery = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name