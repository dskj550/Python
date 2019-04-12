from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^pub$',pub),
    url(r'^(\d+)$',get),
    url(r'^$',getall)
]