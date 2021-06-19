"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from egzamin_probny.views import Start, Lecture
from reservation_system.views import AddRoom, AllRooms, EditRoom, DelRoom, BookRoom, RoomDtl, Main, Search, AddRoom2, \
    AllRooms2, DelRoom2, EditRoom2, BookRoom2, RoomDtl2, Search2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/add/', AddRoom.as_view()),
    path('room/add2/', AddRoom2.as_view(), name="add-room"),

    path('room/modify/<int:id>', EditRoom.as_view()),
    path('room/modify2/<int:id>/', EditRoom2.as_view(), name="edit-room"),

    path('room/delete/<int:id>', DelRoom.as_view()),
    path('room/delete2/<int:id>/', DelRoom2.as_view(), name="delete-room"),

    path('room/reserve/<int:id>', BookRoom.as_view()),
    path('room/reserve2/<int:id>/', BookRoom2.as_view(), name="reserver-room"),

    path('room/<int:id>', RoomDtl.as_view()),
    path('room2/<int:id>/', RoomDtl2.as_view(), name="room"),

    path('rooms/', AllRooms.as_view()),
    path('rooms2/', AllRooms2.as_view(), name="room-list"),

    path('', Main.as_view()),

    path('search/', Search.as_view()),
    path('search2/', Search2.as_view(), name="room-search"),

    path('start/', Start.as_view()),
    path('lecture/<int:id>', Lecture.as_view())
]
