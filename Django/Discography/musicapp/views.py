from django.shortcuts import render
from django.http import Http404

from .models import Artist


#class CLASS_NAME(TemplateView):
#    template_name = "TEMPLATE_NAME"

def artists_list(request):
    artists = Artist.objects.all()
    return render(request, 'musicapp/index.html', {'artists': artists})


def albums_by_artist(request, art_name):
    try:
        artist = Artist.objects.get(artist_name=art_name)
    except Artist.DoesNotExist:
        raise Http404

    return render(request, 'musicapp/albums_artist.html', {
                'albums': artist.albums.all(),
                'artist': artist,
    })
