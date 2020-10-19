from django import forms


class NewLinkForm(forms.Form):
    link = forms.CharField()

    def valid_link(self):
        return (
            'medium.com' in self.cleaned_data['link']
            and ' ' not in self.cleaned_data['link']
        )

    def is_valid(self):
        return super().is_valid() and self.valid_link()
