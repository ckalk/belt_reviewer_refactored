from django.conf.urls import url

from . import views

app_name = 'books_reviews'
urlpatterns = [
    url(r'^$', views.user_dashboard, name="dashboard"),
    url(r'^add$', views.new, name="new"),
    url(r'^(?P<book_id>\d+)$', views.show_book, name="showbook"),
    url(r'^createbook$', views.create_book, name="createbook"),
    url(r'^addreview/(?P<book_id>\d+)$', views.add_review, name="addreview"),
    url(r'^delreview/(?P<rev_id>\d+)$', views.del_review, name="delreview"),

]
