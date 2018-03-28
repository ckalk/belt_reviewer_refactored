from django.conf.urls import url

from . import views

app_name = 'logreg'
urlpatterns = [
	url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^create_user$', views.create_user, name="register"),
    url(r'^logoff$', views.logoff, name="logoff"),
]