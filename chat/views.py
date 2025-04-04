from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    
    if request.user.is_authenticated:
        rooms = request.user.rooms.all()
        return render(request, 'index.html', {'rooms' : rooms})
    
    return render(request, 'index.html')

