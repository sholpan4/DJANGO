import os
from datetime import datetime
from os.path import splitext

from django.contrib.postgres.fields import DateTimeRangeField, ArrayField, HStoreField, CICharField
from django.contrib.postgres.indexes import GistIndex
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Spare(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)

    def __str__(self):
        return f'{self.name}'


class PGSRoomReserving(models.Model):
    name = models.CharField(max_length=20, verbose_name='Помещение')
    reserving = DateTimeRangeField(verbose_name='Время резервирования')
    cancelled = models.BooleanField(default=False, verbose_name='Отменить резервирование')

    class Meta:
        indexes = [
            GistIndex(fields=['reserving'],
                      name='i_pgsrr_reserving',
                      opclasses=('range_ops', ),
                      fillfactor=50)
        ]


class PGSRubric(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    tags = ArrayField(base_field=models.CharField(max_length=20), verbose_name='Теги')

    class Meta:
        indexes = [
            models.Index(fields=('name', 'description'),
                         name='i_pgsrubric_name_description',
                         opclasses=('varchar_pattern_ops', 'bpchar_pattern_ops'))
        ]


# class PGSProject(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platforms = ArrayField(base_field=ArrayField(
#         base_field=models.CharField(max_length=20)),
#         verbose_name='Используемые платформы')
#
#
# class PGSProject2(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platforms = HStoreField(verbose_name='Используемые платформы')
#
#
# class PGSProject3(models.Model):
#     name = CICharField(max_length=40, verbose_name='Название')
#     data = JSONField()


def get_timestamp_path(instance, filename):
    # return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
    return f'{datetime.now().timestamp()}{splitext(filename)[1]}'


class Img(models.Model):
    # archive = models.FileField(upload_to='archives/')
    # archive = models.FileField(upload_to='archives/%Y/%m/%d/')
    # archive = models.FileField(upload_to=get_timestamp_path)

    img = models.ImageField(verbose_name='Изображение', upload_to=get_timestamp_path)
    desc = models.TextField(verbose_name='Описание')

    def delete(self, *args, **kwargs):
        self.img.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


# class Comment(models.Model):
#     class Meta:
#         permissions = (
#             ('hide_comment', 'Может скрывать комментарии')
#         )
#         default_permissions = ('change', 'delete')
