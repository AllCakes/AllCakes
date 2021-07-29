from django.contrib import admin
from django.forms.formsets import ORDERING_FIELD_NAME
from .models import Store, CakeImage, Cake, Order, Review
from .forms import ReviewForm
# Register your models here.

admin.site.register(Store)
admin.site.register(CakeImage)
admin.site.register(Order)
admin.site.register(Cake)
admin.site.register(Review)
# @admin.register(Review)
# class ReviewAmin(admin.ModelAdmin):
#     form = ReviewForm