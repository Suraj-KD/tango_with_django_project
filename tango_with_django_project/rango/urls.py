from django.urls import path, re_path
from rango import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    re_path(r'category/(?P<category_name_url>\w+)$',
            views.category, name='category'),
    re_path(r'category/(?P<category_name_url>\w+)/add_page/$',
            views.add_page, name="add_page"),
    re_path(r'^add_category/$', views.add_category,
            name='add_category')
]
