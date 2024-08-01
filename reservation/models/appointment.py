from django.db import models


class Appointment(models.Model):

    time_slot = models.DateTimeField()
    provider = models.ForeignKey('reservation.Provider', on_delete=models.CASCADE)
