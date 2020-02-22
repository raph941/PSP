from urllib.parse import quote_plus
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from peoplestory.models import Stories
from django.views.generic import ListView, DeleteView, DetailView, RedirectView
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from io import BytesIO
import cloudinary

from .forms import NewStoryForm, CommentForm, ContactForm, UpdateStoryForm


def home(request):
    my_stories_query = Stories.objects.all().order_by('?')
    paginator = Paginator(my_stories_query, 18)
    page = request.GET.get('page', 1)

    try:
        my_stories = paginator.page(page)
    except PageNotAnInteger:
        my_stories = paginator.page(1)
    except EmptyPage:
        my_stories = paginator.page(paginator.num_pages)
  
    context = {
        'my_stories': my_stories,
    }
    return render(request, 'home.html', context)


class SearchResultView(ListView):
    template_name = 'search_results.html'
    context_object_name = 'searched_result'
    paginate_by = 5
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            or_lookup_stories = (
                Q(full_name__icontains=query) |
                Q(story__icontains=query)
                )
            stories_result = Stories.objects.filter(or_lookup_stories)


            return stories_result
        return Stories.objects.none()      


def About(request):
    return render(request, 'about.html')


def Contact(request):
    form = ContactForm(request.POST)

    if request.method == 'POST':          
        if form.is_valid():
            subject = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']

            try:
                send_mail(from_email, message, from_email, ['peopleshapingpeople@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, 'Your message has been sent successfully, you would recieve a response very soon!')
  
            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, 'message was Unsuccessfully')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


@login_required
def CreateStoryView(request):  
    form = NewStoryForm(request.POST, request.FILES)

    if request.method == 'POST':   
 
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user

            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')

            image_obj = Image.open(story.image)
            cropped_image = image_obj.crop((x, y, width+x, height+y))
            resized_image = cropped_image.resize((400, 420), Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image_obj.format)
            
            #save to cloudinary
            try:
                response = cloudinary.uploader.upload(ContentFile(thumb_io.getvalue()), folder = "story_image")
                image_url = response['secure_url']  
            except:
                image_url = "https://res.cloudinary.com/people-shaping-people/image/upload/v1581281253/Default%20Images/fantasies-4063346_640_fbaaqb.jpg"
                messages.warning(request, 'your image upload failed, you can resolve this by editing your story to add prefered image.')
            
            story.image_url = image_url
            story.image.delete()            
            story.save()
            
            messages.success(request, 'Your story has been successfully created')

            return redirect('my_stories')
        else:
            messages.warning(request, 'Your story creation was Unsucessful')
    else:

        form = NewStoryForm()

    return render(request, 'create_story.html', {'form': form})


@login_required
def UpdateStoryView(request, pk):
    story = Stories.objects.get(pk=pk)  
    form = UpdateStoryForm(request.POST, request.FILES, instance=story)

    if request.method == 'POST':          
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user

            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')

            image_obj = Image.open(story.image)
            cropped_image = image_obj.crop((x, y, width+x, height+y))
            resized_image = cropped_image.resize((400, 420), Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image_obj.format)
            

            response = cloudinary.uploader.upload(ContentFile(thumb_io.getvalue()), folder = "story_image")
            image_url = response['secure_url']  
            
            story.image_url = image_url
            story.image.delete()            

            story.save()
            messages.success(request, 'Your story has been successfully Updated')

            return redirect('story_detail', pk)
        else:
            messages.warning(request, 'Your story creation was Not Uncessessful')
    else:
        form = UpdateStoryForm(instance=story)

    context = {
        'form': form,
        'story': story,
    }

    return render(request, 'edit_story.html', context)


@login_required
def MyStory(request):
    pk = request.user.id
    my_stories_query = Stories.objects.all().filter(author_id=pk)

    paginator = Paginator(my_stories_query, 9)
    page = request.GET.get('page', 1)

    try:
        my_stories = paginator.page(page)
    except PageNotAnInteger:
        my_stories = paginator.page(1)
    except EmptyPage:
        my_stories = paginator.page(paginator.num_pages)

    context = {
        'my_stories': my_stories,
    }

    return render(request, 'my_stories.html', context)

class StoryDeleteView(DeleteView):
    model = Stories
    success_url = reverse_lazy('my_stories')
    template_name = 'story_delete.html'


def StoryDetailView(request, pk):
    story = Stories.objects.get(pk=pk)
    story.views += 1
    story.save()
    form = CommentForm(request.POST)
    share_string = quote_plus(story.story_caption)
    popular_stories = Stories.objects.all().order_by('-views')[:5]

    if form.is_valid():
        comment = form.save(commit=False)
        comment.comment_author = request.user
        comment.story = story
        comment.save()
        return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()

    context = {
        'story': story,
        'form': form,
        'share_string': share_string,
        'popular_stories': popular_stories
    }

    return render(request, 'story_detail.html', context)


login_required   
def StoriesLikeToggle(request, pk):
    if request.method == 'GET':
        story_id = request.GET['story_id']
        obj = get_object_or_404(Stories, pk=story_id)
        user = request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
                NewLikes = obj.likes.count()
            else:
                liked = True
                obj.likes.add(user)
                NewLikes = obj.likes.count()
            updated = True
        data = {
            "story_id": story_id,
            "updated": updated,
            "NewLikes": NewLikes,
            "liked": liked
        }
        return JsonResponse(data)

        
def ExploreView(request):
    recent_stories = Stories.objects.all().order_by('-last_updated')[:9]
    my_stories_query = Stories.objects.all().order_by('-views')
    paginator = Paginator(my_stories_query, 6)
    page = request.GET.get('page', 1)

    try:
        my_stories = paginator.page(page)
    except PageNotAnInteger:
        my_stories = paginator.page(1)
    except EmptyPage:
        my_stories = paginator.page(paginator.num_pages)
  
    context = {
        'my_stories': my_stories,
        'recent_stories': recent_stories,
    }

    return render(request, 'explore.html', context)

    


