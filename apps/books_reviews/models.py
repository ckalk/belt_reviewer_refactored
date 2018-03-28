from __future__ import unicode_literals

from django.db import models

# put AuthorManager and Class first since Book has a dependency

class AuthorManager(models.Manager):
    def author_validator(self, postData):
        print "*** in books models author_validator, postData=", postData

        errors = {}

        #validate author's name -- not empty and doesn't already exist in db
        if len(postData['new_author']) < 1:
            errors["name books"] = "You must enter an author's name"
        elif self.filter(name = postData['new_author']):
            errors["name books"] = "Author's name already in database - choose author from dropdown"
        return errors

    # create an author 
    def create_author(self, clean_data):

        return self.create(
            name=clean_data["new_author"]
        )

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
# *************************
    # Connect an instance of AuthorManager to our Author model overwriting the old hidden objects key with a new one with extra properties
    objects = AuthorManager()
    # *************************
    def __str__(self):
        return '%s' % (self.name)


class BookManager(models.Manager):
    def book_validator(self, postData):
        print "*** in books models book_validator, postData=", postData

        errors = {}

        #validate title -- is one provided and is it unique
        if len(postData['title']) < 1:
            errors["title books"] = "You must enter a title"
        elif self.filter(title = postData['title']):
            errors["title books"] = "Book title already in database"
    
        return errors

    # create a book 
    def create_book(self, clean_data, author_id):

        return self.create(
            title=clean_data["title"],
            author = Author.objects.get(id=author_id)
        )

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    # There can be many books to one (primary) author
    author = models.ForeignKey(Author, related_name = "books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
# *************************
    # Connect an instance of BookManager to our Book model overwriting the old hidden objects key with a new one with extra properties
    objects = BookManager()
    # *************************

    def __str__(self):
        return '%s %s' % (self.title, self.author)