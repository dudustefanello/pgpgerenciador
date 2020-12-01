"""pgp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from gerenciador.views import NewLinkView, GetLinkText, SignUpView, LinkList
from email_confirmation.views import email_confirmation


urlpatterns = [
    path('', NewLinkView.as_view(), name='index'),
    path('text', GetLinkText.as_view(), name='text'),
    path('list/', LinkList.as_view(), name='list'),
    path('email_confirmation', email_confirmation, name='token_validation'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'),
]
