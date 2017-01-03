from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django import forms

def home(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login'))
    return render(request, 'home.html')

def landing_page(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    return redirect(reverse('login'))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form': form, })


class ChannelForm(forms.Form):
    name1 = forms.CharField(label='Name 1')
    name2 = forms.CharField(label='Name 2')
    name3 = forms.CharField(label='Name 3')

def create_channel(request):
    if request.method == 'POST':
        #TODO: Client will send 3 userane, transform them into channeid!
    else:
        form = ChannelForm()
        return render(request, 'create_channel.html', {'form': form})
# Create your views here.
