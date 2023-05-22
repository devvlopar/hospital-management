from django.contrib import admin

from Lab.models import Assistants, Lappointment, Test

# Register your models here.
@admin.register(Assistants)
class AdminAssistants(admin.ModelAdmin):
    list_display=['id','name','email','password','phone','lab_pic']


@admin.register(Test)
class AdminTest(admin.ModelAdmin):
    list_display=['id','test_name','amount']


@admin.register(Lappointment)
class AdminLappointment(admin.ModelAdmin):
    list_display=['id','lab','test','patient','date','time','pay_id','amount','pay_at','verify','pay_method']