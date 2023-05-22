from django.shortcuts import render,redirect

from myapp.views import lappointment
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange

from django.db.models import Q
# Create your views here.


def llogin(request):
    try:
        lab = Assistants.objects.get(email=request.session['email'])
        return render(request,'ldash.html',{'lab':lab})
    except:
        if request.method == 'POST':
            try:
                lab = Assistants.objects.get(email=request.POST['email'])
                if request.POST['password'] == lab.password:
                    request.session['email'] = request.POST['email']
                    return render(request,'ldash.html',{'lab':lab})
                return render(request,'llogin.html',{'msg':'Inncorrect password','lab':lab})
            except:
                msg = 'Email is not register'
                return render(request,'llogin.html',{'msg':msg,'lab':lab})
        return render(request,'llogin.html')



def llogout(request):
    try:
        del request.session['email']
        return render(request,'llogin.html') 
    except:
        return render(request,'llogin.html') 
    
def ledit(request):
    lab = Assistants.objects.get(email=request.session['email'])
    if request.method == 'POST':
        lab.name = request.POST['name']
        lab.email = request.POST['email']
        lab.phone = request.POST['phone']
        
        if 'pic' in request.FILES:
            lab.pic = request.FILES['lab_pic']
        lab.save()
        return render(request,'ledit.html',{'lab':lab,'msg':'Profile has been updated'})
    return render(request,'ledit.html',{'lab':lab})


def ldash(request):
    
    return render(request,'ldash.html')
def lchangepass(request):
    lab=Assistants.objects.get(email=request.session['email'])
    if request.method=='POST':
        if request.POST['opassword'] == lab.password:
            if request.POST['npassword'] == request.POST['rpassword']:
                lab.password= request.POST['npassword']
                return render(request,'lchangepass.html',{'msg':'password changed successfully','lab':lab})
            return render(request,'lchangepass.html',{'msg':'new passwords are not same','lab':lab})
        return render(request,'lchangepass.html',{'msg':'old password is incorrect','lab':lab})

    return render(request,'lchangepass.html',{'lab':lab})

def lforgot(request):
    
    if request.method=='POST':

        try:

            lab=Assistants.objects.get(email=request.POST['email'])
            if request.POST['email']==lab.email:
                fpass=lab.password
                subject='your password for login'
                message=f'Welcome to Life Care your password for login is: {fpass}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'lforgot.html',{'msg':'password sent successfully'})        
        except:
            return render(request,'lforgot.html',{'msg':'invalid email'})
    return render(request,'lforgot.html')   


def lviewappointment(request):
    lab=Assistants.objects.get(email=request.session['email'])
    lappointments=Lappointment.objects.filter(Q(verify=True) | Q(pay_method='offline'))
    print(lappointments)
    return render(request,'lviewappointment.html',{'lappointments':lappointments,'lab':lab})

def viewbtn(request,pk):
    lab=Assistants.objects.get(email=request.session['email'])
    lappointments=Lappointment.objects.get(id=pk)
    
    print(lappointments)
    return render(request,'viewbtn.html',{'lappointments':lappointments,'lab':lab})
    
def rep_up(request,pk):
    app = Lappointment.objects.get(id=pk)
    lab=Assistants.objects.get(email=request.session['email'])
    app.lab = lab
    app.test_result = request.FILES['report']
    app.save()    
    return render(request,'viewbtn.html',{'lappointments':app,'lab':lab })

