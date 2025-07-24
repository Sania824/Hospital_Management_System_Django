from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=CASCADE)
    patient = models.ForeignKey(Patient, on_delete=CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.doctor.name + "--" + self.patient.name