from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class DefView(TemplateView):
    template_name = 'cart.html'