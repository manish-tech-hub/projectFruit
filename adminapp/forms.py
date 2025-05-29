from django import forms
from ecomapp import models
Product = models.Product

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=[
            'product_name','product_price','product_image','available_quantity','product_desc'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'input-field'}),
            'product_price': forms.NumberInput(attrs={'class': 'input-field'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'input-field'}),
            'product_desc': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
        }

        