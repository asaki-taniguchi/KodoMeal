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
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from . import views

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
    path('register/', views.register_view, name='register'),
]
