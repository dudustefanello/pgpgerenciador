from django import forms

import re


class NewLinkForm(forms.Form):
    link = forms.URLField()

    def valid_link(self):
        return (re.match('^https://[0-9_a-z.]*medium.com', self.cleaned_data['link']) is not None
                and ' ' not in self.cleaned_data['link'])

    def is_valid(self):
        return super().is_valid() and self.valid_link()
