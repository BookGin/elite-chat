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
    return render(request, 'chatroom.html', {'chats': chats})

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
            channels = Channel.objects.filter()
            return render(request, 'chat_list.html', {'chats':chats, 'channels': channels})

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
            return redirect(reverse('index'))
    else:
        form = ChannelForm()
        return render(request, 'create_channel.html', {'form': form})
