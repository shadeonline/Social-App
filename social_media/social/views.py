from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
import requests
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by("-created_at")
        
        return render(request, 'index.html',{"posts": posts})
    else:
        return render(request, 'index.html', {})
    

def user_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'discover.html', {"profiles": profiles})
    else:
        messages.success(request, ("Please try again after logging in."))
        return redirect('/')


def user_profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        posts = Post.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            # Follow or unfollow user
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save profile
            current_user_profile.save()

        return render(request, 'profile.html', {"profile": profile, "posts": posts})

    else:
        messages.success(request, ("Please try again after logging in."))
        return redirect('/')
    

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are logged in"))
            return redirect('/')
        else:
            messages.success(request, ("Log in failed "))

    return render(request, "login.html", {})

def user_logout(request):
    logout(request)
    messages.success(request, ("Successfully logged out"))
    return redirect('/')


def user_signup(request):
    return render(request, "signup.html", {})


# Chat room
def chatroom(request, room_name, pk):
    # Retrieve chat history from database
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)

    chat_messages = ChatMessage.objects.filter(room=room_name).order_by('timestamp')

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chat_messages': chat_messages,
        'profile': profile
    })
