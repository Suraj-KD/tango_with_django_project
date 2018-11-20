from django.contrib import admin
from rango.models import Category, Page, UserProfile

# Register your models here.
#admin.site.register(Category)
#admin.site.register(Page)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','url', 'views')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'picture')


admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
