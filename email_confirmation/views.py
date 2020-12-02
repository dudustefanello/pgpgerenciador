from django.views.generic import RedirectView

from .models import EmailConfirmation

class EmailConfirmationView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        token = self.request.GET["token"]
        try:
            user = EmailConfirmation.objects.get(token=token).user
            user.is_active = True
            user.save()
        except EmailConfirmation.DoesNotExist:
            self.pattern_name = 'login'
        return super().get_redirect_url(*args, **kwargs)
