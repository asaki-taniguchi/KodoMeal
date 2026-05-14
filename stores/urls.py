from django.urls import path
from . import views

urlpatterns = [
    path('kodomeal/', views.app_top, name='app_top'),
    path('mypage/store/register/', views.store_register_view, name='store_register'),
    path('search/', views.search_result, name='search_result'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('store/<int:store_id>/edit/', views.store_edit_view, name='store_edit'),
    path('store/<int:store_id>/closed/toggle/', views.store_toggle_closed_view, name='store_toggle_closed'),
    path('store/<int:store_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
]