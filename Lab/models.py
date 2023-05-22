from tkinter import CASCADE
from django.db import models
from django.forms import FileField

from myapp.models import User
# Create your models here.

class Assistants(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    lab_pic=models.FileField(upload_to='profile',default='lab.png')



    def __str__(self):
        return self.email



class Test(models.Model):
    test_name=models.CharField(max_length=50)
    amount=models.IntegerField(default=0)

    def __str__(self):
        return self.test_name

class Lappointment(models.Model):
    date=models.DateField()
    time=models.CharField(max_length=25)
    pay_id=models.CharField(max_length=20)
    verify=models.BooleanField(default=False)
    lab=models.ForeignKey(Assistants,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.IntegerField(default=0)
    patient=models.ForeignKey(User,on_delete=models.CASCADE)
    test=models.ForeignKey(Test,on_delete=models.CASCADE)
    pay_at=models.DateTimeField(auto_now_add=True)
    pay_method=models.CharField(max_length=30,null=True,blank=True)
    test_result=models.FileField(upload_to='reports',null=True,blank=True)



    def __str__(self):
        return self.patient.email


    

