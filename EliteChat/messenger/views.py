from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView, status
from django.contrib.auth.decorators import login_required
from .models import Message, Channel
from django.contrib.auth.models import User
from django import forms
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import json
import datetime

def index(request):
    chats = list(Message.objects.all())[-100:]
    channels = list(Channel.objects.all())
    return render(request, 'chatroom.html', {'chats': chats, 'channels': channels})

@csrf_exempt
def post(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == 'send_chat': 
            new_message = Message.objects.create(
                sender=request.user, content = request.POST.get('content'))
            new_message.save()
            return HttpResponse()
        elif post_type == 'get_chat':
            last_chat_id = int(request.POST.get('last_chat_id'))
            chats = Message.objects.filter(id__gt=last_chat_id)
            return render(request, 'chat_list.html', {'chats':chats})

@csrf_exempt
def channel_post(request, channel_id):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == 'send_chat': 
            new_message = Message.objects.create(
            sender=request.user, content = request.POST.get('content'), channel=Channel.objects.get(id=channel_id))
            new_message.save()
            return HttpResponse()
        elif post_type == 'get_chat':
            last_chat_id = int(request.POST.get('last_chat_id'))
            channel = Channel.objects.get(id=channel_id)
            chats = channel.messages.filter(id__gt=last_chat_id)
            return render(request, 'chat_list.html', {'chats':chats})
# Create your views here.
class ChannelForm(forms.Form):
    name1 = forms.CharField(label='Name 1')
    name2 = forms.CharField(label='Name 2')
    name3 = forms.CharField(label='Name 3')
    channel_name = forms.CharField(label='Channel Name')

def create_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            new_channel = Channel.objects.create(name = form.cleaned_data['channel_name'])
            new_channel.save()
            user1 = User.objects.get(username = form.cleaned_data['name1'])
            user2 = User.objects.get(username = form.cleaned_data['name2'])
            user3 = User.objects.get(username = form.cleaned_data['name3'])
            new_channel.add_user(user1)
            new_channel.add_user(user2)
            new_channel.add_user(user3)

            new_message = Message.objects.create(
              sender=request.user, content = "Welcome to new channel!", channel=new_channel)
            new_channel.save()

            return redirect(reverse('index'))
    else:
        form = ChannelForm()
        return render(request, 'create_channel.html', {'form': form})

def channel_message(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    chats = channel.messages.all()
    all_channels = list(Channel.objects.all())
    return render(request, 'chatroom.html', {'channel_id': channel_id, 'channels': all_channels, 'chats': chats})
