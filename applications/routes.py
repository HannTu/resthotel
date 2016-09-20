from rest_framework import routers

from guests import views as gviews
from reservations import views as res_views
from rooms import views as room_views


router = routers.SimpleRouter()
router.register(r'guest', gviews.GuestViewSet)
router.register(r'reservation', res_views.ReservationViewSet)
router.register(r'room', room_views.RoomViewSet)

