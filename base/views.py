from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RoomForm
# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:50]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'room.html', context)

@login_required(login_url='loginuser')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'create_room.html' , context)

@login_required(login_url='loginuser')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'create_room.html', context)

@login_required(login_url='loginuser')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')
    if request.method== 'POST':
        room.delete()
        return redirect ('home')
    
    context = {'obj': room}
    return render(request, 'delete_room.html' ,context )

@login_required(login_url='loginuser')
def delete_message(request,pk):
    message=Message.objects.get(id=pk)
    room_id = message.room.id
    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method == "POST":
        message.delete()
        return redirect('room', pk=room_id)
    context = {'message': message}
    return render(request, 'delete_message.html', context)

def activity(request):
    room_message=Message.objects.all()
    context ={'room_message':room_message}
    return render(request, 'activity.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()

    context = {'user':user, 'rooms': rooms, 'topics': topics, 'room_messages':room_messages}
    return render(request, 'profile.html', context)

def update_user(request,pk):
    return render(request, 'update_user.html')


def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    message = Message.objects.all()
    return render(request, 'topics.html', {'topics': topics,'message' : message})


# Authentications
def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error in logging in, try again"))
            return redirect('loginuser')
    else:
        return render(request, 'loginuser.html')

def logoutuser(request):
    logout(request)
    return redirect('home')

def registeruser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Use 'password1' field
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    context = {'form': form}
    return render(request, 'registeruser.html', context)