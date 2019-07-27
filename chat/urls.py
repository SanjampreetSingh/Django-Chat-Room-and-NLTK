from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_room, name='new_room'),
    path('nltk/', views.nltk),
    re_path(r'^(?P<room_name>[\w-]{,50})/$', views.room, name='room'),
]
