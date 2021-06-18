from django.db import models

# Create your models here.


class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)

class Booking(models.Model):
    date = models.DateField()
    room = models.ForeignKey('Rooms', models.CASCADE)
    comment = models.TextField()

    class Meta:
        unique_together = ('date', 'room_id')
