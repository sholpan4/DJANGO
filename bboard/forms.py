from django.contrib.auth.models import User
from django import forms
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


class UserDetailsForm(forms.Form):
    user_id = forms.IntegerField(label='User ID', required=True)
