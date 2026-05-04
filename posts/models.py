from django.db import models
from django.contrib.auth.models import User
from stores.models import Store

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
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'store'],
                name='unique_user_store_favorite'
            )
        ]
    