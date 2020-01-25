from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import render
from . import views
from . import dashboard_views


urlpatterns = [
    url(r"^NewStory/$", views.CreateStoryView, name="create_story"),
    url(r"^MyStories/$", views.MyStory, name="my_stories"),
    url(r"^DeleteStory/(?P<pk>\d+)$", views.StoryDeleteView.as_view(), name="story_delete_confirm"),
    url(r"^StoryDetail/(?P<pk>\d+)$", views.StoryDetailView, name="story_detail"),
    url(r"^StoryDetail/(?P<pk>\d+)/EditStory$", views.UpdateStoryView, name="edit_story"),
    url(r"^(?P<pk>\d+)/Story/Like$", views.StoriesLikeToggle, name="like"),
    url(r"^SearchResult/$", views.SearchResultView.as_view(), name="search_results"),
    url(r"^Explore/$", views.ExploreView, name="explore"),

    #dashboard urls
    url(r"^Dashboard/Upublished/$", dashboard_views.UnpublishedDashboardView, name="unpublished_dashboard"),
    url(r"^Dashboard/Published/$", dashboard_views.PublishedDashboardView, name="published_dashboard"),
    url(r"^Dashboard/Denied/$", dashboard_views.DeniedDashboardView, name="denied_dashboard"),
    url(r"^Dashboard/User/$", dashboard_views.UserDashboardView, name="user_dashboard"),
    url(r"^Dashboard/User/Publish/(?P<pk>\d+)$", dashboard_views.StoryPublishToggle, name="publish"),
    url(r"^Dashboard/User/Deny/(?P<pk>\d+)$", dashboard_views.StoryDenyToggle, name="deny"),
    url(r"^Dashboard/User/Activate/(?P<pk>\d+)$", dashboard_views.UserDeactivateToggle, name="deactivate"),
    url(r"^Dashboard/User/Deactivate/(?P<pk>\d+)$", dashboard_views.UserActivateToggle, name="activate"),

]