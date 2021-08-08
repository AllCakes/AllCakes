from django.contrib import admin
from django.forms.formsets import ORDERING_FIELD_NAME
from .models import Store, CakeImage, Cake, Order, Review
# Register your models here.

admin.site.register(Store)
admin.site.register(CakeImage)
admin.site.register(Order)
admin.site.register(Cake)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','referred_store','referred_cake','rate', 'comment']
    readonly_fields = ['pub_date',]