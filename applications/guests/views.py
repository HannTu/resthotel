from rest_framework.viewsets import ModelViewSet

from .models import Guest
from .serializers import GuestSerializer


class GuestViewSet(ModelViewSet):
    serializer_class = GuestSerializer
    queryset = Guest.objects.all()
