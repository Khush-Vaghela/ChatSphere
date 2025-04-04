from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room.models import Room
from chat.models import Message

# Create your views here.

@login_required
def create_room(request):
    
    if request.method == "POST":
        room_name = request.POST['room_name']
        room_code = Room.generate_unique_code()

        room = Room.objects.create(
                    creator = request.user,
                    code = room_code,
                    name = room_name
                )
        
        room.members.add(request.user)
        room.save()
        messages = room.message_set.all().order_by('timestamp')

        return render(request, "room.html", {
            'room_name' : room.name, 
            'creator' : room.creator, 
            'room_code' : room.code, 
            'created_at' : room.created_at, 
            'user' : request.user,
            'users' : room.members.all(),
            'messages' : messages
        })
    
    return render(request, "create_room.html")

@login_required
def join_room(request):

    if request.method == "POST":
        room_code = request.POST.get('room_code')

        # Get the room or None if it doesn't exist
        room = Room.objects.filter(code=room_code).first()

        if room is not None and request.user.rooms.filter(code=room_code).exists():

            messages = room.message_set.all().order_by('timestamp')
            return render(request, "room.html", {
                'room_name' : room.name, 
                'creator' : room.creator, 
                'room_code' : room.code, 
                'created_at' : room.created_at, 
                'user' : request.user,
                'users' : room.members.all(),
                'messages' : messages
            })
        
        if room is not None:

            room.members.add(request.user)  # Add user to members list
            messages = room.message_set.all().order_by('timestamp')

            return render(request, "room.html", {
                'room_name' : room.name, 
                'creator' : room.creator, 
                'room_code' : room.code, 
                'created_at' : room.created_at, 
                'user' : request.user,
                'users' : room.members.all(),
                'messages' : messages
            })
        
        else:
            messages.error(request, "Room does not exist.")  # Use Django messages
            return redirect("join_room")  # Redirect instead of manual JavaScript

    return render(request, "join_room.html")

@login_required
def enter_room(request, room_code):

    print(room_code)
    room = Room.objects.filter(code=room_code).first()
    messages = room.message_set.all().order_by('timestamp')

    return render(request, "room.html", {
        'room_name' : room.name, 
        'creator' : room.creator, 
        'room_code' : room.code, 
        'created_at' : room.created_at, 
        'user' : request.user,
        'users' : room.members.all(),
        'messages' : messages
    })

@login_required
def delete_room(request, room_code):

    room = Room.objects.filter(code = room_code).first()
    room.delete()

    return redirect("/")

@login_required
def exit_room(request, room_code):
    room = get_object_or_404(Room, code=room_code)

    if request.user in room.members.all():

        request.user.rooms.remove(room)
        room.members.remove(request.user)
        
    return redirect('/')
