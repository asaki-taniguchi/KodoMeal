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
    has_kids_chair = models.BooleanField(default=False)
    has_diaper_table = models.BooleanField(default=False)
    has_kids_space = models.BooleanField(default=False)
    has_kids_cutlery = models.BooleanField(default=False)
    is_stroller_ok = models.BooleanField(default=False)
    content = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
    
class PostSeatType(models.Model):
    SEAT_TYPE_TATAMI = 1
    SEAT_TYPE_TABLE = 2
    SEAT_TYPE_PRIVATE_ROOM = 3
    
    SEAT_TYPE_CHOICES = [
        (SEAT_TYPE_TATAMI, '座敷'),
        (SEAT_TYPE_TABLE, 'テーブル'),
        (SEAT_TYPE_PRIVATE_ROOM, '個室'),
    ]
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='seat_types'
    )
    seat_type = models.IntegerField(
        choices=SEAT_TYPE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.post.store.name}の座敷タイプ：{self.get_seat_type_display()}'

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
    