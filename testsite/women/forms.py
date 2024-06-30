from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутсвовать только русские символы, дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, self.code)



# class AddPostForm(forms.Form):
    # '''
    # Форма не связанная с моделью
    # '''
    # title = forms.CharField(max_length=255, min_length=5,
    #                         label='Заголовок',
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         error_messages={
    #                             'min_length': 'Слишком короткий заголовок',
    #                             'required': 'Поле обязательно',
    #                         })
    # slug = forms.SlugField(max_length=255, label='URL',
    #                        validators=[
    #                            MinLengthValidator(5, message='Минимум 5 символов'),
    #                            MaxLengthValidator(100,  message='Максимум 100 символов'),
    #                        ])
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    # is_published = forms.BooleanField(required=False, initial=True, label='Статус')
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана',
    #                              label='Категории')
    # husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не замужем',
    #                                  label='Муж')

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- '
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError('Должны присутсвовать только русские символы, дефис и пробел')

class AddPostForm(forms.ModelForm):
    '''
    Форма связанная с моделью
    '''


    #is_published = forms.BooleanField(required=False, initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана',
                                 label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не замужем',
                                     label='Муж')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {
            'slug': 'URL'
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')





