from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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


# def StoryLikeRedirectView(request, pk):
#     story = Stories.objects.get(pk=pk)
#     return HttpResponseRedirect(request.path_info)


class StoriesLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Stories, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_
        

