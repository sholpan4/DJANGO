import uuid

from django.db import models


is_all_posts_passive = True


def is_active_default():
    return is_all_posts_passive


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Название", unique=True)

    def __str__(self):
        return self.name #изменение rubric object 1 на недвижимость

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']  #сортировка по имени


class Bb(models.Model):
    # class Kinds(models.TextChoices):
    #     BUY = 'b', 'Куплю'
    #     SELL = 's', 'Продам'
    #     RENT = 'r'
    #     __empty__ = 'Выберите тип обявления'
    #
    # kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.SELL)

    # KINDS = (
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    # KINDS = (
    #     ('Купля-продажа', (
    #         ('b', 'Куплю'),
    #         ('s', 'Продам'),
    #     )),
    #     ('Обмен', (
    #         ('c', 'Обменяю'),
    #     )),
    # )
    KINDS = (
        (None, 'Выберите тип обявления'),
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    )

    # kind = models.CharField(max_length=1, choices=KINDS, default='s')
    kind = models.CharField(max_length=1, choices=KINDS, blank=True)
    rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, verbose_name="Рубрика")  #внешний ключ аргумент должен быть выше если без кавычек
    title = models.CharField(max_length=50, verbose_name="Товар")
    content = models.TextField(null=True, blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена", default=0)
    is_active = models.BooleanField(default=is_active_default)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменено")
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published', 'title']