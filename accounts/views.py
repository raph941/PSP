from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Value as V
from django.views.generic import ListView
from django.db.models.functions import Concat
from directmessages.apps import Inbox 
from django.http import JsonResponse
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
import cloudinary

from .forms import *
from directmessages.forms import MessageForm
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
            if profile_pic:
                x = form.cleaned_data.get('x')
                y = form.cleaned_data.get('y')
                width = form.cleaned_data.get('width')
                height = form.cleaned_data.get('height')

                image_obj = Image.open(profile_pic)
                cropped_image = image_obj.crop((x, y, width+x, height+y))
                resized_image = cropped_image.resize((400, 420), Image.ANTIALIAS)
                thumb_io = BytesIO()
                resized_image.save(thumb_io, image_obj.format)

                try:
                    response = cloudinary.uploader.upload(ContentFile(thumb_io.getvalue()), folder = "Regular profile_pic")
                    image_url = response['secure_url']  
                except:
                    image_url = "https://res.cloudinary.com/people-shaping-people/image/upload/v1581157209/Default%20Images/head-659651_1920_tfjm1i.png"
                    messages.warning(request, 'your image upload failed, you can resolve this by editing your profile.')
            else:
                image_url = "https://res.cloudinary.com/people-shaping-people/image/upload/v1581157209/Default%20Images/head-659651_1920_tfjm1i.png"

            UserProfile.objects.create(phone_number=phone_number, date_of_birth=date_of_birth,
                                         nationality=nationality, bio=bio,  
                                         profile_pic_url=image_url, user=user)
            
            return redirect('login')
        else:
            form = RegularUserCreationForm()

            #to vary the message to be shown to the user based on the nature of validationerror they make
            username = request.POST['username']
            mail = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if User.objects.filter(email=mail).exists():
                messages.error(request, "A user with thesame Email already exists, if it's you please proceed to Login")
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with thesame Username already exists")
            if password1 and password1 != password2:
                messages.error(request, "passwords did not match")

    return render(request, 'signup_regular.html', {'form': form})


def NewAdminUser(request):
    form = AdminUserCreationForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_regular = False
            user.is_admin = True
            user.save()
            phone_number = form.cleaned_data.get('phone_number')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            nationality = form.cleaned_data.get('nationality')
            bio = form.cleaned_data.get('bio')
            profile_pic = form.cleaned_data.get('profile_pic')
            if profile_pic:
                x = form.cleaned_data.get('x')
                y = form.cleaned_data.get('y')
                width = form.cleaned_data.get('width')
                height = form.cleaned_data.get('height')

                image_obj = Image.open(profile_pic)
                cropped_image = image_obj.crop((x, y, width+x, height+y))
                resized_image = cropped_image.resize((400, 420), Image.ANTIALIAS)
                thumb_io = BytesIO()
                resized_image.save(thumb_io, image_obj.format)

                try:
                    response = cloudinary.uploader.upload(ContentFile(thumb_io.getvalue()), folder = "Admin profile_pic")
                    image_url = response['secure_url']  
                except:
                    image_url = "https://res.cloudinary.com/people-shaping-people/image/upload/v1581157209/Default%20Images/head-659651_1920_tfjm1i.png"
                    messages.warning(request, 'your image upload failed, you can resolve this by editing your profile.')
            else:
                image_url = "https://res.cloudinary.com/people-shaping-people/image/upload/v1581157209/Default%20Images/head-659651_1920_tfjm1i.png"

            UserProfile.objects.create(phone_number=phone_number, date_of_birth=date_of_birth,
                                         nationality=nationality, bio=bio,  
                                         profile_pic_url=image_url, user=user)
            
            return redirect('home')
        else:
            form = RegularUserCreationForm()

            #to vary the message to be shown to the user based on the nature of validationerror they make
            username = request.POST['username']
            mail = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if User.objects.filter(email=mail).exists():
                messages.error(request, "A user with thesame Email already exists, if it's you please proceed to Login")
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with thesame Username already exists")
            if password1 and password1 != password2:
                messages.error(request, "passwords did not match")

    return render(request, 'signup_regular.html', {'form': form})

@login_required
def MyProfile(request, pk): 
    user = get_object_or_404(User, pk=pk) 
    mystory = Stories.objects.filter(author=user)

    context = {
        'user': user,
        'mystory': mystory, 
    }
    
    return render(request, "myprofile.html", context)


@login_required
def UserProfileUpdateView(request, pk): 
    uu_form = UserUpdateForm(request.POST, instance=request.user)
    upu_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
    if request.method == 'POST':
        if uu_form.is_valid and upu_form.is_valid():
            uu_form.save()
            form = upu_form.save(commit=False)

            if upu_form.cleaned_data.get("profile_pic"):
                x = upu_form.cleaned_data.get('x')
                y = upu_form.cleaned_data.get('y')
                width = upu_form.cleaned_data.get('width')
                height = upu_form.cleaned_data.get('height')
                obj = upu_form.cleaned_data.get("profile_pic")

                image_obj = Image.open(obj)
                cropped_image = image_obj.crop((x, y, width+x, height+y))
                resized_image = cropped_image.resize((400, 420), Image.ANTIALIAS)
                thumb_io = BytesIO()
                resized_image.save(thumb_io, image_obj.format)
                #save to cloudinary
                try:
                    if request.user.is_admin:
                        response = cloudinary.uploader.upload(ContentFile(thumb_io.getvalue()), folder = "Admin profile_pic")
                    else:
                        response = cloudinary.uploader.upload(ContentFile(thumb_io.getvalue()), folder = "Regular profile_pic")
                    image_url = response['secure_url']  
                except:
                    image_url = "request.user.userprofile.profile_pic_url"
                    messages.warning(request, 'your image upload failed, you can resolve this by editing your story to add prefered image.')
                
                form.profile_pic_url = image_url
                form.profile_pic.delete()
                form.save()
                messages.success(request, 'Your profile has been successfully updated')
            else:
                form.profile_pic_url = request.user.userprofile.profile_pic_url
                form.save()
            return redirect('myprofile', pk)
        else:
            #to vary the message to be shown to the user based on the nature of validationerror they make
            uu_form = UserUpdateForm(instance=request.user)
            upu_form = UserProfileUpdateForm(instance=request.user.userprofile)
            username = request.POST['username']
            mail = request.POST['email']

            if User.objects.filter(email=mail).exists():
                messages.error(request, "A user with thesame Email already exists, if it's you please proceed to Login")
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with thesame Username already exists")
                
    context = {
        'uu_form': uu_form,
        'upu_form': upu_form,
    }
    return render(request, "profile_update.html", context)


@login_required
def TopAuthors(request):
    queryset = User.objects.all().order_by('?')   
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page', 1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
  
    context = {
        'users': users
    }

    return render(request, 'top_authors.html', context)


class AuthorSearchResultView(ListView):
    template_name = 'author_search_results.html'
    context_object_name = 'searched_result'
    paginate_by = 5
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            or_lookup_authors = (
                Q(full_name__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
                )
            authors_result = User.objects.annotate(
                        full_name=Concat('first_name', V(' '), 'last_name')
                    ).filter(or_lookup_authors)

            return authors_result
        return User.objects.none()          