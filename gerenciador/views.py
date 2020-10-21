from django.http import HttpResponse
from django.views.generic import FormView

from gerenciador.forms import NewLinkForm


class NewLinkView(FormView):
    template_name = 'gerenciador/new_link.html'
    form_class = NewLinkForm
    success_url = 'teste'

    def form_valid(self, form):
        self.success_url = self.success_url + '?link=' + form.cleaned_data['link']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        if 'form' in kwargs:
            result.update({'mensagem': 'Link inválido'})
        return result


def teste(request):
    return HttpResponse('O link é ' + request.GET['link'])
