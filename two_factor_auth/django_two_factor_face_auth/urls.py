"""authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login2/', views.loginPage, name="login2"),
    path('register2/', views.registerPage, name="register2"),
    path('choose/', views.choose, name="choose"),
    path('register_face/', views.registerFacePage, name='register_face'),
    path('register_rhythm/', views.register_rhythm, name='register_rhythm'),
    path('accounts/register/', views.register, name='register'),
    path('login_face/', views.login_face, name='login_face'),
    path('login_rhythm/', views.login_rhythm, name='login_rhythm'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/home/', views.home, name='home'),
    path('accounts/login/', views.face_login, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.home, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
