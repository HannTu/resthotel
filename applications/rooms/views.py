from rest_framework.viewsets import ModelViewSet

from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
