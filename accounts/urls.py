from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render

from accounts import views

urlpatterns = [
    url(r"^SignUp/$", views.NewRegularUser, name="signup"),
    url(r"^MyProfile/(?P<pk>\d+)/$", views.MyProfile, name="myprofile"),  
]
