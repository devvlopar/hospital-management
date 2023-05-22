from django.db import models
from Doctor.models import Doctors









# Create your models here.
class User(models.Model):
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    address=models.TextField()
    age=models.CharField(max_length=10)
    gender=models.CharField(max_length=10)
    pic=models.FileField(upload_to='profile',default='avatar.png')

    def __str__(self):
        return self.email


class Appointments(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctors,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.CharField(max_length=25)
    pay_method=models.CharField(max_length=30)
    pay_id=models.CharField(max_length=50)
    amount=models.IntegerField(default=0)
    verify=models.BooleanField(default=False)
    pay_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.patient.email

class Contact(models.Model):
    name=models.CharField(max_length=35)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=14)
    subject=models.CharField(max_length=50)
    message=models.TextField()