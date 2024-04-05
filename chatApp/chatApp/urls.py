"""
URL configuration for chatApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from chat.views import index, login_view, logout_view, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name="login"),
    path('login/', login_view ),
    path('logout/', logout_view, name="logout"),
    path('register/', register, name="register"),
    path('chat/', index, name="index"),
]
