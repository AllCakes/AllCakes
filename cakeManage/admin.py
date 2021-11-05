from django.contrib import admin
from django.forms.formsets import ORDERING_FIELD_NAME
<<<<<<< HEAD
from .models import Store, Cake, Order, Review, Menu, AmountCoupon, PercentCoupon
=======
from .models import Store, Cake, Order, Review, Store_Menu
>>>>>>> e7291f2fc268c690f2f2c91dbc367e7afa2c17c3
# Register your models here.

admin.site.register(Store)
admin.site.register(Order)
admin.site.register(Cake)
admin.site.register(Review)
<<<<<<< HEAD
admin.site.register(AmountCoupon)
admin.site.register(PercentCoupon)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['user','referred_cake','rate', 'comment']
#     readonly_fields = ['pub_date',]
=======
admin.site.register(Store_Menu)
>>>>>>> e7291f2fc268c690f2f2c91dbc367e7afa2c17c3
