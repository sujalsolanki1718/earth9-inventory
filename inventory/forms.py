from django import forms
from .models import Product, Bill

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer_name', 'total_amount']
