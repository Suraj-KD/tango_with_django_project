from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


# Create your views here.
def index(request):
    category_list = Category.objects.order_by('likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "I am Haguchi"}
    context_dict.update({'categories': category_list, 'pages': page_list})
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'boldmessage': "This is About Page"}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_url):
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name,
                    'category_name_url': category_name_url}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', { 'form': form })


def add_page(request, category_name_url):
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=True)
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render(request, 'rango/add_category.html', {})
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()
    form = PageForm()
    return render(request, 'rango/add_page.html',
                  {'form': form,
                   'category_name_url': category_name_url,
                   'category_name': category_name})


def decode_url(category_name_url):
    category_name = category_name_url.replace('_', ' ')
    return category_name
