from django.contrib import admin
from django.forms.formsets import ORDERING_FIELD_NAME
from .models import Store, Cake, Order, Review, Store_Menu
# Register your models here.

admin.site.register(Store)
admin.site.register(Order)
admin.site.register(Cake)
admin.site.register(Review)
admin.site.register(Store_Menu)