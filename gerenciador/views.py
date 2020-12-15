import requests

from django.views.generic import FormView, TemplateView, CreateView, ListView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from gerenciador.forms import SignUpForm
from django.urls import reverse_lazy

from gerenciador.forms import NewLinkForm
from gerenciador.models import LinksSalvos
from gerenciador.parser import parse


class NewLinkView(FormView):
    template_name = "gerenciador/new_link.html"
    form_class = NewLinkForm
    success_url = "text"

    def form_valid(self, form):
        self.success_url = self.success_url + "?link=" + form.cleaned_data["link"]
        if 'salvar' in self.request.POST:
            link = LinksSalvos()
            link.link = form.cleaned_data["link"]
            link.user = self.request.user
            link.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        if "form" in kwargs:
            result.update({"mensagem": "Link inválido"})
        return result


class GetLinkText(TemplateView):
    template_name = "gerenciador/text.html"

    def get_link_content(self):
        link = self.request.GET["link"]
        try:
            response = requests.get(link, timeout=2)
            if response.status_code == 200:
                try:
                    content = parse(response.content)
                    if content is None:
                        raise AttributeError
                    return content
                except AttributeError:
                    pass
        except requests.exceptions.Timeout:
            pass
        return "Não foi possível carregar o conteúdo do link informado."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "link": self.request.GET["link"],
                "text": self.get_link_content(),
            }
        )
        return context


class LinkList(ListView):
    model = LinksSalvos
    template_name = 'gerenciador/list_link.html'
    
    
class SignUpView(CreateView):
    template_name = "gerenciador/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')
