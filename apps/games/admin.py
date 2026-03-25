from django.contrib import admin
from .models import Game, Genre, Language, Screenshot

admin.site.register(Genre)
admin.site.register(Language)


class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 1
    fields = ('image',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    filter_horizontal = ('genres', 'interface_language', 'voice_language')
    list_display = ('name', 'developer', 'created_at')
    search_fields = ('name', 'developer')
    inlines = [ScreenshotInline]


