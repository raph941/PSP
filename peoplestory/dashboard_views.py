from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from accounts.models import User
from peoplestory.models import Stories
from django.http import HttpResponse
from django.http import JsonResponse


@login_required
def UnpublishedDashboardView(request):
    published_stories = Stories.objects.filter(published=True).filter(denied=False)
    denied_stories = Stories.objects.filter(published=False).filter(denied=True)
    unpublished_stories = Stories.objects.filter(published=False).filter(denied=False)
    all_users = User.objects.all()
    # import pdb; pdb.set_trace()
    context = {
        'published_stories': published_stories,
        'denied_stories': denied_stories,
        'unpublished_stories': unpublished_stories,
        'all_users': all_users,
    }

    return render(request, 'unpublished_dashboard.html', context)


@login_required
def PublishedDashboardView(request):
    published_stories = Stories.objects.filter(published=True).filter(denied=False)
    denied_stories = Stories.objects.filter(published=False).filter(denied=True)
    unpublished_stories = Stories.objects.filter(published=False).filter(denied=False)
    all_users = User.objects.all()
    context = {
        'published_stories': published_stories,
        'denied_stories': denied_stories,
        'unpublished_stories': unpublished_stories,
        'all_users': all_users,
    }

    return render(request, 'published_dashboard.html', context)


@login_required
def DeniedDashboardView(request):
    published_stories = Stories.objects.filter(published=True).filter(denied=False)
    denied_stories = Stories.objects.filter(published=False).filter(denied=True)
    unpublished_stories = Stories.objects.filter(published=False).filter(denied=False)
    all_users = User.objects.all()
    context = {
        'published_stories': published_stories,
        'denied_stories': denied_stories,
        'unpublished_stories': unpublished_stories,
        'all_users': all_users,
    }

    return render(request, 'denied_dashboard.html', context)


@login_required
def UserDashboardView(request):
    published_stories = Stories.objects.filter(published=True).filter(denied=False)
    denied_stories = Stories.objects.filter(published=False).filter(denied=True)
    unpublished_stories = Stories.objects.filter(published=False).filter(denied=False)
    user = User.objects.all()
    all_users = User.objects.all()

    #pagination
    paginator = Paginator(user, 10)
    page = request.GET.get('page', 1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    context = {
        'published_stories': published_stories,
        'denied_stories': denied_stories,
        'unpublished_stories': unpublished_stories,
        'users': users,
        'all_users': all_users,
    }

    return render(request, 'user_dashboard.html', context)


@login_required
def StoryPublishToggle(request, pk):
    if request.method == 'GET':
        story_id = request.GET['story_id']
        obj = get_object_or_404(Stories, pk=story_id)
        obj.published = True
        obj.denied = False
        obj.save()
        publish_status = obj.published
        published_stories = Stories.objects.filter(published=True).filter(denied=False).count()
        denied_stories = Stories.objects.filter(published=False).filter(denied=True).count()
        unpublished_stories = Stories.objects.filter(published=False).filter(denied=False).count()

        data = {
            "publish_status": publish_status,
            "published_stories": published_stories,
            "denied_stories": denied_stories,
            "unpublished_stories": unpublished_stories
        }
        
        return JsonResponse(data)


@login_required
def StoryDenyToggle(request, pk):
    if request.method == 'GET':
        story_pk = request.GET['story_id']
        obj = get_object_or_404(Stories, pk=story_pk)
        obj.published = False
        obj.denied = True
        obj.save()
        publish_status = obj.denied
        published_stories = Stories.objects.filter(published=True).filter(denied=False).count()
        denied_stories = Stories.objects.filter(published=False).filter(denied=True).count()
        unpublished_stories = Stories.objects.filter(published=False).filter(denied=False).count()

        data = {
            "story_pk": story_pk,
            "publish_status": publish_status,
            "published_stories": published_stories,
            "denied_stories": denied_stories,
            "unpublished_stories": unpublished_stories
        }
        
        return JsonResponse(data)


@login_required
def UserActivateToggle(request, pk):
    if request.method == 'GET':
        user_pk = request.GET['user_primarykey']
        obj = get_object_or_404(User, pk=user_pk)
        obj.is_active = True
        obj.save()
        user_is_active = obj.is_active

        data = {
            "user_pk": user_pk,
            "user_is_active": user_is_active,
        }
        
        return JsonResponse(data)


@login_required
def UserDeactivateToggle(request, pk):
    if request.method == 'GET':
        user_pk = request.GET['user_primarykey']
        obj = get_object_or_404(User, pk=user_pk)
        obj.is_active = False
        obj.save()
        user_is_active = obj.is_active

        data = {
            "user_pk": user_pk,
            "user_is_active": user_is_active,
        }
        
        return JsonResponse(data)