from django.db import models
from room.models import Room
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Links to room
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to sender
    content = models.TextField()  # Message text
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto-set send time

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'  # String representation