"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView

from .forms import CustomLoginForm
from . import views
from accounts import views as accounts_views
from posts import views as posts_views
from stores import views as stores_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.portfolio_top, name='portfolio_top'),
    path('kodomeal/', views.app_top, name='app_top'),
    path(
        'login/',
        LoginView.as_view(
            template_name='login.html',
            authentication_form=CustomLoginForm
            ),
        name='login'
        ),
    path('register/', accounts_views.register_view, name='register'),
    path('mypage/', accounts_views.mypage_view, name='mypage'),
    path('mypage/posts/', accounts_views.mypage_posts_view, name='mypage_posts'),
    path('mypage/drafts/', accounts_views.mypage_drafts_view, name='mypage_drafts'),
    path('mypage/store/register/', stores_views.store_register_view, name='store_register'),
    path('mypage/account/edit/', accounts_views.account_edit_view, name='account_edit'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('search/', views.search_result, name='search_result'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('store/<int:store_id>/post/create/', posts_views.post_create, name='post_create'),
    path('store/<int:store_id>/posts/', posts_views.post_list, name='post_list'),
    path('post/<int:post_id>/edit/', posts_views.post_edit, name='post_edit'),
    path('store/<int:store_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
