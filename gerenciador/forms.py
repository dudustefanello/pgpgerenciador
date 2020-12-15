from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


import re


class NewLinkForm(forms.Form):
    link = forms.URLField()

    def valid_link(self):
        return (re.match('^https://[0-9_a-z.]*medium.com', self.cleaned_data['link']) is not None
                and ' ' not in self.cleaned_data['link'])

    def is_valid(self):
        return super().is_valid() and self.valid_link()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
