from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Guest


class GuestModelTestcase(TestCase):
    def test_unique_pesel(self):
        Guest.objects.create(
                name='TestGuest1',
                first_name='Test1',
                last_name='Guest1',
                email='Guest1@Test.py',
                address='Test Place 123',
                pesel=12345678901)

        Guest.objects.create(
                name='TestGuest3',
                first_name='Test3',
                last_name='Guest3',
                email='Guest3@Test.py',
                address='Test Place 123',
                pesel=12345678902)

        with self.assertRaises(IntegrityError):
            Guest.objects.create(
                    name='TestGuest2',
                    first_name='Test2',
                    last_name='Guest2',
                    email='Guest2@Test.py',
                    address='Test Place 123',
                    pesel=12345678901)

    def test_unique_username(self):
        Guest.objects.create(
                name='TestGuest',
                first_name='Test',
                last_name='Guest',
                email='Guest@Test.py',
                address='Test Place 123',
                pesel=12345678901)

        Guest.objects.create(
                name='TestGuest3',
                first_name='Test3',
                last_name='Guest3',
                email='Guest3@Test.py',
                address='Test Place 123',
                pesel=12345678903)

        with self.assertRaises(IntegrityError):
            Guest.objects.create(
                    name='TestGuest',
                    first_name='Test',
                    last_name='Guest',
                    email='Guest@Test.py',
                    address='Test Place 123',
                    pesel=12345678902)

    def test_invalid_pesel_length(self):
        with self.assertRaises(ValidationError):
            Guest.objects.create(
                    name='TestGuest1',
                    first_name='Test1',
                    last_name='Guest1',
                    email='Guest1@Test.py',
                    address='Test Place 123',
                    pesel=1234567890)

            Guest.objects.create(
                    name='TestGuest2',
                    first_name='Test2',
                    last_name='Guest2',
                    email='Guest2@Test.py',
                    address='Test Place 123',
                    pesel=123456789012)


class GuestViewsetsTestcase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.generic_guest_data = {
                'name': 'TestGuest',
                'first_name': 'Test',
                'last_name': 'Guest',
                'email': 'guest@test.py',
                'pesel': 12345678901,
                'address': 'Test Place 123'
                }

    def test_adding_users(self):
        self.assertEqual(Guest.objects.count(), 0)
        self.client.post('/guest/', self.generic_guest_data, format='json')
        self.assertEqual(Guest.objects.count(), 1)

    def test_modifying_guest(self):
        guest = Guest.objects.create(**self.generic_guest_data)
        new_data = dict(self.generic_guest_data)
        new_data['name'] = 'NewName'
        self.client.put('/guest/{}/'.format(guest.id), new_data, format='json')
        self.assertEqual(Guest.objects.get(id=guest.id).name, 'NewName')

    def test_listing_all_guests(self):
        for i in range(3):
            data = dict(self.generic_guest_data)
            data['name'] = data['name'] + str(i)
            data['pesel'] += i
            Guest.objects.create(**data)
        resp = self.client.get('/guest/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

    def test_deleting_guest(self):
        guest = Guest.objects.create(**self.generic_guest_data)
        self.client.delete('/guest/{}/'.format(guest.id))
        self.assertEqual(Guest.objects.count(), 0)

