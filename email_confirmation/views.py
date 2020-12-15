from django.views.generic import TemplateView
from django.contrib.auth import login

from .models import EmailConfirmation


class EmailConfirmationView(TemplateView):
    template_name = "email/email_confirmation.html"

    def get_context_data(self, **kwargs):
        token = self.request.GET.get('token')
        context = {}
        try:
            user = EmailConfirmation.objects.get(token=token).user
            user.is_active = True
            user.save()
            login(self.request, user)
            context["valid_token"] = True
        except EmailConfirmation.DoesNotExist:
            context["valid_token"] = False
        return context
