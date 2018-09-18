from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from rango.models import Category, Page

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "I am bold font from the context"}
    context_dict.update({'categories': category_list, 'pages': page_list})
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'boldmessage': "This is About Page"}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_url):
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)
