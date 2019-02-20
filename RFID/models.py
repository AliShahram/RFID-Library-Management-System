from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name

class User(models.Model):
    user_id = models.CharField(max_length=32, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=70)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.first_name
