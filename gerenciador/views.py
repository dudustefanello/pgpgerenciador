from django.http import HttpResponse
from django.views.generic import FormView, TemplateView

from gerenciador.forms import NewLinkForm


class NewLinkView(FormView):
    template_name = 'gerenciador/new_link.html'
    form_class = NewLinkForm
    success_url = 'text'

    def form_valid(self, form):
        self.success_url = self.success_url + '?link=' + form.cleaned_data['link']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        if 'form' in kwargs:
            result.update({'mensagem': 'Link inválido'})
        return result


class GetLinkText(TemplateView):
    template_name = 'gerenciador/text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'link': self.request.GET['link'] ,'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore, velit sequi tempore, ad voluptatem repellendus nemo veniam officia facere natus provident quisquam ut facilis iure quod vero quos esse accusamus?'})
        return context
