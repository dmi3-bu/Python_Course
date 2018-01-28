from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('genre/<str:genre_input>/', views.genre_info, name='genre'),
    path('artist/<str:artist_input>/', views.artist_info, name='artist'),
    path('album/<int:album_id>/<str:album_input>/', views.album_info, name='album'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
