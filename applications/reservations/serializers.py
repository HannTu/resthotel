from rest_framework import serializers

from .models import Reservation
from applications.guests.serializers import GuestSerializer
from applications.rooms.serializers import RoomSerializer


class ReservationSerializer(serializers.ModelSerializer):
    # guest = GuestSerializer()

    class Meta:
        model = Reservation

