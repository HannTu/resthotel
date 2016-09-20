from datetime import timedelta, datetime

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from rest_framework.test import APIClient, APITestCase

from .models import Reservation
from applications.rooms.models import Room
from applications.guests.models import Guest


class ReservationModelTestCase(TestCase):
    def setUp(self):
        self.default_guest_data = {
                'name': 'DefaultUser',
                'first_name': 'Default',
                'last_name': 'User',
                'email': 'user@default.py',
                'pesel': 12345678901,
                'address': 'Test Street 0'
                }
        self.default_room_data = {
                'number': 1,
                'no_of_beds': 2,
                'bathroom_inside': True,
                'standard': 'A'
                }
        self.default_guest = Guest.objects.create(**self.default_guest_data)
        self.default_room = Room.objects.create(**self.default_room_data)

        self.default_reservation_data = {
                'guest': self.default_guest,
                'room': self.default_room,
                'start_date': datetime.today(),
                'end_date': datetime.today() + timedelta(days=3)
                }
        self.default_reservation = Reservation.objects.create(
                **self.default_reservation_data)

    def test_too_many_guests_for_room(self):
        guest_data = dict(self.default_guest_data)
        guest_data['name'] += '2'
        guest_data['pesel'] += 1
        guest1 = Guest.objects.create(**guest_data)

        guest_data['name'] += '3'
        guest_data['pesel'] += 1
        guest2 = Guest.objects.create(**guest_data)

        Reservation.objects.create(
                guest=guest1,
                room=self.default_room,
                start_date=datetime.today(),
                end_date=datetime.today() + timedelta(days=3))

        with self.assertRaises(ValidationError):
            Reservation.objects.create(
                    guest=guest2,
                    room=self.default_room,
                    start_date=datetime.today(),
                    end_date=datetime.today() + timedelta(days=3))

    def test_start_date_greater_than_end(self):
        new_data = dict(self.default_reservation_data)
        new_data['start_date'], new_data['end_date'] = new_data['end_date'], new_data['start_date']
        with self.assertRaises(ValidationError):
            Reservation.objects.create(**new_data)


class ReservationViewsetsTestcase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.default_guest_data = {
                'name': 'DefaultUser',
                'first_name': 'Default',
                'last_name': 'User',
                'email': 'user@default.py',
                'pesel': 12345678901,
                'address': 'Test Street 0'
                }
        self.default_room_data = {
                'number': 1,
                'no_of_beds': 2,
                'bathroom_inside': True,
                'standard': 'A'
                }
        self.default_guest = Guest.objects.create(**self.default_guest_data)
        self.default_room = Room.objects.create(**self.default_room_data)

        self.default_reservation_data = {
                'guest': self.default_guest,
                'room': self.default_room,
                'guest_id': self.default_guest.id,
                'room_id': self.default_room.id,
                'start_date': datetime.today().strftime('%Y-%m-%d'),
                'end_date': (datetime.today() + timedelta(days=3)).strftime('%Y-%m-%d')
                }

    def test_adding_reservations(self):
        self.assertEqual(Reservation.objects.count(), 0)
        data = dict(self.default_reservation_data)
        data['guest'] = data['guest'].id
        data['room'] = data['room'].id
        rrr = self.client.post('/reservation/', data, format='json')
        self.assertEqual(Reservation.objects.count(), 1)

    def test_modifying_reservations(self):
        reservation = Reservation.objects.create(**self.default_reservation_data)
        new_data = dict(self.default_reservation_data)
        new_data['end_date'] = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        new_data['guest'] = new_data['guest_id']
        new_data['room'] = new_data['room_id']
        rrr= self.client.put('/reservation/{}/'.format(reservation.id), new_data, format='json')
        self.assertEqual(Reservation.objects.get(
            id=reservation.id).end_date.strftime('%Y-%m-%d'),
            new_data['end_date'])

    def test_listing_all_reservations(self):
        for i in range(2):
            data = dict(self.default_reservation_data)
            data['end_date'] = (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d')
            Reservation.objects.create(**data)
        resp = self.client.get('/reservation/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)

    def test_deleting_reservations(self):
        reservation = Reservation.objects.create(**self.default_reservation_data)
        self.client.delete('/reservation/{}/'.format(reservation.id))
        self.assertEqual(Reservation.objects.count(), 0)

