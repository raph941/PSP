from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from peoplestory.models import Stories
from django.views.generic import ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

from .forms import NewStoryForm, CommentForm, ContactForm, UpdateStoryForm



def home(request):
    my_stories = Stories.objects.all().order_by('?')
    
    context = {
        'my_stories': my_stories,
    }
    return render(request, 'home.html', context)


def About(request):
    return render(request, 'about.html')


def Contact(request):
    form = ContactForm(request.POST)

    if request.method == 'POST':          
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']

            try:
                send_mail(subject, message, from_email, ['raph941@gmail.com'])
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
            story.save()
            messages.success(request, 'Your story has been successfully createed')

            return redirect('my_stories')
        else:
            messages.warning(request, 'Your story creation was Uncessessful')
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
    my_stories = Stories.objects.all().filter(author_id=pk)

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
    }

    return render(request, 'story_detail.html', context)



