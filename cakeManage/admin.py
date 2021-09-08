from django.contrib import admin
from django.forms.formsets import ORDERING_FIELD_NAME
from .models import Store, Cake, Order, Review, Menu
# Register your models here.

admin.site.register(Store)
admin.site.register(Order)
admin.site.register(Cake)
admin.site.register(Menu)
admin.site.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['user','referred_cake','rate', 'comment']
#     readonly_fields = ['pub_date',]