import requests
from django.views.generic import FormView, TemplateView

from gerenciador.forms import NewLinkForm
from gerenciador.parser import parse


class NewLinkView(FormView):
    template_name = "gerenciador/new_link.html"
    form_class = NewLinkForm
    success_url = "text"

    def form_valid(self, form):
        self.success_url = self.success_url + "?link=" + form.cleaned_data["link"]
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
