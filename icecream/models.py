from django.db import models


class IceCream(models.Model):
    flavor = models.CharField(max_length=100)
    topping = models.CharField(max_length=100)
    is_vegan = models.BooleanField(default=False)

    def __str__(self):
        return self.flavor
