from django.db import models


class Provider(models.Model):

    first_name = models.CharField(max_length=100)
