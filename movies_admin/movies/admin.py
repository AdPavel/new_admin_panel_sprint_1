from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import DateRangeFilter

from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork



@admin.register(PersonFilmwork)
class PersonFilmworkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'person', 'role')
    list_filter = ('role', ('person', RelatedDropdownFilter))


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating')
    # Фильтрация в списке
    list_filter = ('type', ('creation_date', DateRangeFilter),
                   ('genres', RelatedDropdownFilter), ('persons', RelatedDropdownFilter))

    # Поиск по полям
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)






