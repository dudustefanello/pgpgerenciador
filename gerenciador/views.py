from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def showText(request):
    return render(request, 'gerenciador/text.html')