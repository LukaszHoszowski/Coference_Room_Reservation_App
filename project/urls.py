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

from reservation_system.views import AddRoom, AllRooms, EditRoom, DelRoom, BookRoom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/add/', AddRoom.as_view()),
    path('room/modify/<int:id>', EditRoom.as_view()),
    path('room/delete/<int:id>', DelRoom.as_view()),
    path('room/reserve/<int:id>', BookRoom.as_view()),
    path('rooms/', AllRooms.as_view()),
]
