from django import forms
from django.forms import widgets
from .models import *

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'store_image','meta_body', 'text', 'contact', 'locationSi', 'locationGu']
        
class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['cakename', 'body', 'meta_body', 'cake_image', 'size', 'price']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cakename'].widget.attrs.update({'class': 'form-control','style': 'width: 100%'})
        self.fields['body'].widget.attrs.update({'class': 'form-control','style': 'width: 100%'})

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=['pickup_date','pickup_time','lettering_position','원하시는도안사진첨부',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lettering_position'].widget.attrs.update({'class': 'butn'})
        self.fields['lettering_position'].widget.attrs.update({'data-key': 'letter'})
        
class LocationSearchForm(forms.Form):
    search_word=forms.CharField(label='Search word')  

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=['review_img','comment']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_img'].widget.attrs.update({'style': 'border-radius: 5px'})

class StoreMenuForm(forms.ModelForm):
    class Meta:
        model = Store_Menu
        fields=[]