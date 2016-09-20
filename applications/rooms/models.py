from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.manager import Manager


def no_of_beds_validator(value):
    if value not in range(1, 5):
        raise ValidationError('{} not in range: 1-4'.format(value))


def room_number_validator(value):
    if value not in range(1, 51):
        raise ValidationError('{} not in range: 1-50'.format(value))

def room_standard_validator(value):
    if value not in ['A', 'B', 'C']:
        raise ValidationError('Incorrect room standard')


ROOM_STANDARDS = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C')
]


class RoomManager(Manager):
    def create(self, *args, **kwargs):
        instance = self.model(**kwargs)
        instance.save()
        return instance


class Room(models.Model):
    number = models.IntegerField(unique=True, validators=[room_number_validator])
    no_of_beds = models.IntegerField(validators=[no_of_beds_validator])
    bathroom_inside = models.BooleanField()
    standard = models.CharField(
            choices=ROOM_STANDARDS, max_length=1, blank=False,
            validators=[room_standard_validator])

    objects = RoomManager()

    def save(self, *args, **kwargs):
        room_number_validator(self.number)
        no_of_beds_validator(self.no_of_beds)
        room_standard_validator(self.standard)
        return super(Room, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Room: {}'.format(self.number)

    @property
    def no_of_free_beds(self):
        return self.no_of_beds - self.reservation_set.count()

