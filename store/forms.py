from django import forms
from .models import Product

class AddProductForm(forms.ModelForm):
    CATEGORY_CHOICES = (
    ("M", "MEN"), 
    ("W", "WOMEN"), 
    ("MC", "MALE CHILDREN"), 
    ("FC", "FEMALE CHILDREN"), )
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)

    class Meta():
        model = Product
        fields = ('product_description', 'product_image3', 'product_image2', 'product_image1', 'product_colors', 'number_available', 'product_sizes', 'product_price', 'product_name', 'category')
    # instance = ""