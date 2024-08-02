from django.db import models
from django.utils import timezone
from django.conf import settings

import datetime


def calculate_expiry():
    return timezone.now() + datetime.timedelta(**settings.EXPIRATION_OFFSET)


class ActiveReservationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(confirmed=False, expiry__gte=timezone.now())


class ConfirmedReservationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(confirmed=True)


class ExpiredReservationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(confirmed=False, expiry__lt=timezone.now())


class Reservation(models.Model):

    client = models.ForeignKey('reservation.Client', on_delete=models.CASCADE)
    appointment = models.ForeignKey('reservation.Appointment', on_delete=models.CASCADE)

    expiry = models.DateTimeField(default=calculate_expiry)
    confirmed = models.BooleanField(default=False)

    objects = models.Manager()

    active_objects = ActiveReservationManager()
    confirmed_objects = ConfirmedReservationManager()
    expired_objects = ExpiredReservationManager()


    @property
    def expired(self):
        return self.expiry < timezone.now()
