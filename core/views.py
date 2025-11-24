from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Página inicial do projeto My Tools Backend"""
    return render(request, 'home.html')
