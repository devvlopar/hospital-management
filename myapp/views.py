
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from Lab.models import Assistants, Lappointment, Test
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
from Doctor.models import Doctors

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.db.models import Q

# Create your views here.
def index(request):
    doctor=Doctors.objects.all()
    return render(request,'index.html',{'doctor':doctor})


def np(request):
    if request.method == 'POST':
        return render(request,'reg.html',{'msg':'ONE STEP AWAY TO BOOK APPOINTMENT REGISTER NOW'})
    return render(request,'reg.html')


def register(request):
    if request.method == 'POST':

        try:
            User.objects.get(email=request.POST['email'])
            msg='email already registered'
            return render(request,'reg.html',{'msg':msg})        
        except:
            if request.POST['password']== request.POST['cpassword']:
                global temp
                temp={
                'fname':request.POST['fname'],
                'lname':request.POST['lname'],
                'email':request.POST['email'],
                'password':request.POST['password'],
                'phone':request.POST['phone'],    
                }
                otp = randrange(1111,9999)
                subject = 'welcome to Life Care'
                message = f'your otp for registeration is :  {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp})
            else:
                return render(request,'reg.html',{'msg':'both passwords are not same'}) 
    return render(request,'reg.html')



def otp(request):
    if request.method=='POST':
        if request.POST['otp'] == request.POST['uotp']:
            global temp
            User.objects.create(
            fname=temp['fname'],
            lname=temp['lname'],
            email=temp['email'],
            password=temp['password'],
            phone=temp['phone'],
            )
            return render(request,'reg.html',{'msg':'Account created successfully'})
        return render(request,'otp.html',{'msg':'invalid otp','otp':request.POST['otp']})
    return render(request,'reg.html')




def plogin(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'pdash.html',{'uid':uid})
    except:
        if request.method == 'POST':
            try:
                uid = User.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    return render(request,'pdash.html',{'uid':uid})
                return render(request,'plogin.html',{'msg':'Inncorrect password','uid':uid})
            except:
                msg = 'Email is not register'
                return render(request,'plogin.html',{'msg':msg})
        return render(request,'plogin.html')

def plogout(request):
    try:

        del request.session['email']
        return render(request,'plogin.html') 
    
    except:
        return render(request,'plogin.html') 




def pedit(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.email = request.POST['email']
        uid.phone = request.POST['phone']
        uid.address = request.POST['address']
        uid.age = request.POST['age']
        uid.gender = request.POST['gender']
        
        if 'pic' in request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
        return render(request,'pedit.html',{'uid':uid,'msg':'Profile has been updated'})
    return render(request,'pedit.html',{'uid':uid}) 
     

def pforgot(request):
    
    if request.method=='POST':

        try:

            uid=User.objects.get(email=request.POST['email'])
            if request.POST['email']==uid.email:
                fpass=uid.password
                subject='your password for login'
                message=f'Welcome to Life Care your password for login is: {fpass}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'pforgot.html',{'msg':'password sent successfully'})        
        except:
            return render(request,'pforgot.html',{'msg':'invalid email'})
    return render(request,'pforgot.html')   



def pchangepass(request):
    uid=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        if request.POST['opassword'] == uid.password:
            if request.POST['npassword'] == request.POST['rpassword']:
                uid.password= request.POST['npassword']
                uid.save()
                return render(request,'pchangepass.html',{'msg':'password changed successfully','uid':uid})
            return render(request,'pchangepass.html',{'msg':'new passwords does not match','uid':uid})
        return render(request,'pchangepass.html',{'msg':'old password is incorrect','uid':uid})
    return render(request,'pchangepass.html',{'uid':uid})

def cancer(request):
    return render(request,'cancer.html')
def organ(request):
    return render(request,'organ.html')
def covid(request):
    return render(request,'covid.html')
def generic(request):
    return render(request,'generic.html')
def services(request):
    return render(request,'services.html')
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')


def pdash(request):
    uid=User.objects.get(email=request.session['email'])
    lab = Lappointment.objects.filter(Q(patient=uid) & ~Q(test_result = None))
    return render(request,'pdash.html',{'uid':uid,'lab':lab})

def dashboard(request):
    return render(request,'dashboard.html')

#json javascript jquesry
def getspe(request):
    data = list(Doctors.objects.filter(specialization=request.GET['value']).values())
    return JsonResponse({'data':data})

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
def appointment(request):
    uid=User.objects.get(email=request.session['email']) 
    doctor = Doctors.objects.all()
    if request.method=='POST':
        doctor = Doctors.objects.get(id=request.POST['doctorname'])
        ap = Appointments.objects.create(
            doctor = doctor,
            pay_method = request.POST['pay_method'],
            date = request.POST['date'],
            time = request.POST['time'],
            patient = uid,
            amount = doctor.fees,
            
        )
        if request.POST['pay_method'] == 'offline':
            return render(request,'appointment.html',{'msg':'appointment booked successfully','uid':uid})
        currency = 'INR'
        amount = (doctor.fees)*100  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = f'docpaymenthandler/{ap.id}'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['ap'] = ap
        return render(request,'pay.html', context=context)
    return render(request,'appointment.html',{'uid':uid,'doctor':doctor})




 
# def pay(request):
#     currency = 'INR'
#     amount = 50000  # Rs. 200
 
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
 
#     return render(request,'pay.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def docpaymenthandler(request,pk):
 
    # only accept POST request.
    if request.method == "POST":
        ap = Appointments.objects.get(id=pk)
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            # if result is None:
            amount = (ap.amount)*100  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                ap.pay_id = payment_id
                ap.verify = True
                ap.save()
                # render success page on successful caputre of payment
                
                subject = 'Appointment status'
                message = f'''  Appointment Booked Successfully :  {ap.pay_id}
                amount payed:  {ap.amount}
                payment mode :  {ap.pay_method}
                payment time :  {ap.pay_at}
                '''
               
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.session['email'], ]
                send_mail( subject, message, email_from, recipient_list )               
                return render(request, 'success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'fail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest() 




def lappointment(request):
    uid=User.objects.get(email=request.session['email'])
    test=Test.objects.all() 
    
      
    if request.method == 'POST':
        test = Test.objects.get(id = request.POST['test'])
        lap=Lappointment.objects.create(
            test=test,
            time=request.POST['time'],
            date=request.POST['date'],
            amount=test.amount,
            pay_method=request.POST['pay_method'],
            patient=uid,       

        )
        if request.POST['pay_method'] == 'offline':
            return render(request,'lappointment.html',{'msg':'Appointment booked successfully','lap':lap,'uid':uid})

        currency = 'INR'
        amount = (test.amount)*100  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = f'labpaymenthandler/{lap.id}'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['lap'] = lap
        return render(request,'test_pay.html', context=context)
    
    return render(request,'lappointment.html',{'uid':uid,'test':test})
    


@csrf_exempt
def labpaymenthandler(request,pk):
 
    # only accept POST request.
    if request.method == "POST":
        lap = Lappointment.objects.get(id=pk)
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            # if result is None:
            amount = (lap.amount)*100  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                lap.pay_id = payment_id
                lap.verify = True
                lap.save()
                # render success page on successful caputre of payment
                subject = 'Appointment status'
                message = f''' Appointment Booked Successfully :  {lap.pay_id}
                amount payed:  {lap.amount}
                payment mode :  {lap.pay_method}
                payment time :  {lap.pay_at}
                '''
               
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.session['email'], ]
                send_mail( subject, message, email_from, recipient_list )

                return render(request, 'success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'fail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()  



def donate(request):
    
    return render(request,'donate.html')







def pviewappointment(request):
    uid=User.objects.get(email=request.session['email'])
    appointments=Appointments.objects.filter(Q(patient=uid) & Q(Q(pay_method = 'online') & Q(verify = True) | Q(pay_method='offline')))
    print(appointments)
    return render(request,'pviewappointment.html',{'appointments':appointments,'uid':uid})

def delete(request):
    uid=User.objects.get(id=request.POST['id'])
    uid.delete()

def contact(request):
    try:
        if request.method=='POST':
            
            Contact.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                subject=request.POST['subject'],
                message=request.POST['message'],
            )
        return render(request,'contact.html',{'msg':'ThankYou for contacting Us'})
    except:
        return render(request,'contact.html')