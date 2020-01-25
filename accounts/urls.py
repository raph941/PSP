from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render

from accounts import views

urlpatterns = [
    url(r"^SignUp/$", views.NewRegularUser, name="signup"),
    url(r"^SignUp/Admin/$", views.NewAdminUser, name="admin_signup"),
    url(r"^MyProfile/(?P<pk>\d+)/$", views.MyProfile, name="myprofile"),  
    url(r"^MyProfile/ProfileUpdate/(?P<pk>\d+)$", views.UserProfileUpdateView, name="profile_update"),  
]
