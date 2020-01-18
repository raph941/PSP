from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import render
from . import views


urlpatterns = [
    url(r"^NewStory/$", views.CreateStoryView, name="create_story"),
    url(r"^MyStories/$", views.MyStory, name="my_stories"),
    url(r"^DeleteStory/(?P<pk>\d+)$", views.StoryDeleteView.as_view(), name="story_delete_confirm"),
    url(r"^StoryDetail/(?P<pk>\d+)$", views.StoryDetailView, name="story_detail"),
    url(r"^StoryDetail/(?P<pk>\d+)/EditStory$", views.UpdateStoryView, name="edit_story"),
    url(r"^(?P<pk>\d+)/Story/Like$", views.StoriesLikeToggle.as_view(), name="like"),
    url(r"^SearchResult/$", views.SearchResultView.as_view(), name="search_results"),
    url(r"^Explore/$", views.ExploreView, name="explore"),

]