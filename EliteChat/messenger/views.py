from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView, status
from django.contrib.auth.decorators import login_required
from .models import Message, Channel
from django.contrib.auth.models import User
from django import forms
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.conf import settings
from django.utils.encoding import smart_str
from pathlib import Path
import os
import string
import random
import json
import datetime

def index(request):
    user_channel, created = Channel.objects.get_or_create(name=request.user.username)
    if created:
        user_channel.save()
        user_channel.add_user(request.user)
        init_msg = Message.objects.create(
              sender=request.user, content = "Welcome! try to type something", channel=user_channel)
        init_msg.save()
    chats = list(user_channel.messages.all())[-100:]
    channels = list(request.user.belonged_channel.all())
    return render(request, 'chatroom.html', {'chats': chats, 'channels': channels})

@csrf_exempt
def post(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == 'send_chat': 
            new_message = Message.objects.create(
                sender=request.user, content = request.POST.get('content'),
                channel=Channel.objects.get_or_create(name=request.user.username))
            new_message.save()
            return HttpResponse()
        elif post_type == 'get_chat':
            last_chat_id = int(request.POST.get('last_chat_id'))
            channel = Channel.objects.get(name=request.user.username)
            chats = channel.messages.filter(id__gt=last_chat_id)
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
    all_channels = list(request.user.belonged_channel.all())
    return render(request, 'chatroom.html', {'channel_id': channel_id, 'channels': all_channels, 'chats': chats})

class UploadFileForm(forms.Form):
    file = forms.FileField()

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            rand_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
            print(repr(request.FILES['file']))
            filename = rand_str + os.path.splitext(request.FILES['file'].name)[1]
            path = settings.BASE_DIR + '/uploadfiles/' + filename
            with open(path, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            return HttpResponse(filename)
        return HttpResponse("UPLOAD FAIL")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def get_file(request, file_id):
    filepath = settings.BASE_DIR + '/uploadfiles/' + file_id
    if Path(filepath).is_file():
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_id)
        response['X-Sendfile'] = smart_str(filepath)
        with open(filepath, 'rb') as f:
            response.write(f.read())
            return response
    return HttpResponse("No such file!")
