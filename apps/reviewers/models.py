from __future__ import unicode_literals

from django.db import models

from ..books_reviews.models import Book

from ..logreg.models import User

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        print "*** in reviewers models review_validator, postData=", postData

        errors = {}

        #validate review -- is one provided
        if len(postData['review']) < 1:
            errors["review reviewers"] = "You must enter a review"
 
        # you could also check and see if the logged in user has already left a review for this book, but I'm not going to check that
    
        return errors


class Review(models.Model):
    review = models.TextField(max_length=2000)
    rating = models.IntegerField()
    # There can be many reviews to one book
    book = models.ForeignKey(Book, related_name = "reviews")
    # There can be many reviews by one user
    reviewer = models.ForeignKey(User, related_name = "reviewer_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
# *************************
    # Connect an instance of ReviewManager to our Review model overwriting the old hidden objects key with a new one with extra properties
    objects = ReviewManager()
    # *************************

    def __str__(self):
        return '%s %s %s %s' % (self.review, self.rating, self.book, self.reviewer)