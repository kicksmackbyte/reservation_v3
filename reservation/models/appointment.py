from django.db import models
from .reservation import Reservation


class AvailableAppointmentManager(models.Manager):

    def get_queryset(self):

        reservations = Reservation.confirmed_objects.all() | Reservation.reserved_objects.all()
        appointment_ids = [r.appointment_id for r in reservations]

        return super().get_queryset().exclude(id__in=appointment_ids)


class ConfirmedAppointmentManager(models.Manager):

    def get_queryset(self):

        confirmed_appointment_ids = Reservation.confirmed_objects.all()

        return super().get_queryset().filter(id__in=confirmed_appointment_ids)


class Appointment(models.Model):

    time_slot = models.DateTimeField()
    provider = models.ForeignKey('reservation.Provider', on_delete=models.CASCADE)

    available_objects = AvailableAppointmentManager()
    confirmed_objects = ConfirmedAppointmentManager()
