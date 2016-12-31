from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView, status
from django.contrib.auth.decorators import login_required
from .models import Message
import json
import datetime

class UserMessenger(APIView):
    def get(self, request, format=None):
        data = []
        message_obj = Message.objects.all().filter(owner=request.user)
        for obj in message_obj.iterator():
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
