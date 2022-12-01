import uuid

from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('title'), max_length=30)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('Full name'), max_length=50)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('create date'))
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=255,
                            choices=[('movie', _('type movie')), ('tv_show', _('type TV show'))])
    genres = models.ManyToManyField(Genre, through='GenreFilmwork', verbose_name=_('Film genre'))
    persons = models.ManyToManyField(Person, through='PersonFilmwork', verbose_name=_('Person'))
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)

    class Meta:
        db_table = "content\".\"film_work"
        indexes = [
            models.Index(fields=['type', 'creation_date']),
            models.Index(fields=['creation_date', 'rating'])
        ]
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('film_work'))
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [models.Index(fields=['film_work', 'genre'])]
        verbose_name = _('Film genre')
        verbose_name_plural = _('Films genre')

    def __str__(self):
        return ''


class PersonFilmwork(UUIDMixin):
    role_list = [
        ('actor', _('actor')),
        ('director', _('director')),
        ('writer', _('writer'))
    ]


    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('film work'))
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('Person'))
    role = models.CharField(_('role'), choices=role_list, max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [models.UniqueConstraint(fields=['film_work', 'person', 'role'], name="film_work_person_idx")]
        verbose_name = _('Person filmwork')
        verbose_name_plural = _('Persons filmwork')

    def __str__(self):
        return self.role
