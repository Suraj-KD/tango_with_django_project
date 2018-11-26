from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(initial=0)
    likes = forms.IntegerField(initial=0)

    class Meta:
        model = Category
        fields = ('name', 'views', 'likes')
        widgets = {'views': forms.HiddenInput(),
                   'likes': forms.HiddenInput()}


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the url  of the page")
    views = forms.IntegerField(initial=0)

    class Meta:
        model = Page
        fields = ('title', 'url', 'views')
        widgets = {'views': forms.HiddenInput()}

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'password': forms.PasswordInput()}


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')