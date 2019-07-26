from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_room, name='new_room'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
