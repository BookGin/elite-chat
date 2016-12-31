from django.conf.urls import url, include
from django.contrib import admin
from web import views as web_views
from .views import *
urlpatterns = [
    url(r'^get/', include("web.urls"))
]
