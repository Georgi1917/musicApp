from django.shortcuts import render
from django.views.generic import TemplateView


class MainPage(TemplateView):

    template_name = "index/main-page.html"