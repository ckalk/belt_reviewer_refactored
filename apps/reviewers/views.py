from django.shortcuts import render, HttpResponse, redirect

# import object Class(es) from models.py
from ..logreg.models import User
from ..books_reviews.models import Book, Author
from .models import Review

# import messages to use flask error messaging
from django.contrib import messages

# Inside your app's views.py file
from django.core.urlresolvers import reverse


# /user/<user_id> - display info about specific reviewer
def show_user(request, user_id):
    print "**** in show_user route"
    
    this_user = User.objects.get(id=user_id)
    this_user_reviews = Review.objects.filter(reviewer=this_user)
    num_reviews = Review.objects.filter(reviewer=this_user).count()

    context = {
        "user": this_user,
        "reviews": this_user_reviews,
        "num_reviews": num_reviews
        }

    return render(request, 'reviewers/show.html', context)
