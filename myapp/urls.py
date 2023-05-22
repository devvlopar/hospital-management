from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
      path('getspe/',views.getspe,name="getspe"),
      
      path('',views.index,name="index"),
      path('np/',views.np,name="np"),

      path('register/',views.register,name="register"),
      path('plogin/',views.plogin,name="plogin"),
      path('covid/',views.covid,name="covid"),
      path('cancer/',views.cancer,name="cancer"),
      path('generic/',views.generic,name="generic"),
      path('organ/',views.organ,name="organ"),
      path('services/',views.services,name="services"),
      path('about/',views.about,name="about"),
      path('contact/',views.contact,name="contact"),
      path('otp/',views.otp,name="otp"),
      path('pdash/',views.pdash,name="pdash"),
      path('dashboard/',views.dashboard,name="dashboard"),
      path('plogout/',views.plogout,name="plogout"),
      path('pedit/',views.pedit,name="pedit"),
      path('pforgot/',views.pforgot,name="pforgot"),
      path('pchangepass/',views.pchangepass,name="pchangepass"),
      path('appointment/',views.appointment,name="appointment"),
      path('donate/',views.donate,name="donate"),
      
      
      
      path('pviewappointment/',views.pviewappointment,name="pviewappointment"),
      path('delete/',views.delete,name="delete"),
      
      path('lappointment/',views.lappointment,name="lappointment"),

      # path('pay/', views.pay, name='pay'),
      path('appointment/docpaymenthandler/<int:pk>', views.docpaymenthandler, name='docpaymenthandler'),
      path('lappointment/labpaymenthandler/<int:pk>',views.labpaymenthandler,name="labpaymenthandler"),
     
      

]
