from django.db import models
from django.contrib.auth.models import User
class Message(models.Model):
    owner = models.ForeignKey(
        User, related_name='owned_message',
    )
    content = models.TextField()
    receiver = models.ManyToManyField(
        User, related_name='received_message',
    )
    time = models.DateTimeField()
    def connect_receiver(self, receiver_name):
        print("receiver_name ", receiver_name)
        self.receiver.add(User.objects.get(username = receiver_name))

# Create your models here.
