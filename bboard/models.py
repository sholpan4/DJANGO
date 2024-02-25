import uuid

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from precise_bbcode.fields import BBCodeTextField
from localflavor.generic.models import PhoneNumberField

is_all_posts_passive = True


def is_active_default():
    return is_all_posts_passive


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное',
                              code='odd',
                              params={'value': val}
                              )


class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError(
                'Введенное число должно находиться в диапазоне от %(min)s до %(max)s',
                code='out_of_range',
                params={'min': self.min_value, 'max': self.max_value}
            )


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(cnt=models.Count('bb')).order_by('-cnt')
    # Rubric.objects.all().order_by_bb_count()


class RubricManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().order_by('-order', '-name')
        return RubricQuerySet(self.model, using=self._db)

    def order_by_bb_count(self):
        # return super().get_queryset().annotate(cnt=models.Count('bb')).order_by('-cnt')
        return self.get_queryset().order_by_bb_count()


class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Название", unique=True)
    order = models.SmallIntegerField(default=0, db_index=True)
    objects = models.Manager.from_queryset(RubricQuerySet)()
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.name #изменение rubric object 1 на недвижимость

    def get_absolute_url(self):
        return f"/{self.pk}/"

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['order', 'name']  #сортировка по имени


class RevRubric(Rubric):
    class Meta:
        proxy = True
        ordering = ['-name']


class Bb(models.Model):
    KINDS = (
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    )

    kind = models.CharField(max_length=1, choices=KINDS, default='s', verbose_name='Тип объявления')
    rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, verbose_name="Рубрика")  #внешний ключ аргумент должен быть выше если без кавычек
    title = models.CharField(
        # unique=True
        max_length=50,
        verbose_name="Товар",
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Это мы сами написали'}
      )

    content = models.TextField(null=True, blank=True, verbose_name="Описание")

    # content = BBCodeTextField(null=True, blank=True, verbose_name="Описание")

    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name="Цена",
                                default=0,
                                )
    is_active = models.BooleanField(default=is_active_default)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменено")
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.title}'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if errors:
            raise ValidationError(errors)

    def clean_title(self):
        errors = {}
        if self.title == "Car":
            errors['title'] = ValidationError('Бобры не продаются, родина в них нуждается')
        if errors:
            raise ValidationError(errors)

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price:.2f})'
        return self.title

    # title_and_price.short_description = 'Название и цена'

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published', 'title']
        # order_with_respect_to = 'rubric' #возвращать отсортированный список с рубрикой
