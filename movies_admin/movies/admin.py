from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import DateRangeFilter

from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)


@admin.register(PersonFilmwork)
class PersonFilmworkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'person', 'get_actor')
    list_filter = ('role', ('person', RelatedDropdownFilter))


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'get_genres', 'rating')

    list_prefetch_related = ('genres', )

    def get_queryset(self, request):
        queryset = (
            super()
                .get_queryset(request)
                .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'

    list_filter = ('type', ('creation_date', DateRangeFilter),
                   ('genres', RelatedDropdownFilter), ('persons', RelatedDropdownFilter))

    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)
