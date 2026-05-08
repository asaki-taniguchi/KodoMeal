from django.db import models
from django.contrib.auth.models import User
from stores.models import Store

class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    ) 
    menu_name = models.CharField(max_length=100, blank=True)
    target_age = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    facilities = models.JSONField(default=list, blank=True)
    content = models.TextField()
    rating = models.IntegerField()
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='post_images/'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post.store.name}の投稿画像'
        
class PostKidsMenu(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='kids_menus'
    )
    menu_name = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    target_age = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.menu_name    

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
    