from datetime import timedelta
from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from .models import Artist, Album, Genre


def index(request):
    artists = Artist.objects.all()
    if 'sort' in request.GET:
        sort = request.GET['sort']
    else:
        sort = ''

    # В алфавитном порядке:
    if sort == '':
        artists = artists.order_by('artist_name')
    # В обратном алфавитном порядке:
    if sort == 'r':
        artists = artists.order_by('-artist_name')
    # По количеству альбомов:
    if sort == 'a':
        artists = artists.annotate(album_count=Count('albums')).order_by('-album_count', 'artist_name')

    return render(request, 'musicapp/index.html', {'artists': artists})


def artist_info(request, artist_input):
    try:
        artist = Artist.objects.get(artist_name=artist_input)
    except Artist.DoesNotExist:
        raise Http404

    artist.albums.all().order_by('release_date')
    albums = artist.albums.all()

    return render(request, 'musicapp/artist_info.html', {
                'albums': albums,
                'artist': artist,
                'description': artist.description,
    })


# Id необходим, так как у разных исполнителей могут быть альбомы с одинаковым названием
def album_info(request, album_id, album_input):
    try:
        album = Album.objects.get(id=album_id, album_name=album_input)
    except Album.DoesNotExist:
        raise Http404

    # Просуммируем длительность всех треков, чтобы вычислить продолжительность альбома:
    total_length = timedelta(0)
    for track in album.tracks.all():
        total_length += track.length

    return render(request, 'musicapp/album_info.html', {
                'artists': album.artists.all(),
                'album_name': album.album_name,
                'album_cover': album.album_cover,
                'genres': album.genres.all(),
                'release_date': album.release_date,
                'tracks': album.tracks.all(),
                'total_length': total_length,
    })


def genre_info(request, genre_input):
    try:
        genre = Genre.objects.get(name=genre_input)
    except Genre.DoesNotExist:
        raise Http404

    return render(request, 'musicapp/genre_info.html', {
                'genre': genre.name,
                'albums': genre.albums.all(),
    })
