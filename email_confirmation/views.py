from django.shortcuts import render


def email_confirmation(request, token):
    print("token", token)
