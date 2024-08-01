from django.db import models
from datetime import datetime


def calculate_expiry():
    return datetime.now() + timedelta(minutes=30)


class Reservation(models.Model):

    client = models.ForeignKey('reservation.Client', on_delete=models.CASCADE)
    provider = models.ForeignKey('reservation.Provider', on_delete=models.CASCADE)
    appointment = models.ForeignKey('reservation.Appointment', on_delete=models.CASCADE)

    expiry = models.DateTimeField(default=calculate_expiry)
    confirmed = models.BooleanField(default=False)
