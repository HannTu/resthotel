from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

from applications.guests.models import Guest
from applications.rooms.models import Room


def correct_date_validator(start, end):
    if start > end:
        raise ValidationError('End date must be later than start date')

def proper_number_of_guests_validator(room):
    if room.no_of_free_beds < 1:
        raise ValidationError('Not enough place in the room')


class ReservationManager(models.manager.Manager):
    def create(self, *args, **kwargs):
        instance = self.model(**kwargs)
        instance.save()
        return instance


class Reservation(models.Model):
    guest = models.ForeignKey(Guest)
    room = models.ForeignKey(Room)
    start_date = models.DateField()
    end_date = models.DateField()

    objects = ReservationManager()

    def save(self, *args, **kwargs):
        correct_date_validator(self.start_date, self.end_date)
        proper_number_of_guests_validator(self.room)
        return super(Reservation, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Reservation: {}, {}'.format(self.guest.name, self.room.number)

