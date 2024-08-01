from django.db import models


class Appointment(models.Model):

    time_slot = models.DateTimeField()
