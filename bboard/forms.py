from django.forms import ModelForm
from .models import Bb, Rubric


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        # __all__


class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ('name', )