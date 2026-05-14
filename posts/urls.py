from django.urls import path
from . import views

urlpatterns = [
    path('store/<int:store_id>/post/create/', views.post_create, name='post_create'),
    path('store/<int:store_id>/posts/', views.post_list, name='post_list'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]