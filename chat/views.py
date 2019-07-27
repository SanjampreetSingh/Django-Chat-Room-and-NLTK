from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.db import transaction

from haikunator import Haikunator
import json
import random
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag


from .models import Room, Message


def index(request):
    return render(request, 'chat/index.html', {})


def new_room(request):
    new_room = None
    while not new_room:
        with transaction.atomic():
            name = Haikunator.haikunate()
            if Room.objects.filter(name=name).exists():
                continue
            new_room = Room.objects.create(name=name)
    return redirect(room, room_name=name)


def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    messages = reversed(Message.objects.filter(room=room).order_by('timestamp')[:50])
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages,
    })


def nltk(request):
    message = str(request.POST.get('message'))
    tokenize = word_tokenize(message)
    pos = pos_tag(tokenize)
    data = {
        'data': pos
    }
    return JsonResponse(data, status=201)
