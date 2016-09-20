from rest_framework.viewsets import ModelViewSet

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

