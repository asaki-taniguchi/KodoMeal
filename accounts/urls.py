from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('password-rest/sent/', views.password_reset_request_view, name='password_reset_sent'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('mypage/posts/', views.mypage_posts_view, name='mypage_posts'),
    path('mypage/drafts/', views.mypage_drafts_view, name='mypage_drafts'),
    path('mypage/account/edit/', views.account_edit_view, name='account_edit'),
]