from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    list_display = ('full_name',)
    search_fields = ('full_name', 'id')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating')
    # Фильтрация в списке
    list_filter = ('type', 'creation_date')
    # Поиск по полям
    search_fields = ('title', 'description', 'id')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass




