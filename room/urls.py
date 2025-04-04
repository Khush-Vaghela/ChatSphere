from django.urls import path
from . import views

urlpatterns = [

    path('create_room', views.create_room, name = 'create_room'),
    path('join_room', views.join_room, name = 'join_room'),
    path('room/<str:room_code>/', views.enter_room, name = 'enter_room'),
    path('room/<str:room_code>/delete/', views.delete_room, name = 'delete_room'),
    path('room/<str:room_code>/exit/', views.exit_room, name = 'exit_room'),
]