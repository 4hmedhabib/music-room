from django.urls import path
from . import views

urlpatterns = [
    path("rooms/", views.RoomView.as_view()),
    path("create-room/", views.CreateRoomView.as_view(), name="create-room"),
    path("get-room/", views.GetRoom.as_view(), name="get-room"),
]
