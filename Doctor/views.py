
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from myapp.models import Appointments, User
from myapp.views import appointment
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange

from django.db.models import Q

# Create your views here.
def dlogin(request):
    
    if request.method=="POST":
        try:
            doctor=Doctors.objects.get(doctoremail=request.POST['doctoremail'])
            
            if request.POST['doctoremail']==doctor.doctoremail:
                if request.POST['password']==doctor.password:
                    request.session['doctoremail'] = request.POST['doctoremail']
                    return render(request,'ddash.html',{'msg':'login successfully','doctor':doctor})
                return render(request,'dlogin.html',{'msg':'invalid password','doctor':doctor})                        
        except:
            return render(request,'dlogin.html',{'msg':'email not registered',})
    return render(request,'dlogin.html')

def dlogout(request):
    try:
        del request.session['doctoremail']
        return render(request,'dlogin.html')
    except:    
        return render(request,'dlogin.html')

def ddash(request):
    doctor=Doctors.objects.get(doctoremail=request.session['doctoremail'])
    return render(request,'ddash.html',{'doctor':doctor})


def dforgot(request):
    
    if request.method=='POST':

        try:

            doctor=Doctors.objects.get(doctoremail=request.POST['doctoremail'])
            if request.POST['doctoremail']==doctor.doctoremail:
                fpass=doctor.password
                subject='your password for login'
                message=f'Welcome to Life Care your password for login is: {fpass}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['doctoremail'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'dforgot.html',{'msg':'password sent successfully'})        
        except:
            return render(request,'dforgot.html',{'msg':'invalid email'})
    return render(request,'dforgot.html')   


def dchangepass(request):
    doc=Doctors.objects.get(doctoremail=request.session['doctoremail'])
    if request.method == 'POST':
        if request.POST['opassword'] == doc.password:
            if request.POST['npassword'] == request.POST['rpassword']:
                doc.password=request.POST['npassword']
                doc.save()
                return render(request,'dchangepass.html',{'msg':'password changed successfully','doc':doc})
            return render(request,'dchangepass.html',{'msg':'new passwords are not same','doc':doc})    
        return render(request,'dchangepass.html',{'msg':'old password is incorrect','doc':doc})
    return render(request,'dchangepass.html',{'doc':doc})

def dedit(request):
    doctor=Doctors.objects.get(doctoremail=request.session['doctoremail'])
    if request.method == 'POST':
        doctor.doctorname=request.POST['doctorname']
        doctor.doctoremail=request.POST['doctoremail']
        doctor.specialization=request.POST['specialization']
        doctor.phone=request.POST['phone']
        

        if 'pic' in request.FILES:
            doc_pic = request.FILES['doc_pic']
        doctor.save()
        return render(request,'dedit.html',{'msg':'profile updated successfully','doctor':doctor})
    return render(request,'dedit.html',{'doctor':doctor})

def viewappointment(request):
    doctor=Doctors.objects.get(doctoremail=request.session['doctoremail'])
    appointments=Appointments.objects.filter(Q(doctor=doctor) & Q(Q(pay_method = 'online') & Q(verify = True) | Q(pay_method='offline')))
    print(appointments)
    return render(request,'viewappointment.html',{'appointments':appointments,'doctor':doctor})




def search(request):
    uid=User.objects.all()
    doctor=Doctors.objects.get(doctoremail=request.session['doctoremail'])
    appointments=Appointments.objects.filter(patient__fname__contains=request.GET['search'],doctor=doctor)
    print(appointments)
    return render(request,'viewappointment.html',{'appointments':appointments,'doctor':doctor})

