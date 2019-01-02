from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


# Create your views here.
def index(request):
    category_list = Category.objects.order_by('likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "Please Login"}
    context_dict.update({'categories': category_list, 'pages': page_list})
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    #return render(request, 'rango/index.html', context_dict)
    #response = render(request, 'rango/index.html', context_dict)
    # Get the number of visits to site
    # we use COOKIES.get() function to obtain visits cookie
    # If the cookie exists, the value returned is casted to an integer
    # If the cookie doesn't exists, we default to zero and cast it.
    #visits = int(request.COOKIES.get('visits', '0'))

    # getting visits count using session
    visits = request.session.get('visits')

    # If visitor is visiting the site for 1st time, set visits count to 1
    if not visits:
        visits = 1

    # Set this flag to False after every new session get started
    reset_last_visit_time = False
    
    # get the last visit if it exists in cookie
    last_visit = request.session.get('last_visit')
    
    if last_visit:
        # Set the current time as last visit time to the site
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # Increse the no of visit by 1 to site if page is refreshed after 5 sec
        if (datetime.now() - last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        # update last_visit and visits value in cookie with latest value
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    
    context_dict['visits'] = visits
    return render(request, 'rango/index.html', context_dict)
    '''
    # Does the cookie last_visit exist?
    if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value
        last_visit = request.COOKIES['last_visit']
        # Cast the value to Python DateTime object
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # If it has been more than one day since the last visit...
        if (datetime.now() - last_visit_time).seconds > 5:
            # ...reassign the value of the cookie to +1 of what it was before...
            response.set_cookie('visits', visits+1)
            # ...and update the last visit cookie, too.
            response.set_cookie('last_visit', datetime.now())
        else:
            response.set_cookie('last_visit', datetime.now())
    else:
        # Cookie last_visit doesn't exists, so create it on to the current date/time
        response.set_cookie('last_visit', datetime.now())

    # Return the response back to the user, updating any cookies that need changed
    return response
    '''

def about(request):
    context_dict = {'boldmessage': "This is About Page"}
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict['visits'] = count
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

@login_required()
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

@login_required()
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


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        #  Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid..
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to database
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance .
            profile.save()

            # Update our variable to tell the template registration was successful
            registered = True
            # After successful registeration return to Home page
            return redirect('index')
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', {'user_form': user_form,
                                                   'profile_form': profile_form,
                                                   'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        #  This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is account active? It could have been disabled
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user=user)
                return redirect('index')
            else:
                # An inactive account was used - no logging in!
                return HttpResponseRedirect('Your Rango account was disabled.')
        else:
            # Bad login credentials were provided, so we can't loh the user in
            print("Invalid login credential username : {0}, password: {1}".format(username, password))
            return HttpResponseRedirect("Invalid login details provided")
    # The request is not HTTP POST, so display the login form,
    # This scenario would most likely to be HTTP GET
    else:
        # No context variable to pass to template,so paas the empty dictionary object
        return render(request, 'rango/login.html', {})


@login_required()
def user_logout(request):
    # Since we already know user is logged in, so we simply loging out
    logout(request)
    return redirect('index')
