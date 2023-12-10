"""
URL configuration for djangoApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django import views
from django.contrib import admin
from django.urls import path

from app01 import views as app01_views
from api import views as api_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path("auth/", app01_views.auth),
    # path("login/", app01_views.login),  # Fbv
    # path("info/<str:dt>/", app01_views.InfoView.as_view()),  # Drf的CBV
    # #/user/111/ -> pk=111
    # path("user/<int:pk>/", app01_views.UserView.as_view()),  # Django原生CBV
    # path("authlogin/", app01_views.AuthloginView.as_view()),
    # path("authuser/", app01_views.AuthuserView.as_view()),
    # path("authorder/", app01_views.AuthorderView.as_view()),
    path("login/", app01_views.LoginView.as_view()),
    path("user/", app01_views.UserView.as_view()),
    path("order/", app01_views.OrderView.as_view(), name="order"),
    path("avatar/", app01_views.AvatarView.as_view()),
    # __________________apiview______________________
    path("home/", api_views.HomeView.as_view()),
    path("api/<str:version>/home2/", api_views.Home2View.as_view(),name="h2"),
    path("home3/", api_views.Home3View.as_view()),
]
