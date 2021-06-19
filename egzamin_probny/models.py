from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=64, unique=True)
    year_at_univeristy = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

class Lecture(models.Model):
    name = models.CharField(max_length=64, unique=True)
    lecturer = models.CharField(max_length=64)
    students = models.ManyToManyField(Student)
