from django.conf.urls import url
from directmessages import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r"^$", views.DirectMessagesView, name="message_url"),
    url(r"^Chat/$", views.ConversationToggleView, name="conversation_url"),
    url(r"^Chat/Post$", views.MessagePostView, name="msg_post_url"),
]
