from django import forms
from .models import Store, Cake, Order, Review
from .widgets import starWidget

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'store_image', 'text', 'contact', 'location']

class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['cakename','body']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=['name','연락처','희망픽업일','희망픽업시간','맛','모양','사이즈','원하시는도안사진첨부',]
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields =  ['body']
        # widgets = {
        #     'grade': starWidget,
        # }