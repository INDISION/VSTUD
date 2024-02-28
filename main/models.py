from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    TRANSPORTAION_OPTIONS = (
        ('hostel', 'H'),
        ('college_bus', 'D'),
        ('private', 'P')
    )
    GENDER_OPTIONS = (
        ("male", "MALE"),
        ("female", "FEMALE")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    register_no = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_OPTIONS)
    phone_no = models.CharField(max_length=20)
    transportation = models.CharField(max_length=20, choices=TRANSPORTAION_OPTIONS)

    def __str__(self):
        return self.register_no