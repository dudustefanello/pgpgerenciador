from django import forms


class NewLinkForm(forms.Form):
    link = forms.URLField()

    def valid_link(self):
        return (
            'https://medium.com' in self.cleaned_data['link'][:18]
            and ' ' not in self.cleaned_data['link']
        )

    def is_valid(self):
        return super().is_valid() and self.valid_link()
