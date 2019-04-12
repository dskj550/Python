from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^reg$',reg),
    url(r'^login$',login),
    url(r'^show$',show)
]