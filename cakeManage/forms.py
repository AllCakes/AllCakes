from django import forms
from .models import Search, Store, Cake, Order
from django.forms import Form

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'store_image','meta_body', 'text', 'contact', 'location']
        
class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['cakename', 'body', 'meta_body', 'cake_image', '맛','모양','사이즈','크림종류','레터링색']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=['희망픽업일','희망픽업시간','레터링위치','원하시는도안사진첨부',]
        
class LocationSearchForm(forms.Form):
    search_word=forms.CharField(label='Search word')  
