"""EliteChat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from web import views as web_views
from messenger.views import UserMessenger
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', web_views.landing_page, name="landing_page"),
    url(r'^web/', include("web.urls")),
    url(r'^messenger/', include("web.urls")),
    url(r'^message/', UserMessenger.as_view())
]
