from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Dun)
admin.site.register(Applicant)
admin.site.register(FamilyMember)
admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'status')

