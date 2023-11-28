# from django.db import models
# from django.contrib.auth.models import User


# class AdvUser(models.Model):
#     is_activated = models.BooleanField(default=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


# class Spare(models.Model):
#     name = models.CharField(max_length=30)


# class Machine(models.Model):
#     name = models.CharField(max_length=30)
#     spares = models.ManyToManyField(Spare)


from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Человек'
        verbose_name = 'Люди'
        ordering = ['name']


class Child(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Person, on_delete=models.CASCADE)
    toys = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ребенок'
        verbose_name = 'Дети'
        ordering = ['name']


class IceCream(models.Model):
    flavor = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.flavor

    class Meta:
        verbose_name_plural = 'Мороженые'
        verbose_name = 'Мороженое'
        ordering = ['flavor']


class IceCreamParlor(models.Model):
    parlor = models.CharField(max_length=200)
    ice_creams = models.ManyToManyField(IceCream)

    def __str__(self):
        return self.parlor

    class Meta:
        verbose_name_plural = 'Киоски'
        verbose_name = 'Киоск'
        ordering = ['parlor']
