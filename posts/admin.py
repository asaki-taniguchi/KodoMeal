from django.contrib import admin
from .models import Post, Favorite, PostKidsMenu, PostImage , PostSeatType

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store', 'menu_name', 'is_draft', 'created_at')
    ordering = ('-created_at',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store', 'created_at')
    ordering = ('-created_at',)
    
@admin.register(PostKidsMenu)
class PostKidsMenuAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'menu_name', 'quantity', 'target_age')
    ordering = ('id',)
    
@admin.register(PostSeatType)
class PostSeatTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'seat_type', 'created_at')
    ordering =('id',)
    
@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'image', 'created_at')
    ordering =('id',)   