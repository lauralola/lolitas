from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

TABLE_CHOICES =(
    ('Table one- 2 people', 'Table one- 2 people'),
)

TIME_CHOICES = (
    ('6PM', '6PM'),
    ('9PM', '9PM'),
)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)
    table = models.CharField(max_length=50, choices= TABLE_CHOICES, default="Table One- 2 people")
    day= models.DateField(default=datetime.now)
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f'{self.user.username} | day: {self.day} | time: {self.time}'

# Create your models here.
