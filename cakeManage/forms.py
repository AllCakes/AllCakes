from django import forms
from .models import Store, Cake, Order

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'store_image', 'text', 'contact', 'location']

class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['cakename', 'body', 'cake_image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=['희망픽업일','희망픽업시간','맛','모양','사이즈','크림종류','레터링위치','레터링색','원하시는도안사진첨부',]
