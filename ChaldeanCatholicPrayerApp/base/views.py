from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from .models import Room, Topic, Comment, userProfile
from .forms import RoomForm, CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



#rooms = [
#    {'id': 1, 'name': 'Rumsha Prayers'},
#    {'id': 2, 'name': 'Pray the Rosary'},
#    {'id': 3, 'name': 'Mass Liturgy'},
#]

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Login')

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            name = form.cleaned_data.get('name')
            bio = form.cleaned_data.get('bio')
            profile_pic = form.cleaned_data.get('profile_pic')
            user_profile = userProfile.objects.create(
                user=user,
                name=name,
                userName=user.username,
                biography=bio,
                profile_pic=profile_pic
            )

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)
    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.annotate(num_rooms=Count('room')).order_by('-num_rooms')[:5]

    room_count = rooms.count()
    room_comments = Comment.objects.filter(Q(room__topic__name__icontains=q))

    profile = None
    if request.user.is_authenticated:
        profile = userProfile.objects.get(user=request.user)

    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)

    context = {'rooms' : rooms, 'topics' : topics, 'room_count':room_count, 'room_comments':room_comments, 'profile':profile, 'user_profile':user_profile}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_comments = room.comment_set.all().order_by('-created')
    commenters = room.commenters.all()
    other_rooms = Room.objects.exclude(id=pk)[:9]

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)
    
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)


    context = {'room': room, 'room_comments':room_comments, 'commenters':commenters, 'other_rooms': other_rooms, 'user_profile':user_profile}
    return render(request, 'base/room.html', context)

def createProfile(request, pk):
    user = User.objects.get(id=pk)
    comments = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'comments': comments, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)


    context = {'form': form, 'user_profile':user_profile}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)

    context = {'form': form, 'user_profile':user_profile}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)

    context = {'user_profile':user_profile, 'obj':room}

    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteComment(request,pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You are not able to perform this deletion')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)
    
    context = {'user_profile':user_profile,'obj':comment}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    profile = userProfile.objects.get(user=user)

    madeData = {'bio':profile.biography, 'name':profile.name, 'profilePic': profile.profile_pic}
    form = CustomUserUpdateForm(instance=user, initial = madeData)

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save(commit = False)
            user.save()

            name = form.cleaned_data.get('name')
            bio = form.cleaned_data.get('bio')
            profile_pic = form.cleaned_data.get('profile_pic')
            profile.name = name
            profile.biography = bio
            
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            return redirect('user-profile', pk=user.id)
        
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)

    context = {'form':form, 'profile':profile, 'user_profile':user_profile}
    return render(request, 'base/update_user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    topics = Topic.objects.annotate(num_rooms=Count('room')).order_by('-num_rooms')

    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)

    context = {'user_profile':user_profile, 'topics':topics}

    return render(request, 'base/topics.html', context)

def activityPage(request):
    
    room_comments = Comment.objects.all()
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)

    context = {'user_profile':user_profile, 'room_comments':room_comments}


    return render(request, 'base/activity.html', context)

def profilePage(request, pk):
    user = User.objects.get(id=pk)
    profile = userProfile.objects.get(user=user)
    comments = Comment.objects.filter(user=user)
    topics = Topic.objects.annotate(num_rooms=Count('room')).order_by('-num_rooms')[:5]

    bio = profile.biography
    min_length = 200

    if (len(bio)) < min_length:
        bio += " &nbsp " * (min_length - len(bio))

    user_profile = None
    if request.user.is_authenticated:
        user_profile = userProfile.objects.get(user=request.user)

    context = {'user':user, 'profile':profile, 'comments':comments, 'topics':topics, 'padded_bio':bio, 'user_profile':user_profile}

    return render(request, 'base/profile.html', context)