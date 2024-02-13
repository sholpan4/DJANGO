from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User


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
    spares = models.ManyToManyField(Spare, through='Kit', through_fields=('machine', 'spare'))
    notes = GenericRelation('Note')

    def __str__(self):
        return f'{self.name}'

    # class Meta:
    #     ordering = ['name']


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)


# class AditMachine(Machine):
#     car_model = models.CharField(max_length=30)
#     car_year = models.PositiveIntegerField()
#     car_make = models.CharField(max_length=30)
#
#     class Meta(Machine.Meta):
#         abstract = True
#
#
# # class OrdMachine(AditMachine):
# #     class Meta(AditMachine.Meta):
# #         proxy = True
# #         ordering = ['car_year', 'car_make']


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')


class Message(models.Model):
    content = models.TextField()


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, parent_link=True)


# class Message(models.Model):
#     content = models.TextField()
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#         ordering = ['name']
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)
#     email = None
#
#     class Meta(Message.Meta):
#         pass


class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        abstract = True
        ordering = ['name']


class Children(Person):
    age = models.PositiveIntegerField()

    class Meta(Person.Meta):
        pass


class Grandchildren(Children):
    class Meta(Children.Meta):
        proxy = True
        ordering = ['age']
