from django.contrib import admin
from django.forms.formsets import ORDERING_FIELD_NAME
from .models import *
# Register your models here.

admin.site.register(Store)
admin.site.register(Order)
admin.site.register(Cake)
admin.site.register(Review)
admin.site.register(AmountCoupon)
admin.site.register(PercentCoupon)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['user','referred_cake','rate', 'comment']
#     readonly_fields = ['pub_date',]
admin.site.register(Store_Menu)