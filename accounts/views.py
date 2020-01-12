from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django import forms
from django.contrib.auth import views as auth_views

from .forms import *
from .models import UserProfile, User
from peoplestory.models import Stories


def NewRegularUser(request):
    form = RegularUserCreationForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_regular = True
            user.save()
            phone_number = form.cleaned_data.get('phone_number')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            nationality = form.cleaned_data.get('nationality')
            bio = form.cleaned_data.get('bio')
            profile_pic = form.cleaned_data.get('profile_pic')

            UserProfile.objects.create(phone_number=phone_number, date_of_birth=date_of_birth,
                                         nationality=nationality, bio=bio,  
                                         profile_pic=profile_pic, user=user)
            messages.success(request, "successfully Created")
            return redirect('login')
        else:
            messages.error(request, "user was not successfully Created")
            form = RegularUserCreationForm()

    return render(request, 'signup_regular.html', {'form': form})



@login_required
def MyProfile(request, pk): 
    user = User.objects.get(pk=pk) 
    mystory = Stories.objects.filter(author=user)

    context = {
       'mystory': mystory, 
    }
    
    return render(request, "myprofile.html", context)


@login_required
def UserProfileUpdateView(request, pk): 
    if request.method == 'POST':
        uu_form = UserUpdateForm(request.POST, instance=request.user)
        upu_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if uu_form.is_valid and upu_form.is_valid():
            uu_form.save()
            upu_form.save()
            return redirect('myprofile', pk)
    else:
        uu_form = UserUpdateForm(instance=request.user)
        upu_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'uu_form': uu_form,
        'upu_form': upu_form,
    }
    return render(request, "profile_update.html", context)