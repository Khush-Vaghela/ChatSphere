import secrets
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_rooms")  # Creator of the room
    members = models.ManyToManyField(User, related_name="rooms")  # Users who have joined
    code = models.CharField(max_length=6, unique=True, blank=True)  # Unique room code
    name = models.CharField(max_length=100)  # Optional: Name of the room
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        while True:
            code = secrets.token_urlsafe(4)[:6]
            if not Room.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f"Room {self.code} by {self.creator.username} ({self.members.count()} members)"
