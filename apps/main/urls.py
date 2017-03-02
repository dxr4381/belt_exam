from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user$', views.create_user),
    url(r'^success$', views.success),
    url(r'^sessions$', views.login_user),
    url(r'^log_out$', views.log_out),
    url(r'^submit$', views.submit),
    url(r'^list/(?P<id>\d+)$', views.list),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^profile/(?P<id>\d+)$', views.profile),
    url(r'^home$', views.home),

 ]
