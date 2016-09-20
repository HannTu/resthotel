from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.manager import Manager


def pesel_length_validator(value):
    if len(str(value)) != 11:
        raise ValidationError('Invalid PESEl number length')


class GuestManager(Manager):
    def create(self, *args, **kwargs):
        instance = self.model(**kwargs)
        instance.save()
        return instance


class Guest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    pesel = models.IntegerField(unique=True, validators=[pesel_length_validator])
    email = models.EmailField()
    address = models.TextField()

    objects = GuestManager()

    def save(self, *args, **kwargs):
        pesel_length_validator(self.pesel)
        return super(Guest, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Guest: {}'.format(self.name)

