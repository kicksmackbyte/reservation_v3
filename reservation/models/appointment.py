from django.db import models
from .reservation import Reservation
from django.utils import timezone
from django.conf import settings

import datetime

class AvailableAppointmentManager(models.Manager):

    def get_queryset(self):

        reservations = Reservation.confirmed_objects.all() | Reservation.active_objects.all()
        appointment_ids = [r.appointment_id for r in reservations]

        advanced_notice = timezone.now() + datetime.timedelta(**settings.ADVANCED_NOTICE)

        return super().get_queryset().exclude(id__in=appointment_ids).exclude(time_slot__lt=advanced_notice)


class ConfirmedAppointmentManager(models.Manager):

    def get_queryset(self):

        confirmed_reservations = Reservation.confirmed_objects.all()
        confirmed_appointment_ids = [r.appointment_id for r in confirmed_reservations]

        return super().get_queryset().filter(id__in=confirmed_appointment_ids)


class ReservedAppointmentManager(models.Manager):

    def get_queryset(self):

        reservations = Reservation.objects.all()
        reserved_appointment_ids = [r.appointment_id for r in reservations]

        return super().get_queryset().filter(id__in=reserved_appointment_ids)


class Appointment(models.Model):

    time_slot = models.DateTimeField()
    provider = models.ForeignKey('reservation.Provider', on_delete=models.CASCADE)

    objects = models.Manager()
    available_objects = AvailableAppointmentManager()
    confirmed_objects = ConfirmedAppointmentManager()
    reserved_objects = ReservedAppointmentManager()
