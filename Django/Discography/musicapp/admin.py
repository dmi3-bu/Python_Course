from django.contrib import admin
from musicapp.models import Artist, Album, Track, Genre


# Модель админки, чтобы отображались все колонки при просмотре:
class AllColumnsModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields
                             if field.name != "id"]
        super(AllColumnsModelAdmin, self).__init__(model, admin_site)


admin.site.register(Artist, AllColumnsModelAdmin)
admin.site.register(Album, AllColumnsModelAdmin)
admin.site.register(Track, AllColumnsModelAdmin)
admin.site.register(Genre, AllColumnsModelAdmin)
