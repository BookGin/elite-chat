from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView, status
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
import json
import datetime

class UserMessenger(APIView):
    def get(self, request, format=None):
        data = []
        user = User.objects.get(username=request.user)
        print(request.user)
        for obj in user.owned_message.all().iterator():
            data.append({"content" : obj.content, "time": obj.time})
        for obj in user.received_message.all().iterator():
            data.append({"content" : obj.content, "time": obj.time})
        print(data)
        return HttpResponse(data)

    def post(self, request, format=None):
        response = {}
        data = request.data
        print(data)
        message = Message(
            owner=request.user, content = data['content'], time=datetime.datetime.now()
        )
        message.save()

        message.connect_receiver(data['receiver'])
        return JsonResponse(response)
# Create your views here.
