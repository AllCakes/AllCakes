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
admin.site.register(Menu_Color)
admin.site.register(Menu_Cream)