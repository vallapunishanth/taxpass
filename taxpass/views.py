from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def home(request):
    return render(request, template_name='home.html')