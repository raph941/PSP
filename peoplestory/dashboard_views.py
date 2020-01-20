from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from accounts.models import User
from peoplestory.models import Stories



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