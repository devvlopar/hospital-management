
from django.db import models
# Create your models here.

class Doctors(models.Model):
    doctorname = models.CharField(max_length=50)
    doctoremail=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    phone=models.CharField(max_length=13)
    specialization=models.CharField(max_length=30)
    doc_pic=models.FileField(upload_to='profile',default='doc.png')
    fees=models.IntegerField()

    def __str__(self):
        return self.doctorname

    
