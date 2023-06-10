from django.contrib import admin

from .models import Match


class MatchAdmin(admin.ModelAdmin):
    '''Класс для вывода на странице админа
    информации о Симпатиях пользователей.'''

    list_display = ('id', 'liker', 'liking')
    list_filter = ('liker', 'liking')


admin.site.register(Match, MatchAdmin)
