"""PSP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static


from peoplestory import views



urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r"^AboutUs/$", views.About, name="about"),
    url(r"^ContactUs/$", views.Contact, name="contact"),
    url(r"^PrivacyPolicy/$", views.PrivacyPolicy, name="privacy_policy"),

    path('accounts/', include('accounts.urls')),
    path('Stories/', include('peoplestory.urls')),
    path('DM/', include('directmessages.urls')),
    #authentication urls
    url('^', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)