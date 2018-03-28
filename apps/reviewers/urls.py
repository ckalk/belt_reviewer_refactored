from django.conf.urls import url

from . import views

app_name = 'reviewers'
urlpatterns = [
    url(r'^(?P<user_id>\d+)$', views.show_user, name="showuser"),
]