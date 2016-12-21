from django.urls import reverse
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def landing_page(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    return redirect(reverse('login'))
# Create your views here.
