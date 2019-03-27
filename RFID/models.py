from django.db import models
import datetime

class User(models.Model):
    user_id = models.CharField(max_length=32, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=70)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.first_name

class Object(models.Model):
    AVAILABLE = 'Y'
    UNAVAILABLE = 'N'
    TURING = 'T'
    HOPPER = 'H'

    AVAILABILITY_CHOICES = (
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavilable'),
    )

    LOCATION_CHOICES = (
        (TURING, 'Turing'),
        (HOPPER, 'Hopper'),
    )

    object_id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=60)
    availability = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES, default=AVAILABLE)
    max_time = models.IntegerField()
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES, default=HOPPER)

    def __str__(self):
        return self.name



class Records(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    object_id = models.ForeignKey(Object, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=1)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('user_id', 'object_id', 'date'),)
