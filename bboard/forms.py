# from django.forms import ModelForm, modelform_factory, DecimalField
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.widgets import Select
from .models import Bb, Rubric


class BbForm(forms.ModelForm):
    title = forms.CharField(label='название товара',
                            validators=[validators.RegexValidator(regex='^.{4,}$')],
                            error_messages={'invalid': 'Слишком короткое название товара!'}
                            )

    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика',
                                    help_text='Не забудь выбрать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))
    datetime = forms.DateField(widget=forms.widgets.SelectDateWidget())
    captcha = CaptchaField(label='Введите текст картинки', error_messages={'invalid': 'Неправильный текст'},
                           # generator='captcha.helper.random_char_challenge',
                           # generator='captcha.helper.math_challenge',
                           generator='captcha.helper.word_challenge',
                           )

    def clean_title(self):
        # val = self.cleaned_data['title']
        val = self.cleaned_data.get('title')
        if val == 'Прошлогдний снег':
            raise ValidationError('К продаже не допускается!')
        return val

    def clean(self):
        super().clean()
        errors = {}

        if not self.cleaned_data.get('content'):
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.cleaned_data.get('price') < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение')
        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Парол', widget=forms.widgets.PasswordInput())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.widgets.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


# полное об #1
# class BbForm(forms.ModelForm):
#     title = forms.CharField(label='Название товара')
#     content = forms.CharField(label='Описание',
#                               widget=forms.widgets.Textarea())
#     price = forms.DecimalField(label='Цена', decimal_places=2)
#     rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
#                                     label='Рубрика',
#                                     help_text='Не забудь выбрать рубрику!',
#                                     widget=forms.widgets.Select(attrs={'size': 8}))
#
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')

# Фабрика классов
# BbForm = modelform_factory(
#     Bb,
#     fields=('title', 'content', 'price', 'rubric'),
#     labels={'title': 'Название товара'},
#     help_texts={'rubric': 'Не забудь выбрать рубрику!'},
#     field_classes={'price': DecimalField},
#     widgets={'rubric': Select(attrs={'size': 8})},
# )

# Быстрые обявления
# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels = {'title': 'Название товара'}
#         help_texts = {'rubric': 'Не забудь выбрать рубрику!'}
#         field_classes = {'price': DecimalField}
#         widgets = {'rubric': Select(attrs={'size': 8})}
# __all__


class RubricForm(forms.ModelForm):
    class Meta:
        model = Rubric
        fields = ('name', )


class RubricBaseFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms
                 if 'name' in form.cleaned_data]
        if ('Недвижимость' not in names) or ('Транспорт' not in names) or ('Мебель' not in names):
            raise ValidationError('Добавьте рубрики недвижимости, транспорта и мебели')


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово', required=True)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')

    captcha = CaptchaField(label='Введите текст картинки', error_messages={'invalid': 'Неправильный текст'})

    error_css_class = 'error'
    required_css_class = 'required'

