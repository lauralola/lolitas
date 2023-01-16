from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Available'), (1, 'Booked'))

TABLE_CHOICES =(
    ('Table one- 2 people', 'Table one- 2 people'),
)

TIME_CHOICES = (
    ('6PM', '6PM'),
    ('9PM', '9PM'),
)
class Customer(models.Model):
    email = models.EmailField()

class Table(models.Model):
    seats = models.IntegerField()
    min_people = models.IntegerField()
    max_people = models.IntegerField()

class Reservation(models.Model):
    table = models.ForeignKey('Table', on_delete=models.CASCADE)
    party = models.ForeignKey('Customer', on_delete=models.CASCADE)
    spot = models.DateField()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)
    table = models.IntegerField(choices= TABLE_CHOICES, default="Table One- 2 people")
    status = models.IntegerField(choices=STATUS, default=0)
    day= models.DateField(default=datetime.now)
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f'{self.user.username} | day: {self.day} | time: {self.time}'

# Create your models here.
