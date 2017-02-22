from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user$', views.create_user),
    url(r'^success$', views.success),
    url(r'^sessions$', views.login_user),
]
