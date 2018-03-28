from django.shortcuts import render, HttpResponse, redirect

# import object Class(es) from models.py
# from ..books_reviews.models import Books, Reviews
from .models import User

# import messages to use flask error messaging
from django.contrib import messages

# Inside your app's views.py file
from django.core.urlresolvers import reverse


# ************************

# / - display logreg index page (home page) with form to register or sign in (need index template)
def index(request):
    #clear session just to make sure only one person is logged in
    request.session.clear()

    return render(request, 'logreg/index.html')

# ************************

# /login - process data from login form on index page
def login(request):
    print "***** in login route: request.POST = ", request.POST

    # Use validation performed in models.py
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        
        # return to index page with loginerrors
        return redirect(reverse('logreg:index'))

    else:
        user = User.objects.get(email=request.POST["email"])
        request.session['id'] = user.id
        request.session['alias'] = user.alias
        messages.success(request, "Thank you {} for logging in".format(user.name))

        # return to user dashboard
        return redirect(reverse('books:dashboard')) 

# ************************

# /logoff -  log current user off and return to logreg index page
def logoff(request):
    # clean session and return to logreg index page
    request.session.clear()
    return redirect(reverse('logreg:index')) 

# ************************

# /create_user - process data from registration form on index page
def create_user (request):
    print "***** in create_user route: request.POST = ", request.POST

    # Use validation performed in models.py
    errors = User.objects.reg_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        
        # return to index page with register errors
        return redirect(reverse('logreg:index')) 

    else:
        new_user = User.objects.create_user(request.POST)
        request.session['id'] = new_user.id
        request.session['alias'] = new_user.alias
        messages.success(request, "Thank you {} for registering".format(new_user.name))

        # return to user dashboard
        return redirect(reverse('books:dashboard')) 

