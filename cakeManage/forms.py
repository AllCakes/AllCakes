from django import forms
from .models import Review, Store, Cake, Order, Store_Menu

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'store_image','meta_body', 'text', 'contact', 'locationSi', 'locationGu']

class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['cakename', 'body', 'meta_body', 'cake_image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=['pickup_date','pickup_time','lettering_position','원하시는도안사진첨부',]
        
class LocationSearchForm(forms.Form):
    search_word=forms.CharField(label='Search word')  

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=['comment','review_img',]

class StoreMenuForm(forms.ModelForm):
    class Meta:
        model = Store_Menu
        fields=[]