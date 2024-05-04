from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class AttractionForm(forms.Form):
    name = forms.CharField(label='название')
    img_link = forms.CharField(label='ссылка на картинку')
    address = forms.CharField(label='адрес', required=False)
    latitude = forms.CharField(label='latitude', required=False)
    longitude = forms.CharField(label='longitude', required=False)
    short_description = forms.CharField(widget=forms.Textarea(), label='описание', required=False)


class RouteForm(forms.Form):
    route_name = forms.CharField(label='Название маршрута', max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'Мой маршрут'}))
    route_text = forms.CharField(label='Описание', max_length=500,
                                 widget=forms.TextInput(attrs={'placeholder': 'Описание'}))
    points = forms.CharField(label="Достопримечательности", widget=forms.Textarea(
        attrs={'placeholder': 'Адрес или название 1\nАдрес или название 2\nАдрес или название 3\nи т.д.'}))
    route_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class CurRouteForm(forms.Form):
    max_time = forms.IntegerField(label='Время маршрута в минутах', required=False)
