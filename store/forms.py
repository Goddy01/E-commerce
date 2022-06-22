from django import forms
from .models import Product
from .models import category_choices

class AddProductForm(forms.ModelForm):
    category = forms.MultipleChoiceField(choices=category_choices, widget=forms.CheckboxSelectMultiple())

    class Meta():
        model = Product
        fields = ('product_description', 'product_image3', 'product_image2', 'product_image1', 'product_colors', 'number_available', 'product_sizes', 'product_price', 'product_name', 'category_choices')
    # instance = ""