from django.shortcuts import render
from rest_framework import generics

from .serializers import RoomSerializer
from .models import Room

# Create your views here.
# our end point for the music room app
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer