from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.artists_list),
    path('<str:art_name>/', views.albums_by_artist, name='artist'),
]