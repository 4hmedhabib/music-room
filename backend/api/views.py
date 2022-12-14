from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CreateRoomSerializer, RoomSerializer
from .models import Room


# Create your views here.
# our end point for the music room app
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = ["code", "host"]

    def get(self, request):
        code = request.GET.get(self.lookup_url_kwarg[0])
        host = request.GET.get(self.lookup_url_kwarg[1])


        if code != None:
            room = Room.objects.filter(code=code)
            if room.count() > 0:
                data = RoomSerializer(room[0]).data
                data["is_host"] = host == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Room Not Found": "Something went wrong!"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Something went wrong!.'}, status=status.HTTP_400_BAD_REQUEST)

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        print("REQUEST")
        print("==========================")

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key

            queryset = Room.objects.filter(host=host)

            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
