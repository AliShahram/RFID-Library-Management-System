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
    CHECK_OUT = '1'
    CHECK_IN = '0'

    TYPE_CHOICES = (
        (CHECK_OUT, 'Check out'),
        (CHECK_IN, 'Check in'),
    )


    ACTIVE = True
    COMPLETED = False

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed')
    )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=CHECK_OUT)
    status = models.BooleanField(choices=STATUS_CHOICES, default=CHECK_OUT)

    class Meta:
        unique_together = (('user_id', 'object_id', 'date'),)

    def __str__(self):
        return "%s, %s" %(self.user_id, self.object_id)
