from django.db import models

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
