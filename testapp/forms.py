from django import forms
from django.core import validators
from django.core.validators import FileExtensionValidator

from .models import Img


class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изоброжение',
                           validators=[
                               validators.FileExtensionValidator(allowed_extensions=('gif', 'jpg', 'png'))],
                           error_messages={'invalid_extension': 'Этот формат не поддерживается'}),
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'
