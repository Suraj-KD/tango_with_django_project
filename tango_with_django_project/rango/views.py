from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Rango Says, Hello World!")


def about(request):
    return HttpResponse("<center><p>This is  your About Page</p></center>")
