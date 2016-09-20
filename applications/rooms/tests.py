from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Room


class RoomModelTestcase(TestCase):
    def setUp(self):
        self.generic_room_data = {
                'number': 1,
                'no_of_beds': 2,
                'bathroom_inside': True,
                'standard': 'A'
                }

    def test_negative_room_number(self):
        with self.assertRaises(ValidationError):
            data = dict(self.generic_room_data)
            data['number'] = -1
            Room.objects.create(**data)

    def test_correct_room_number(self):
        Room.objects.create(**self.generic_room_data)

    def test_too_high_room_number(self):
        data =  dict(self.generic_room_data)
        data['number'] = 60
        # TODO: fix error
        with self.assertRaises(ValidationError):
            Room.objects.create(**data)

    def test_not_unique_room_number(self):
        Room.objects.create(**self.generic_room_data)
        data = dict(self.generic_room_data)
        data['number'] = 2
        Room.objects.create(**data)

        with self.assertRaises(IntegrityError):
            Room.objects.create(**self.generic_room_data)

    def test_too_many_beds(self):
        data = dict(self.generic_room_data)
        data['no_of_beds'] = 8
        with self.assertRaises(ValidationError):
            Room.objects.create(**data)

    def test_too_few_beds(self):
        data = dict(self.generic_room_data)
        data['no_of_beds'] = -1
        with self.assertRaises(ValidationError):
            Room.objects.create(**data)

    def test_invalid_room_standard(self):
        data = dict(self.generic_room_data)
        data['standard'] = 'D'
        with self.assertRaises(ValidationError):
            Room.objects.create(**data)

        data['standard'] = ''
        #TODO: fix error
        with self.assertRaises(ValidationError):
            Room.objects.create(**data)


class RoomViewsetsTestcase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.generic_room_data = {
                'number': 1,
                'no_of_beds': 2,
                'bathroom_inside': True,
                'standard': 'A'
                }

    def test_adding_rooms(self):
        self.assertEqual(Room.objects.count(), 0)
        self.client.post('/room/', self.generic_room_data, format='json')
        self.assertEqual(Room.objects.count(), 1)

    def test_modifying_rooms(self):
        room = Room.objects.create(**self.generic_room_data)
        new_data = dict(self.generic_room_data)
        new_data['no_of_beds'] += 1
        self.client.put('/room/{}/'.format(room.id), new_data, format='json')
        self.assertEqual(Room.objects.get(id=room.id).no_of_beds, 3)

    def test_listing_all_rooms(self):
        for i in range(3):
            data = dict(self.generic_room_data)
            data['number'] += i
            Room.objects.create(**data)
        resp = self.client.get('/room/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

    def test_deleting_room(self):
        room = Room.objects.create(**self.generic_room_data)
        self.client.delete('/room/{}/'.format(room.id))
        self.assertEqual(Room.objects.count(), 0)

