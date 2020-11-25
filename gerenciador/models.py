from django.contrib.auth.models import User
from django.db import models


class LinksSalvos(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    link = models.TextField()
