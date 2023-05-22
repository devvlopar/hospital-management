from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    
    path('dlogin/', views.dlogin, name="dlogin"),
    path('dlogout/', views.dlogout, name="dlogout"),
    path('dforgot/', views.dforgot, name="dforgot"),
    path('dchangepass/', views.dchangepass, name="dchangepass"),
    path('dedit/', views.dedit, name="dedit"),
    path('ddash/', views.ddash, name="ddash"),
    path('viewappointment/', views.viewappointment, name="viewappointment"),
    path('search/', views.search, name="search"),
]
