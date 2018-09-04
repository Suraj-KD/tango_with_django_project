from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def index(request):
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return HttpResponse("<center><p>This is  your About Page</p></center>")
