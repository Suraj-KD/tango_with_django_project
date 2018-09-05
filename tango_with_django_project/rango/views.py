from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def index(request):
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'boldmessage': "This is About Page"}
    return render(request, 'rango/about.html', context_dict)
