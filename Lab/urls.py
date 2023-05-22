from django.contrib import admin
from django.urls import path,include
from Lab import views

urlpatterns = [
      path('llogin',views.llogin,name="llogin"),
      path('llogout',views.llogout,name="llogout"),
      path('lforgot',views.lforgot,name="lforgot"),
      path('ledit/', views.ledit, name="ledit"),
      path('ldash/', views.ldash, name="ldash"),
      path('lchangepass/', views.lchangepass, name="lchangepass"),
      path('lviewappointment/', views.lviewappointment , name="lviewappointment"),
      path('viewbtn/<int:pk>', views.viewbtn , name="viewbtn"),
      path('rep-up/<int:pk>', views.rep_up , name="rep-up"),
      

]