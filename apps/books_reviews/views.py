from django.shortcuts import render, HttpResponse, redirect

# import object Class(es) from models.py

from .models import Book, Author
from ..reviewers.models import Review
from ..logreg.models import User


# import messages to use flask error messaging
from django.contrib import messages

# Inside your app's views.py file
from django.core.urlresolvers import reverse

# ****************************************************
# /books - display user welcome page after login (need index template)
def user_dashboard(request):
    print "**** in user_dashboard route --welcome page"
    context = {
        "last3_reviews": Review.objects.filter().order_by('-id')[:3],
        "books_w_reviews": Review.objects.values_list('book__id', 'book__title').distinct().order_by('book__title')
        }

    return render(request, 'books_reviews/index.html', context)


# ****************************************************
# /books/add - display page with form to add a book (need new template)
def new(request):
    print "**** in books new route"
    context = {
        "author_list": Author.objects.all()
        }
    return render(request, 'books_reviews/new.html', context)


# ****************************************************
# /books/<book_id> - display info and reviews of specific book (need a show template)
def show_book(request, book_id):
    print "**** in show_book route"

    this_book = Book.objects.get(id=book_id)
    this_book_reviews = Review.objects.filter(book=this_book)

    context = {
        "book": this_book,
        "reviews": this_book_reviews 
        }
        
    return render(request, 'books_reviews/show.html', context)


# ****************************************************
# /books/createbook - process foradding a book and author (and then a review)
def create_book(request):
    print "***** in create_book route: request.POST = ", request.POST

    # if something was entered in the new_author form field, first process new author
    if len(request.POST['new_author']) > 0:
        errors = Author.objects.author_validator(request.POST)

        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        
            # return to books new page with new_author errors
            return redirect(reverse('books:new')) 

        # if new_author has no validation errors, add new author
        author = Author.objects.create_author(request.POST)
        messages.success(request, "Thank you for adding author {}".format(author.name))
    
    else:
        # get id of selected author for creating book
        author = Author.objects.get(name=request.POST['author_name'])

    # now process new book title, first see if validation errors
    errors = Book.objects.book_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        
        # return to books new page with book title errors
        return redirect(reverse('books:new')) 
     
    # if new book has no validation errors, add new book by author
    new_book = Book.objects.create_book(request.POST, author.id)
    book_id = new_book.id
    messages.success(request, "Thank you for adding book title {}".format(new_book.title))

# process new review of book_id, first see if validation errors
    errors = Review.objects.review_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        
        # go to new book page with review errors
        return redirect(reverse('books:new')) 
     
    # if review has no validation errors, add review to book by logged in user
    user_id = request.session['id']
    # print "***in create_book: request.POST="
    # print "*** book_id=", book_id, " user_id=", user_id
    review = request.POST['review']
    rating = request.POST['rating']
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=user_id)
    
    Review.objects.create(review=review,rating=rating, reviewer=user, book=book)
    messages.success(request, "Thank you for adding a book review")

    # if adding book, author and review was successful, go to books:show
    return redirect(reverse('books:showbook', args=(book_id,)))


# ****************************************************
# /books/addreview- process review to add to book
def add_review(request, book_id):
    print "**** in books add_review route, request=", request

    # process new review of book_id, first see if validation errors
    errors = Review.objects.review_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        
        # go to show book page with review errors
        return redirect(reverse('books:showbook', args=(book_id,)))
     
    # if review has no validation errors, add review to book by logged in user
    user_id = request.session['id']
    review = request.POST['review']
    rating = request.POST['rating']
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=user_id)
    
    Review.objects.create(review=review,rating=rating, reviewer=user, book=book)
    messages.success(request, "Thank you for adding a review")

    # return to books:show
    return redirect(reverse('books:showbook', args=(book_id,)))


# ****************************************************
# /books/delreview/<rev_id> - process deleting a review of specific book, but only by user who created the review
def del_review(request, rev_id):
    print "**** in del_review route"
    
    review = Review.objects.get(id=rev_id)
    book_id = review.book.id
    review.delete()
    
    messages.success(request, "Your review has been deleted")

    return redirect(reverse('books:showbook', args=(book_id,))) 