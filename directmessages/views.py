from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from directmessages.apps import Inbox 
from accounts.models import User
from django.http import JsonResponse
from django.core import serializers
from .forms import MessageForm


@login_required
def DirectMessagesView(request):
    '''conv_partners is a list of users that that you are conversing with'''
    conv_partners = Inbox.get_conversations(request.user)
    form = MessageForm(request.POST)

    context = {
        'conv_partners': conv_partners,
        'form': form
    }

    return render(request, 'messages.html', context)


@login_required
def ConversationToggleView(request):
    if request.method == 'GET':
        user_id = request.GET['user_pk']
        user2 = User.objects.get(pk=user_id)

        temp_msg_obj = Inbox.get_conversation(request.user, user2, limit=None, reversed=False, mark_read=False) 
        if temp_msg_obj.last().sender == request.user:
            msg_obj = Inbox.get_conversation(request.user, user2, limit=None, reversed=False, mark_read=False) 
        else:
            msg_obj = Inbox.get_conversation(request.user, user2, limit=None, reversed=False, mark_read=True) 
            
        data = serializers.serialize("json", msg_obj)
           
        return JsonResponse(data, safe=False)


@login_required
def MessagePostView(request):
    if request.method == 'POST':
        msg_content = request.POST['message']
        reciever_pk = request.POST['reciever_pk']
        user1 = request.user
        user2 = User.objects.get(pk=reciever_pk)

        Inbox.send_message(user1, user2, msg_content)
        message_obj = Inbox.get_conversation(user1, user2, limit=None, reversed=False, mark_read=False)        
        post_data = serializers.serialize("json", message_obj)

        return JsonResponse(post_data, safe=False)


@login_required
def MessagePostFromProfileView(request):
    if request.method == 'POST':
        msg_content = request.POST['message']
        reciever_pk = request.POST['recipient']
        user1 = request.user
        user2 = User.objects.get(pk=reciever_pk)
        post_data = Inbox.send_message(user1, user2, msg_content)
        if post_data[1] == 200:
            data = {
                'status': 'success'
            }
        else:
            data = {
                'status': 'failed',
            }
        return JsonResponse(data, safe=False)
