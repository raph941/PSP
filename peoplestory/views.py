from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from peoplestory.models import Stories
from django.views.generic import ListView, DeleteView, DetailView
from django.urls import reverse_lazy

from .forms import NewStoryForm, CommentForm



def home(request):
    my_stories = Stories.objects.all()

    context = {
        'my_stories': my_stories,
    }
    return render(request, 'home.html', context)


def About(request):
    return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')


@login_required
def CreateStoryView(request):  
    form = NewStoryForm(request.POST, request.FILES)

    if request.method == 'POST':          
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()

            return redirect('my_stories')
        else:
            form = NewStoryForm()

    return render(request, 'create_story.html', {'form': form})


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



