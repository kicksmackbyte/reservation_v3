from django.db import models
from .reservation import Reservation
from django.utils import timezone

import datetime

ADVANCED_NOTICE = {'days': 1}

class AvailableAppointmentManager(models.Manager):

    def get_queryset(self):

        reservations = Reservation.confirmed_objects.all() | Reservation.active_objects.all()
        appointment_ids = [r.appointment_id for r in reservations]

        advanced_notice = timezone.now() + datetime.timedelta(**ADVANCED_NOTICE)

        return super().get_queryset().exclude(id__in=appointment_ids).exclude(time_slot__lt=advanced_notice)


class ConfirmedAppointmentManager(models.Manager):

    def get_queryset(self):

        confirmed_appointment_ids = Reservation.confirmed_objects.all()

        return super().get_queryset().filter(id__in=confirmed_appointment_ids)


class Appointment(models.Model):

    time_slot = models.DateTimeField()
    provider = models.ForeignKey('reservation.Provider', on_delete=models.CASCADE)

    objects = models.Manager()
    available_objects = AvailableAppointmentManager()
    confirmed_objects = ConfirmedAppointmentManager()
