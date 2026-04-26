from django.db import models

class Post(models.Model):
    store_id = models.IntegerField()
    menu_name = models.CharField(max_length=100, blank=True)
    target_age = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    facilities = models.JSONField(default=list, blank=True)
    content = models.TextField()
    rating = models.IntegerField()
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    