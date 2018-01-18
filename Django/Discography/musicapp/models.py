from django.db import models


class Artist(models.Model):
    """
    Модель исполнителя
    """
    artist_name = models.CharField('Исполнитель', max_length=30)
    description = models.TextField('Описание', blank=True, null=True)
    albums = models.ManyToManyField('Album',verbose_name = 'Альбомы', related_name='Artist',
                                    blank=True)

    class Meta:
        ordering = ('artist_name',)
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self):
        return self.artist_name


class Album(models.Model):
    """
    Модель альбома
    """
    album_name = models.CharField('Название', max_length=30)
    release_date = models.DateField('Выпущен')
    genres = models.ManyToManyField('Genre', verbose_name = 'Жанры',  related_name='Album')
    
    class Meta:
        ordering = ('album_name',)
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def __str__(self):
        return self.album_name


class Track(models.Model):
    """
    Модель трека
    """
    track_name = models.CharField('Трек', max_length=40)
    length = models.DurationField('Длительность')
    order_no = models.IntegerField('Номер в альбоме')
    album = models.ForeignKey('Album',verbose_name = 'Альбом', related_name='Track',
                              on_delete='SET_NULL')

    class Meta:
        ordering = ('album','order_no',)
        verbose_name = "Трек"
        verbose_name_plural = "Треки"

    def __str__(self):
        return self.track_name


class Genre(models.Model):
    """
    Модель жанра
    """
    name = models.CharField('Жанр', max_length=15)

    class Meta:
        ordering = ('name',)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name
