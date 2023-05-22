from django.contrib import admin

from Doctor.models import Doctors

# Register your models here.
@admin.register(Doctors)
class AdminDoctors(admin.ModelAdmin):
    list_display=['id','doctorname','doctoremail','password','phone','specialization','doc_pic']