from django.db import models
from django.utils import timezone

import datetime


def calculate_expiry():
    return timezone.now() + datetime.timedelta(minutes=30)


class ConfirmedAppointmentManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(confirmed=True)


class ReservedAppointmentManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(confirmed=False, expiry__lt=timezone.now())


class Reservation(models.Model):

    client = models.ForeignKey('reservation.Client', on_delete=models.CASCADE)
    appointment = models.ForeignKey('reservation.Appointment', on_delete=models.CASCADE)

    expiry = models.DateTimeField(default=calculate_expiry)
    confirmed = models.BooleanField(default=False)

    objects = models.Manager()
    confirmed_objects = ConfirmedAppointmentManager()
    reserved_objects = ReservedAppointmentManager()
